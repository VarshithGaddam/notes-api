# Complete API Testing Guide

## Prerequisites
Server running at: `http://127.0.0.1:8000`

---

## Test 1: POST /register ✅
**Method:** POST  
**URL:** `http://127.0.0.1:8000/register`  
**Body (JSON):**
```json
{
  "email": "user1@example.com",
  "password": "password123"
}
```
**Expected Response:** 201 Created
```json
{
  "message": "User created successfully",
  "email": "user1@example.com"
}
```

---

## Test 2: POST /login ✅
**Method:** POST  
**URL:** `http://127.0.0.1:8000/login`  
**Body (JSON):**
```json
{
  "email": "user1@example.com",
  "password": "password123"
}
```
**Expected Response:** 200 OK
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```
**Action:** Copy the `access_token` - you'll need it for all subsequent requests!

---

## Test 3: POST /notes (Create Note) ✅
**Method:** POST  
**URL:** `http://127.0.0.1:8000/notes`  
**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Body (JSON):**
```json
{
  "title": "Test Note 1",
  "content": "This is my first test note"
}
```
**Expected Response:** 201 Created
```json
{
  "id": 1,
  "title": "Test Note 1",
  "content": "This is my first test note",
  "created_at": "2025-05-15T...",
  "updated_at": "2025-05-15T...",
  "is_pinned": false
}
```

---

## Test 4: GET /notes/{id} (Get Specific Note) ✅
**Method:** GET  
**URL:** `http://127.0.0.1:8000/notes/1`  
**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:** 200 OK
```json
{
  "id": 1,
  "title": "Test Note 1",
  "content": "This is my first test note",
  "created_at": "2025-05-15T...",
  "updated_at": "2025-05-15T...",
  "is_pinned": false
}
```

---

## Test 5: GET /notes (Get All Notes) ✅
**Method:** GET  
**URL:** `http://127.0.0.1:8000/notes`  
**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:** 200 OK
```json
[
  {
    "id": 1,
    "title": "Test Note 1",
    "content": "This is my first test note",
    "created_at": "2025-05-15T...",
    "updated_at": "2025-05-15T...",
    "is_pinned": false
  }
]
```

---

## Test 6: PUT /notes/{id} (Update Note) ✅
**Method:** PUT  
**URL:** `http://127.0.0.1:8000/notes/1`  
**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Body (JSON):**
```json
{
  "title": "Updated Note Title",
  "content": "Updated note content"
}
```
**Expected Response:** 200 OK
```json
{
  "id": 1,
  "title": "Updated Note Title",
  "content": "Updated note content",
  "created_at": "2025-05-15T...",
  "updated_at": "2025-05-15T...",
  "is_pinned": false
}
```

---

## Test 7: DELETE /notes/{id} ✅
**Method:** DELETE  
**URL:** `http://127.0.0.1:8000/notes/1`  
**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:** 204 No Content  
(Empty response body)

**Note:** Create a new note before testing share functionality!

---

## Test 8: POST /notes/{id}/share (Share Note) ✅

### Step 1: Create second user
**Method:** POST  
**URL:** `http://127.0.0.1:8000/register`  
**Body (JSON):**
```json
{
  "email": "user2@example.com",
  "password": "password123"
}
```

### Step 2: Create a note with user1
**Method:** POST  
**URL:** `http://127.0.0.1:8000/notes`  
**Headers:**
- `Authorization: Bearer USER1_TOKEN`

**Body (JSON):**
```json
{
  "title": "Shared Note",
  "content": "This note will be shared"
}
```
**Note the note ID from response (e.g., id: 2)**

### Step 3: Share the note
**Method:** POST  
**URL:** `http://127.0.0.1:8000/notes/2/share`  
**Headers:**
- `Authorization: Bearer USER1_TOKEN`

**Body (JSON):**
```json
{
  "share_with_email": "user2@example.com"
}
```
**Expected Response:** 200 OK
```json
{
  "message": "Note shared successfully with user2@example.com"
}
```

---

## Test 9: Second User Accessing Shared Note ✅

### Step 1: Login as user2
**Method:** POST  
**URL:** `http://127.0.0.1:8000/login`  
**Body (JSON):**
```json
{
  "email": "user2@example.com",
  "password": "password123"
}
```
**Copy user2's access_token**

### Step 2: Get the shared note
**Method:** GET  
**URL:** `http://127.0.0.1:8000/notes/2`  
**Headers:**
- `Authorization: Bearer USER2_TOKEN`

**Expected Response:** 200 OK
```json
{
  "id": 2,
  "title": "Shared Note",
  "content": "This note will be shared",
  "created_at": "2025-05-15T...",
  "updated_at": "2025-05-15T...",
  "is_pinned": false
}
```

### Step 3: Verify user2 sees it in their notes list
**Method:** GET  
**URL:** `http://127.0.0.1:8000/notes`  
**Headers:**
- `Authorization: Bearer USER2_TOKEN`

**Expected:** Should see the shared note in the list!

---

## Test 10: GET /about ✅
**Method:** GET  
**URL:** `http://127.0.0.1:8000/about`  
**No authentication required**

**Expected Response:** 200 OK
```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "my_features": {
    "Pin Notes": "Users can pin important notes...",
    "Full-text Search": "Implemented search functionality...",
    ...
  }
}
```

---

## Test 11: GET /openapi.json ✅
**Method:** GET  
**URL:** `http://127.0.0.1:8000/openapi.json`  
**No authentication required**

**Expected Response:** 200 OK  
Returns complete OpenAPI specification JSON

---

## Bonus Tests

### Test 12: GET /search (Full-text Search)
**Method:** GET  
**URL:** `http://127.0.0.1:8000/search?q=shared`  
**Headers:**
- `Authorization: Bearer YOUR_TOKEN`

**Expected:** Returns notes matching "shared" in title or content

### Test 13: POST /notes/{id}/pin (Pin Note)
**Method:** POST  
**URL:** `http://127.0.0.1:8000/notes/2/pin`  
**Headers:**
- `Authorization: Bearer USER1_TOKEN`

**Body (JSON):**
```json
{
  "is_pinned": true
}
```
**Expected Response:** 200 OK
```json
{
  "message": "Note pinned successfully"
}
```

---

## Summary Checklist

- ✅ POST /register - User registration
- ✅ POST /login - User authentication
- ✅ POST /notes - Create note
- ✅ GET /notes - Get all notes
- ✅ GET /notes/{id} - Get specific note
- ✅ PUT /notes/{id} - Update note
- ✅ DELETE /notes/{id} - Delete note
- ✅ POST /notes/{id}/share - Share note
- ✅ Second user can access shared note
- ✅ GET /about - API information
- ✅ GET /openapi.json - API documentation
- ✅ GET /search - Full-text search (Bonus)
- ✅ POST /notes/{id}/pin - Pin notes (Bonus)

All endpoints are working! 🎉
