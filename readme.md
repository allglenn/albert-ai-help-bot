# Albert AI Integration Demo

## About the Project

This project serves as a demonstration of integrating Albert AI, a French government initiative that provides state agencies access to open-source AI models. Albert AI is part of France's strategy to democratize AI usage within public services while maintaining data sovereignty and promoting open-source solutions.

## Technical Stack

### Backend (API)
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **PostgreSQL**: Robust, open-source database
- **JWT**: JSON Web Tokens for secure authentication
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

## Features

### Authentication
- Secure JWT-based authentication
- Token blacklisting for logout functionality
- Password hashing with bcrypt
- Protected routes with dependency injection
- Automatic token expiration

### User Management
- User registration with email validation
- Secure password storage
- User profile retrieval
- Email uniqueness enforcement
- Active/inactive user status

### Database
- PostgreSQL integration
- Async database operations
- Migration support
- Token blacklist management
- Automatic cleanup of expired tokens

## Project Structure
```
project/
├── api/                 # FastAPI backend
│   ├── controllers/     # Business logic
│   ├── models/         # Pydantic models
│   ├── services/       # Service layer
│   ├── views/          # API endpoints
│   ├── db/             # Database models and config
│   ├── utils/          # Utility functions
│   └── config.py       # Application configuration
├── ui/                 # React frontend
└── docker-compose.yml  # Docker composition
```

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

## API Endpoints

### Authentication
- `POST /api/v1/auth/login`: JSON login endpoint
- `POST /api/v1/auth/token`: Form-based login endpoint
- `POST /api/v1/auth/logout`: Logout and invalidate token

### Users
- `POST /api/v1/users/`: Create new user
- `GET /api/v1/users/me`: Get current user profile
- `GET /api/v1/users/{user_id}`: Get user by ID

## Development

The project is configured for an optimal development experience:
- Frontend changes are automatically reflected thanks to React's development server
- Backend changes trigger automatic reloads through Uvicorn's reload feature
- Docker volumes ensure persistent development without rebuilding containers
- PostgreSQL data persists across container restarts

### Environment Variables

Key environment variables (see .env.example for full list):
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key
- `ALBERT_AI_API_KEY`: API key for Albert AI services
- `DEBUG`: Enable/disable debug mode

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Token blacklisting for secure logout
- Database-level email uniqueness
- Protected API endpoints
- CORS configuration
- Environment variable separation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Albert AI team for providing the API infrastructure
- French government's digital services for promoting open-source AI solutions

