# Notes API

A secure RESTful API for managing notes with user authentication, sharing capabilities, and advanced features.

## Features

### Core Features
- ✅ User registration and authentication (JWT)
- ✅ Full CRUD operations for notes
- ✅ Share notes with other users
- ✅ Secure access control (users can only access their own notes or shared notes)
- ✅ OpenAPI documentation

### Custom Features (Bonus)
- 📌 **Pin Notes**: Pin important notes to keep them at the top
- 🔍 **Full-text Search**: Search across note titles and content
- 📄 **Pagination**: Efficient data loading with skip/limit parameters
- 🔒 **Comprehensive Security**: Input validation, password hashing, JWT tokens

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (optional, defaults to SQLite):
```
DATABASE_URL=sqlite:///./notes.db
SECRET_KEY=your-secret-key-here
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - Login and get JWT token

### Notes Management
- `GET /notes` - Get all notes (with pagination and search)
- `GET /notes/{id}` - Get a specific note
- `POST /notes` - Create a new note
- `PUT /notes/{id}` - Update a note
- `DELETE /notes/{id}` - Delete a note

### Sharing & Features
- `POST /notes/{id}/share` - Share a note with another user
- `POST /notes/{id}/pin` - Pin/unpin a note
- `GET /search?q=keyword` - Full-text search

### Info
- `GET /about` - API and developer information
- `GET /` - API status

## Usage Examples

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 3. Create a Note
```bash
curl -X POST "http://localhost:8000/notes" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Note content here"}'
```

### 4. Share a Note
```bash
curl -X POST "http://localhost:8000/notes/1/share" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"share_with_email": "friend@example.com"}'
```

### 5. Pin a Note
```bash
curl -X POST "http://localhost:8000/notes/1/pin" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_pinned": true}'
```

### 6. Search Notes
```bash
curl -X GET "http://localhost:8000/search?q=keyword" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Database

By default, the application uses SQLite (`notes.db`). For production, you can use PostgreSQL by setting the `DATABASE_URL` environment variable:

```
DATABASE_URL=postgresql://user:password@localhost:5432/notesdb
```

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Input validation using Pydantic
- SQL injection prevention via SQLAlchemy ORM
- Access control for note operations
- Secure password requirements (minimum 6 characters)

## Deployment

### Using Render, Railway, or similar platforms:

1. Push your code to GitHub
2. Connect your repository to the platform
3. Set environment variables:
   - `DATABASE_URL` (if using PostgreSQL)
   - `SECRET_KEY` (generate a secure random key)
4. Deploy!

### Using Docker (optional):

```bash
docker build -t notes-api .
docker run -p 8000:8000 notes-api
```

## Testing

Test the API using the interactive documentation at `/docs` or use tools like:
- Postman
- curl
- httpie
- Python requests library

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication logic
│   ├── database.py      # Database configuration
│   └── config.py        # Settings and configuration
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## License

MIT
