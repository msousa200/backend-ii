from prometheus_client import Gauge, Histogram

PROCESSING_TIME = Histogram(
    "text_processing_duration_seconds",
    "Time spent processing text",
    ["processing_type"]
)

TASKS_TOTAL = Gauge(
    "text_processing_tasks_total",
    "Total number of text processing tasks",
    ["status"]
)

TASK_QUEUE_SIZE = Gauge(
    "text_processing_queue_size",
    "Size of the text processing task queue"
)
