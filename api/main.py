from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import user as user_views

app = FastAPI(title="Albert AI Integration Demo", version="1.0.0", description="This is a demo application that demonstrates the integration of Albert AI, a French government initiative that provides state agencies with access to open-source AI models. Albert AI is designed to democratize access to artificial intelligence technologies within French public services. This project showcases how public services can integrate with Albert AI's APIs using a modern web stack. It provides a simple interface to interact with AI services while following French government security and accessibility guidelines.")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(user_views.router, prefix="/api/v1") 