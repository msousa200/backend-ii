import asyncio
import time
import random
from typing import List, Dict, Any
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def task_with_random_duration(name: str, min_delay: float, max_delay: float) -> str:
    """Simulates a task with random execution time"""
    delay = random.uniform(min_delay, max_delay)
    logger.info(f"Task {name} started, will take {delay:.2f} seconds")
    
    try:
        await asyncio.sleep(delay)
        logger.info(f"Task {name} completed successfully")
        return f"{name} completed in {delay:.2f}s"
    except asyncio.CancelledError:
        logger.warning(f"Task {name} was cancelled")
        raise  

async def run_tasks_with_timeout(timeout: float = 2.0) -> Dict[str, Any]:
    """
    Launch multiple tasks and handle timeouts gracefully
    
    Args:
        timeout: Maximum time to wait for tasks (in seconds)
        
    Returns:
        Dictionary with results and task status information
    """
    tasks = [
        asyncio.create_task(task_with_random_duration(f"Task {i}", 0.5, 3.0))
        for i in range(1, 6)  
    ]
    
    results = {
        "completed": [],
        "timed_out": [],
        "cancelled": 0
    }
    
    try:
        done, pending = await asyncio.wait(
            tasks, 
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED
        )
        
        for task in done:
            try:
                result = task.result()
                results["completed"].append(result)
            except Exception as e:
                logger.error(f"Task failed with error: {e}")
        
        results["timed_out"] = [f"Task {i+1}" for i, task in enumerate(tasks) if task in pending]
        results["cancelled"] = len(pending)
        
        for task in pending:
            task.cancel()
            
        if pending:
            await asyncio.wait(pending, return_when=asyncio.ALL_COMPLETED)
            logger.info(f"Cancelled {len(pending)} tasks that exceeded timeout")
    
    except Exception as e:
        logger.error(f"Error while waiting for tasks: {e}")
        for task in tasks:
            if not task.done():
                task.cancel()
    
    return results


async def main():
    logger.info("\n=== EXERCISE: Tasks with Timeout ===")
    timeout_results = await run_tasks_with_timeout(timeout=1.5)
    logger.info(f"Timeout results: {timeout_results}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

