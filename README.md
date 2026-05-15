# Notes API

A secure RESTful API for managing notes with user authentication, sharing capabilities, and advanced features.

**🚀 Live Demo:** https://notes-api-l50o.onrender.com

**📚 API Documentation:** https://notes-api-l50o.onrender.com/docs

**Developer:** Varshith (varshithg2004@gmail.com)

---

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
- 🤝 **Note Sharing**: Collaborate by sharing notes with other users

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

## Live API Usage

### Base URL
```
https://notes-api-l50o.onrender.com
```

### Usage Examples

### 1. Register a User
```bash
curl -X POST "https://notes-api-l50o.onrender.com/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Login
```bash
curl -X POST "https://notes-api-l50o.onrender.com/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 3. Create a Note
```bash
curl -X POST "https://notes-api-l50o.onrender.com/notes" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Note content here"}'
```

### 4. Share a Note
```bash
curl -X POST "https://notes-api-l50o.onrender.com/notes/1/share" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"share_with_email": "friend@example.com"}'
```

### 5. Pin a Note
```bash
curl -X POST "https://notes-api-l50o.onrender.com/notes/1/pin" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_pinned": true}'
```

### 6. Search Notes
```bash
curl -X GET "https://notes-api-l50o.onrender.com/search?q=keyword" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 7. Get API Information
```bash
curl "https://notes-api-l50o.onrender.com/about"
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

### Live Deployment
This API is deployed on **Render.com** and accessible at:
- **Production URL**: https://notes-api-l50o.onrender.com
- **API Docs**: https://notes-api-l50o.onrender.com/docs
- **OpenAPI Spec**: https://notes-api-l50o.onrender.com/openapi.json

### Deploy Your Own Instance

#### Using Render.com:

1. Fork this repository
2. Sign up at https://render.com
3. Create a new Web Service
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
   - `ALGORITHM` - `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`
   - `DATABASE_URL` - `sqlite:///./notes.db` (or PostgreSQL URL)
7. Deploy!

#### Using Docker:

```bash
docker build -t notes-api .
docker run -p 8000:8000 -e SECRET_KEY=your-secret-key notes-api
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=sqlite:///./notes.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
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

## Testing

### Interactive Testing
Visit the live API documentation at https://notes-api-l50o.onrender.com/docs to test all endpoints interactively.

### Automated Testing
The API has been tested with all required endpoints:
- ✅ User registration (POST /register) - Returns 201 Created
- ✅ Duplicate registration - Returns 409 Conflict
- ✅ User login (POST /login) - Returns JWT token
- ✅ CRUD operations for notes
- ✅ Note sharing functionality
- ✅ Access control and permissions
- ✅ Search and pagination
- ✅ Pin/unpin notes

## API Response Codes

- `200 OK` - Successful GET/PUT/POST operations
- `201 Created` - Successful resource creation
- `204 No Content` - Successful DELETE operation
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Invalid/missing authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource (e.g., email already registered)
- `422 Unprocessable Entity` - Validation error

## Contributing

This project was created as part of an internship assignment. Feel free to fork and modify for your own use.

## Developer

**Varshith**
- Email: varshithg2004@gmail.com
- GitHub: https://github.com/VarshithGaddam

## License

MIT
