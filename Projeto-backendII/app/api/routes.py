from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.future import select
from sqlalchemy import update, desc, func
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional
import asyncio
import time
import json
import uuid
import os

from app.models.database import TextTask, Base
from app.db.deps import get_db
from app.db.database import SessionLocal
from app.models.pydantic_models import (
    TextProcessingRequest, TextProcessingResponse, TextProcessingStatusResponse,
    ProcessingType, ProcessingStatus, TaskMetadata, LanguageDetectionRequest, 
    LanguageDetectionResponse, DateTimeEncoder
)
from app.services.crew_service import CrewAIService
from app.utils.logging_util import api_logger, PerformanceTimer
from app.utils.metrics import TASKS_TOTAL, TASK_QUEUE_SIZE, PROCESSING_TIME
from app.services.language_service import LanguageService

api_router = APIRouter()

crew_service = CrewAIService()

@api_router.post("/process-text", response_model=TextProcessingStatusResponse)
async def process_text(
    request: TextProcessingRequest,
    background_tasks: BackgroundTasks,
    req: Request,
    db: SessionLocal = Depends(get_db)
):
    request_id = str(uuid.uuid4())
    request_data = request.model_dump()
    if len(request_data["text"]) > 100:
        request_data["text"] = request_data["text"][:100] + "..."
    api_logger.log_request(
        endpoint="/api/process-text",
        method="POST",
        request_data=request_data,
        request_id=request_id
    )
    
    start_time = time.time()
    
    try:
        with PerformanceTimer("api_process_text_request") as timer:
            metadata = TaskMetadata(
                request_id=request_id,
                client_ip=str(req.client.host) if req.client else "unknown",
                target_language=request.target_language if request.processing_type == ProcessingType.TRANSLATION else None,
                model_used=os.getenv("OLLAMA_MODEL", "tinyllama")
            )
            
            metadata_dict = metadata.model_dump()
            metadata_json = json.dumps(metadata_dict)
            
            text_task = TextTask(
                original_text=request.text,
                processing_type=request.processing_type.value,
                status=ProcessingStatus.PENDING.value,
                task_metadata=metadata_json
            )
            
            db.add(text_task)
            db.commit()
            db.refresh(text_task)
            
            timer.add_info("task_id", text_task.id)
            
            TASKS_TOTAL.labels(status=ProcessingStatus.PENDING.value).inc()
            TASK_QUEUE_SIZE.inc()
            
            background_tasks.add_task(
                process_text_task,
                text_task.id,
                request.text,
                request.processing_type.value,
                request_id
            )
            
            response_dict = {
                "id": text_task.id,
                "status": text_task.status,
                "processing_type": text_task.processing_type,
                "created_at": text_task.created_at,
                "updated_at": text_task.updated_at
            }
            response = TextProcessingStatusResponse(**response_dict)
            
            duration_ms = (time.time() - start_time) * 1000
            api_logger.log_response(
                endpoint="/api/process-text",
                request_id=request_id,
                status_code=200,
                response_data=json.loads(json.dumps(response.model_dump(), cls=DateTimeEncoder)),
                duration_ms=duration_ms
            )
            
            return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        api_logger.log_response(
            endpoint="/api/process-text",
            request_id=request_id,
            status_code=500,
            response_data={"error": str(e)},
            duration_ms=duration_ms
        )
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@api_router.get("/tasks/{task_id}", response_model=TextProcessingResponse)
async def get_task(task_id: int, db: SessionLocal = Depends(get_db)):
    request_id = str(uuid.uuid4())
    api_logger.log_request(
        endpoint=f"/api/tasks/{task_id}",
        method="GET",
        request_id=request_id
    )
    
    start_time = time.time()
    
    try:
        with PerformanceTimer("api_get_task") as timer:
            result = db.execute(select(TextTask).where(TextTask.id == task_id))
            task = result.scalars().first()
            
            timer.add_info("task_id", task_id)
            
            if not task:
                duration_ms = (time.time() - start_time) * 1000
                api_logger.log_response(
                    endpoint=f"/api/tasks/{task_id}",
                    request_id=request_id,
                    status_code=404,
                    duration_ms=duration_ms
                )
                raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
            
            duration_ms = (time.time() - start_time) * 1000
            response_data = {
                "id": task.id,
                "status": task.status,
                "processing_type": task.processing_type
            }
            api_logger.log_response(
                endpoint=f"/api/tasks/{task_id}",
                request_id=request_id,
                status_code=200,
                response_data=response_data,
                duration_ms=duration_ms
            )
            
            return task
    except HTTPException:
        raise
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        api_logger.log_response(
            endpoint=f"/api/tasks/{task_id}",
            request_id=request_id,
            status_code=500,
            response_data={"error": str(e)},
            duration_ms=duration_ms
        )
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")

@api_router.get("/tasks", response_model=List[TextProcessingStatusResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    processing_type: str = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: SessionLocal = Depends(get_db)
):
    request_id = str(uuid.uuid4())
    api_logger.log_request(
        endpoint="/api/tasks",
        method="GET",
        request_data={"skip": skip, "limit": limit, "status": status, 
                     "processing_type": processing_type, "sort_by": sort_by,
                     "sort_order": sort_order},
        request_id=request_id
    )
    
    start_time = time.time()
    
    try:
        with PerformanceTimer("api_list_tasks") as timer:
            query = select(TextTask)
            
            if status:
                query = query.where(TextTask.status == status)
            if processing_type:
                query = query.where(TextTask.processing_type == processing_type)
            
            if sort_by in ["created_at", "updated_at", "processing_type", "status", "id"]:
                sort_column = getattr(TextTask, sort_by)
                if sort_order.lower() == "desc":
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(sort_column)
            else:
                query = query.order_by(desc(TextTask.created_at))
            
            query = query.offset(skip).limit(limit)
            
            result = db.execute(query)
            tasks = result.scalars().all()
            
            count_query = select(func.count()).select_from(TextTask)
            if status:
                count_query = count_query.where(TextTask.status == status)
            if processing_type:
                count_query = count_query.where(TextTask.processing_type == processing_type)
                
            count_result = db.execute(count_query)
            total_count = count_result.scalar()
            
            timer.add_info("total_count", total_count)
            timer.add_info("returned_count", len(tasks))
            
            duration_ms = (time.time() - start_time) * 1000
            api_logger.log_response(
                endpoint="/api/tasks",
                request_id=request_id,
                status_code=200,
                response_data={"count": len(tasks), "total": total_count},
                duration_ms=duration_ms
            )
            
            return tasks
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        api_logger.log_response(
            endpoint="/api/tasks",
            request_id=request_id,
            status_code=500,
            response_data={"error": str(e)},
            duration_ms=duration_ms
        )
        raise HTTPException(status_code=500, detail=f"Error listing tasks: {str(e)}")

def process_text_task(task_id: int, text: str, processing_type: str, request_id: str = None):
    from app.utils.logging_util import PerformanceTimer, crew_logger, db_logger
    from app.services.language_service import LanguageService
    from app.db.database import SessionLocal
    
    session = SessionLocal()
    
    if not request_id:
        request_id = str(uuid.uuid4())
    
    with PerformanceTimer("background_process_text") as timer:
        timer.add_info("task_id", task_id)
        timer.add_info("processing_type", processing_type)
        timer.add_info("request_id", request_id)
        
        try:
            db_logger.info(f"Starting background task for task_id={task_id}, type={processing_type}")
            
            TASKS_TOTAL.labels(status=ProcessingStatus.PENDING.value).dec()
            TASKS_TOTAL.labels(status=ProcessingStatus.PROCESSING.value).inc()
            TASK_QUEUE_SIZE.dec()
            
            session.execute(
                update(TextTask)
                .where(TextTask.id == task_id)
                .values(status=ProcessingStatus.PROCESSING.value)
            )
            session.commit()
            
            task_result = session.execute(select(TextTask).where(TextTask.id == task_id))
            task = task_result.scalars().first()
            
            target_language = None
            metadata = {}
            if task.task_metadata:
                try:
                    metadata = json.loads(task.task_metadata)
                    if isinstance(metadata, dict) and 'target_language' in metadata:
                        target_language = metadata['target_language']
                        timer.add_info("target_language", target_language)
                except json.JSONDecodeError:
                    timer.add_info("metadata_error", "JSON decode error")
            
            crew_logger.info(f"Processing {processing_type} task {task_id} with CrewAI")
            timer.add_info("text_length", len(text))
        
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            processed_text = loop.run_until_complete(crew_service.process_text(text, processing_type, target_language))
            loop.close()
            
            if hasattr(processed_text, 'raw'):
                processed_text = processed_text.raw
            else:
                processed_text = str(processed_text)
                
            timer.add_info("result_length", len(processed_text))
                
            if processing_type == "translation":
                crew_logger.info(f"Cleaning translation output for task {task_id}")
                processed_text = LanguageService.clean_translation_output(processed_text, text)
                processed_text, is_valid = LanguageService.validate_translation(processed_text, text)
                timer.add_info("translation_valid", is_valid)
            
            crew_logger.info(f"Task {task_id} completed successfully")
            
            TASKS_TOTAL.labels(status=ProcessingStatus.PROCESSING.value).dec()
            TASKS_TOTAL.labels(status=ProcessingStatus.COMPLETED.value).inc()
            
            processing_duration = timer.duration if hasattr(timer, 'duration') else time.time() - timer.start_time
            if isinstance(processing_duration, float):
                PROCESSING_TIME.labels(processing_type=processing_type).observe(processing_duration)
            
            session.execute(
                update(TextTask)
                .where(TextTask.id == task_id)
                .values(processed_text=processed_text, status=ProcessingStatus.COMPLETED.value)
            )
            session.commit()
            
        except Exception as e:
            crew_logger.error(f"Error processing task {task_id}: {str(e)}", exc_info=True)
            timer.add_info("error", str(e))
            
            TASKS_TOTAL.labels(status=ProcessingStatus.PROCESSING.value).dec()
            TASKS_TOTAL.labels(status=ProcessingStatus.FAILED.value).inc()
            
            session.execute(
                update(TextTask)
                .where(TextTask.id == task_id)
                .values(status=ProcessingStatus.FAILED.value, processed_text=f"Error: {str(e)}")
            )
            session.commit()
        finally:
            session.close()

@api_router.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(
    request: LanguageDetectionRequest,
    req: Request
):
    request_id = str(uuid.uuid4())
    request_data = request.model_dump()
    if len(request_data["text"]) > 100:
        request_data["text"] = request_data["text"][:100] + "..."
    api_logger.log_request(
        endpoint="/api/detect-language",
        method="POST",
        request_data=request_data,
        request_id=request_id
    )
    
    start_time = time.time()
    
    try:
        with PerformanceTimer("api_detect_language") as timer:
            language, confidence = LanguageService.detect_language(request.text)
            
            response = LanguageDetectionResponse(
                language=language,
                confidence=confidence,
                text_length=len(request.text)
            )
            
            duration_ms = (time.time() - start_time) * 1000
            api_logger.log_response(
                endpoint="/api/detect-language",
                request_id=request_id,
                status_code=200,
                response_data=response.model_dump(),
                duration_ms=duration_ms
            )
            
            return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        api_logger.log_response(
            endpoint="/api/detect-language",
            request_id=request_id,
            status_code=500,
            response_data={"error": str(e)},
            duration_ms=duration_ms
        )
        raise HTTPException(status_code=500, detail=f"Error detecting language: {str(e)}")
