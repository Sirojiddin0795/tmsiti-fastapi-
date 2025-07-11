# TMSITI Backend API 
<h1>https://tmsiti-fastapi.onrender.com</h1>

A comprehensive FastAPI backend system for the Technical Standardization and Research Institute (TMSITI) website with multilingual support, role-based authentication, and document management capabilities.

## Features

- **Multi-language Support**: Uzbek, Russian, and English localization
- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Content Management**: News, announcements, regulations, and institute information
- **File Upload**: Support for images and PDF documents
- **Database**: SQLite for development, easily configurable for production
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Admin Panel**: Administrative endpoints for content management

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: JWT tokens with bcrypt password hashing
- **File Processing**: Pillow for image handling
- **Validation**: Pydantic for request/response validation
- **Documentation**: OpenAPI/Swagger auto-generation

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tmsiti-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python create_tables.py
```

5. Run the development server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Default Admin Access

After running the database initialization script, you can access the admin panel with:

- **Username**: `admin`
- **Email**: `admin@tmsiti.uz`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login!

## Project Structure

```
tmsiti-backend/
├── app/
│   ├── api/
│   │   └── v1/           # API routes
│   ├── core/             # Core functionality
│   ├── db/
│   │   └── models/       # Database models
│   ├── middlewares/      # Custom middleware
│   ├── schemas/          # Pydantic schemas
│   ├── localization/     # Language files
│   └── main.py          # FastAPI application
├── static/              # Static files and uploads
├── create_tables.py     # Database initialization
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
└── README.md           # This file
```

## Environment Variables

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=sqlite:///./tmsiti.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ADMIN_PASSWORD=admin123

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=static/uploads

# Application
DEBUG=False
DEFAULT_LANGUAGE=uz
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout

### Content Management
- `GET /api/v1/news` - Get news articles
- `POST /api/v1/news` - Create news article (Admin/Moderator)
- `GET /api/v1/announcements` - Get announcements
- `POST /api/v1/announcements` - Create announcement (Admin/Moderator)

### Institute Information
- `GET /api/v1/institute/about` - About institute
- `GET /api/v1/institute/management` - Management information
- `GET /api/v1/institute/structure` - Organizational structure
- `GET /api/v1/institute/vacancies` - Current vacancies

### Regulations
- `GET /api/v1/regulations/laws` - Laws and regulations
- `GET /api/v1/regulations/standards` - Technical standards
- `GET /api/v1/regulations/building` - Building regulations

### Activities
- `GET /api/v1/activities/management-system` - Management system certification
- `GET /api/v1/activities/laboratory` - Laboratory services

### Contact
- `POST /api/v1/contact/inquiry` - Submit contact inquiry
- `GET /api/v1/contact/anti-corruption` - Anti-corruption information

## Docker Deployment

### Using Docker Compose (Recommended)

1. Build and run the application:
```bash
docker-compose up --build
```

2. Access the application at `http://localhost:8000`

### Using Docker directly

1. Build the image:
```bash
docker build -t tmsiti-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 tmsiti-backend
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Style

The project follows PEP 8 guidelines. Use tools like `black` and `flake8` for formatting:

```bash
pip install black flake8
black .
flake8 .
```

### Database Migrations

For database schema changes:

1. Update models in `app/db/models/`
2. Run the initialization script:
```bash
python create_tables.py
```

## Localization

The application supports three languages:
- Uzbek (uz) - Default
- Russian (ru)
- English (en)

Language files are located in `app/localization/` and are automatically loaded based on request headers or query parameters.

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- Role-based access control
- File upload validation
- CORS protection
- Input validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For questions or issues:
- Email: support@tmsiti.uz
- Documentation: Check API docs at `/docs`
- Issues: Submit on the project repository

## Changelog

### v1.0.0 (2024-01-XX)
- Initial release
- Multi-language support
- Authentication system
- Content management
- File upload functionality
- Docker support
