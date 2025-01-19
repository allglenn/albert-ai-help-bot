# Albert AI Integration Demo

## About the Project

This project serves as a demonstration of integrating Albert AI, a French government initiative that provides state agencies access to open-source AI models. Albert AI is part of France's strategy to democratize AI usage within public services while maintaining data sovereignty and promoting open-source solutions.

## Technical Stack

### Backend (API)
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server implementation
- **Python 3.11**: Latest stable version with improved performance

### Frontend (UI)
- **React 18**: JavaScript library for building user interfaces
- **React Hooks**: For state management and side effects
- **Fetch API**: For making HTTP requests to the backend

### Infrastructure
- **Docker**: Containerization of both frontend and backend services
- **Docker Compose**: For orchestrating the multi-container application
- **Hot Reloading**: Supported for both frontend and backend development

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/allglenn/albert-ai-help-bot.git
cd albert-ai-help-bot
```

2. Create a .env file (optional):
```bash
cp .env.example .env
# Edit .env with your Albert AI credentials
```

3. Start the application:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

The project is configured for an optimal development experience:
- Frontend changes are automatically reflected thanks to React's development server
- Backend changes trigger automatic reloads through Uvicorn's reload feature
- Docker volumes ensure persistent development without rebuilding containers

## Integration with Albert AI

This demonstration project showcases how to:
- Connect to Albert AI's API endpoints
- Handle authentication and authorization
- Process AI model responses
- Present results through a modern web interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Albert AI team for providing the API infrastructure
- French government's digital services for promoting open-source AI solutions

