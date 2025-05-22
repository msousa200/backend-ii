"""
Modelos ORM do banco de dados.
Mantenha aqui apenas as classes das tabelas.
"""

import json
from typing import Dict, Any, Optional
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, 
    func, CheckConstraint, Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import validates
from app.db.database import Base
from app.models.pydantic_models import ProcessingType, ProcessingStatus

class TextTask(Base):
    __tablename__ = "text_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    __table_args__ = (
        Index('idx_status_created', 'status', 'created_at'),
        Index('idx_type_status', 'processing_type', 'status'),
    )

    original_text = Column(
        Text,
        CheckConstraint(
            "LENGTH(original_text) <= 50000",
            name='check_original_text_length'
        ),
        nullable=False
    )
    processed_text = Column(
        Text, 
        nullable=True,
    )

    processing_type = Column(
        String(50), 
        nullable=False,
        index=True,
    )
    status = Column(
        String(20), 
        nullable=False,
        default=ProcessingStatus.PENDING.value,
        index=True,
    )

    task_metadata = Column(
        JSONB(none_as_null=True).with_variant(Text, "sqlite"),
        nullable=True,
        comment="JSON metadata with additional task parameters such as target_language"
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True
    )

    @property
    def duration(self) -> float:
        if self.status != ProcessingStatus.COMPLETED.value or not self.updated_at:
            return 0.0
        return (self.updated_at - self.created_at).total_seconds()

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        if not self.task_metadata:
            return {}
        try:
            if isinstance(self.task_metadata, str):
                return json.loads(self.task_metadata)
            return self.task_metadata
        except (json.JSONDecodeError, AttributeError):
            return {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary with serializable values"""
        result = {
            "id": self.id,
            "processing_type": self.processing_type,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if hasattr(self, "original_text"):
            result["original_text"] = self.original_text
        if hasattr(self, "processed_text") and self.processed_text:
            result["processed_text"] = self.processed_text
        if self.task_metadata:
            result["metadata"] = self.metadata_dict
        return result

    @validates('processing_type')
    def validate_processing_type(self, key: str, value: str) -> str:
        if value not in [t.value for t in ProcessingType]:
            raise ValueError(f"Invalid processing type: {value}")
        return value

    @validates('status')
    def validate_status(self, key: str, value: str) -> str:
        if value not in [s.value for s in ProcessingStatus]:
            raise ValueError(f"Invalid status: {value}")
        return value

    @validates('task_metadata')
    def validate_metadata(self, key: str, value: Optional[Dict[str, Any]]) -> Optional[str]:
        if value is None:
            return None
            
        if isinstance(value, str):
            try:
                json.loads(value)
                return value
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in task_metadata")
                
        if isinstance(value, dict):
            return json.dumps(value)
            
        raise ValueError("task_metadata must be a dictionary or JSON string")

    def __repr__(self) -> str:
        return (f"<TextTask(id={self.id}, type={self.processing_type}, "
                f"status={self.status}, created_at={self.created_at})>")