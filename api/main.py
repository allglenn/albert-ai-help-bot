from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import user as user_views
from views import auth as auth_views
from db.database import init_db
from middleware.error_handler import error_handler_middleware
from services.monitoring import MonitoringService
import asyncio
from prometheus_client import generate_latest
from fastapi.responses import Response
from views import help_assistant

app = FastAPI(title="Albert AI Integration Demo", version="1.0.0", description="This is a demo application that demonstrates the integration of Albert AI, a French government initiative that provides state agencies with access to open-source AI models. Albert AI is designed to democratize access to artificial intelligence technologies within French public services. This project showcases how public services can integrate with Albert AI's APIs using a modern web stack. It provides a simple interface to interact with AI services while following French government security and accessibility guidelines.")

# Initialize monitoring first
MonitoringService.init_monitoring(app)

# Add error handling middleware
app.middleware("http")(error_handler_middleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest().decode(), media_type="text/plain")

# Include routers
app.include_router(auth_views.router, prefix="/api/v1")
app.include_router(user_views.router, prefix="/api/v1")
app.include_router(help_assistant.router, prefix="/api/v1") 