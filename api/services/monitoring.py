from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time
import psutil

# Basic request counter
REQUEST_COUNT = Counter(
    "http_request_count_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

# Request duration histogram
REQUEST_TIME = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

# Basic system metrics
PROCESS_MEMORY = Gauge(
    "process_memory_bytes",
    "Memory usage in bytes"
)

PROCESS_CPU = Gauge(
    "process_cpu_percent",
    "CPU usage percent"
)

class MonitoringService:
    @staticmethod
    def init_monitoring(app):
        @app.middleware("http")
        async def metrics_middleware(request, call_next):
            start_time = time.time()
            
            response = await call_next(request)
            
            # Record request duration
            duration = time.time() - start_time
            REQUEST_TIME.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            # Count request
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=str(response.status_code)
            ).inc()
            
            # Update system metrics
            PROCESS_MEMORY.set(psutil.Process().memory_info().rss)
            PROCESS_CPU.set(psutil.Process().cpu_percent())
            
            return response

        # Add metrics endpoint
        @app.get("/metrics")
        async def metrics():
            return Response(
                content=generate_latest(),
                media_type=CONTENT_TYPE_LATEST
            ) 