import asyncio
import time
import random
from typing import List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AsyncRateLimiter:
    """
    Rate limiter that allows only a fixed number of tasks per second
    
    Uses a semaphore and task scheduling to control execution rate
    """
    
    def __init__(self, tasks_per_second: int):
        """
        Initialize rate limiter
        
        Args:
            tasks_per_second: Maximum number of tasks allowed per second
        """
        self.tasks_per_second = tasks_per_second
        self.interval = 1.0 / tasks_per_second  
        self.semaphore = asyncio.Semaphore(tasks_per_second)
        self.last_released = 0
        logger.info(f"Rate limiter initialized: {tasks_per_second} tasks/second")
    
    async def execute(self, coro, *args, **kwargs):
        """
        Execute a coroutine with rate limiting
        
        Args:
            coro: The coroutine function to execute
            *args, **kwargs: Arguments to pass to the coroutine
            
        Returns:
            The result of the coroutine execution
        """
        async with self.semaphore:
            now = time.time()
            time_since_last = now - self.last_released
            
            if time_since_last < self.interval and self.last_released > 0:
                delay = self.interval - time_since_last
                await asyncio.sleep(delay)
            
            self.last_released = time.time()
            
            return await coro(*args, **kwargs)

async def sample_task(task_id: int) -> str:
    """Sample task for rate limiter demonstration"""
    logger.info(f"Executing task {task_id}")
    await asyncio.sleep(0.1)
    return f"Task {task_id} completed"

async def demo_rate_limiter() -> List[str]:
    """Demonstrate the async rate limiter"""
    rate_limiter = AsyncRateLimiter(tasks_per_second=5)
    
    tasks = []
    for i in range(20):  
        task = asyncio.create_task(
            rate_limiter.execute(sample_task, i)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

async def main():
    logger.info("\n=== CHALLENGE: Rate Limiter ===")
    start_time = time.time()
    rate_limiter_results = await demo_rate_limiter()
    elapsed = time.time() - start_time
    
    logger.info(f"Rate limiter completed {len(rate_limiter_results)} tasks in {elapsed:.2f} seconds")
    logger.info(f"Average rate: {len(rate_limiter_results)/elapsed:.2f} tasks/second")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")