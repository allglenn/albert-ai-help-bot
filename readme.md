# Albert AI Integration Demo

## Table of Contents
- [About the Project](#about-the-project)
- [Technical Stack](#technical-stack)
- [Features](#features)
- [Monitoring](#monitoring)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About the Project
A modern web application demonstrating the integration of Albert AI, a French government initiative providing state agencies with access to open-source AI models. This project showcases how public services can integrate with AI services while following French government security and accessibility guidelines.

## Technical Stack

### Backend
- FastAPI (Python)
- SQLAlchemy (Async)
- PostgreSQL
- JWT Authentication
- Alembic for migrations

### Frontend
- React
- Material-UI (MUI)
- React Router
- Modern JavaScript (ES6+)

### Infrastructure
- Docker & Docker Compose
- Prometheus for monitoring
- Grafana for visualization

## Features
- 🔐 Secure Authentication System
- 👤 User Management
- 🤖 AI Assistant Management
  - Create custom AI assistants
  - Configure assistant capabilities
  - Manage assistant profiles
  - Real-time chat interface
- 📊 Monitoring & Analytics
- 🎨 Modern, Responsive UI
- 🔒 Role-based Access Control

## Project Structure
```
project/
├── api/                      # FastAPI backend
│   ├── controllers/          # Business logic
│   ├── models/              # Pydantic models
│   ├── views/               # API routes
│   ├── services/            # External services
│   ├── db/                  # Database
│   │   ├── models.py        # SQLAlchemy models
│   │   └── database.py      # DB configuration
│   └── config.py            # Application configuration
├── ui/                      # React frontend
│   └── src/
│       ├── pages/
│       │   ├── public/      # Public (unauthenticated) pages
│       │   │   ├── LandingPage.js
│       │   │   ├── LoginPage.js
│       │   │   └── RegisterPage.js
│       │   └── private/     # Protected (authenticated) pages
│       │       ├── Dashboard.js
│       │       ├── ChatPage.js
│       │       └── ProfilePage.js
│       ├── components/
│       │   └── layout/      # Layout components
│       │       ├── PublicLayout.js
│       │       ├── PrivateLayout.js
│       │       └── Navbar.js
│       └── App.js
├── prometheus/              # Prometheus configuration
│   └── prometheus.yml       # Scraping configuration
├── grafana/                 # Grafana configuration
│   └── provisioning/        # Auto-provisioning
│       ├── dashboards/      # Dashboard definitions
│       └── datasources/     # Data source definitions
└── docker-compose.yml       # Docker composition
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js (for local development)
- Python 3.9+ (for local development)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/albert-ai-demo.git
cd albert-ai-demo
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Monitoring: http://localhost:3001

### Development Setup
1. Backend:
```bash
cd api
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

2. Frontend:
```bash
cd ui
npm install
npm start
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Monitoring
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments
- Albert AI team for providing the API infrastructure
- French government's digital services for promoting open-source AI solutions

