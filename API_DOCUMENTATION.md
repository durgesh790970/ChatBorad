# ChatBoard API Documentation

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All API endpoints require session authentication. You must be logged in to access them.

The CSRF token is required for POST and PATCH requests.

## Endpoints

### 1. Get Users List

**Endpoint:**
```
GET /api/users/
```

**Description:** Get list of all users except the current logged-in user.

**Headers:**
```
Content-Type: application/json
Authorization: Session (logged in)
```

**Response:**
```json
[
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_online": true
    },
    {
        "id": 2,
        "username": "jane_smith",
        "email": "jane@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "is_online": false
    }
]
```

**Status Codes:**
- `200 OK` - List retrieved successfully
- `401 Unauthorized` - Not logged in
- `403 Forbidden` - No permission

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -b "sessionid=your-session-id"
```

**Example JavaScript:**
```javascript
fetch('/api/users/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'include'
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 2. Get Chat History

**Endpoint:**
```
GET /api/messages/history/?other_user_id=<user_id>
```

**Description:** Retrieve all messages between the current user and another user.

**Query Parameters:**
- `other_user_id` (required): The ID of the other user in the conversation

**Headers:**
```
Content-Type: application/json
Authorization: Session (logged in)
```

**Response:**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "sender": 1,
        "sender_username": "john_doe",
        "receiver": 2,
        "receiver_username": "jane_smith",
        "message_text": "Hello Jane!",
        "timestamp": "2024-01-15T10:30:00Z",
        "is_read": true
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "sender": 2,
        "sender_username": "jane_smith",
        "receiver": 1,
        "receiver_username": "john_doe",
        "message_text": "Hi John! How are you?",
        "timestamp": "2024-01-15T10:31:00Z",
        "is_read": true
    }
]
```

**Status Codes:**
- `200 OK` - Messages retrieved successfully
- `401 Unauthorized` - Not logged in
- `404 Not Found` - User not found

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/messages/history/?other_user_id=2" \
  -H "Content-Type: application/json" \
  -b "sessionid=your-session-id"
```

**Example JavaScript:**
```javascript
const otherUserId = 2;

fetch(`/api/messages/history/?other_user_id=${otherUserId}`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'include'
})
.then(response => response.json())
.then(messages => console.log(messages));
```

---

### 3. Send Message via API

**Endpoint:**
```
POST /api/messages/send/
```

**Description:** Send a message to another user. For real-time chat, WebSocket is preferred.

**Headers:**
```
Content-Type: application/json
X-CSRFToken: <csrf_token>
Authorization: Session (logged in)
```

**Request Body:**
```json
{
    "receiver_id": 2,
    "message_text": "Hello! How are you?"
}
```

**Response:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "sender": 1,
    "sender_username": "john_doe",
    "receiver": 2,
    "receiver_username": "jane_smith",
    "message_text": "Hello! How are you?",
    "timestamp": "2024-01-15T10:32:00Z",
    "is_read": false
}
```

**Status Codes:**
- `201 Created` - Message sent successfully
- `400 Bad Request` - Missing required fields or invalid data
- `401 Unauthorized` - Not logged in
- `404 Not Found` - Receiver not found

**Validation Errors:**
```json
{
    "error": "receiver_id and message_text are required."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/messages/send/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your-csrf-token" \
  -b "sessionid=your-session-id" \
  -d '{
    "receiver_id": 2,
    "message_text": "Hello!"
  }'
```

**Example JavaScript:**
```javascript
const getCsrfToken = () => {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const [key, value] = cookie.trim().split('=');
            if (key === name) cookieValue = decodeURIComponent(value);
        });
    }
    return cookieValue;
};

fetch('/api/messages/send/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
    },
    credentials: 'include',
    body: JSON.stringify({
        receiver_id: 2,
        message_text: 'Hello!'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 4. Update Online Status

**Endpoint:**
```
PATCH /api/status/
```

**Description:** Update the user's online/offline status.

**Headers:**
```
Content-Type: application/json
X-CSRFToken: <csrf_token>
Authorization: Session (logged in)
```

**Request Body:**
```json
{
    "is_online": true
}
```

**Response:**
```json
{
    "username": "john_doe",
    "is_online": true,
    "message": "Online status updated successfully."
}
```

**Status Codes:**
- `200 OK` - Status updated successfully
- `400 Bad Request` - Missing `is_online` field
- `401 Unauthorized` - Not logged in
- `500 Internal Server Error` - Server error

**Example cURL:**
```bash
curl -X PATCH http://localhost:8000/api/status/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your-csrf-token" \
  -b "sessionid=your-session-id" \
  -d '{
    "is_online": true
  }'
```

**Example JavaScript:**
```javascript
fetch('/api/status/', {
    method: 'PATCH',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
    },
    credentials: 'include',
    body: JSON.stringify({
        is_online: true
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## WebSocket Endpoint

For real-time messaging, use WebSocket instead of REST API.

**WebSocket URL:**
```
ws://localhost:8000/ws/chat/<user_id>/
wss://yourdomain.com/ws/chat/<user_id>/  (for HTTPS)
```

### WebSocket Message Format

**Client sends (JavaScript):**
```javascript
socket.send(JSON.stringify({
    message: "Hello!"
}));
```

**Server responds:**
```json
{
    "type": "chat_message",
    "message_id": "550e8400-e29b-41d4-a716-446655440003",
    "sender_id": 1,
    "sender_username": "john_doe",
    "receiver_id": 2,
    "receiver_username": "jane_smith",
    "message": "Hello!",
    "timestamp": "2024-01-15T10:33:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Description of what went wrong"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "error": "User not found."
}
```

### 500 Internal Server Error
```json
{
    "error": "An error occurred"
}
```

---

## Rate Limiting

Currently not implemented, but can be added using:
```python
# Install django-ratelimit
pip install django-ratelimit
```

## Testing API with Postman

1. **Import Collection**: Use the URLs above
2. **Set up Environment Variables**:
   - `base_url`: http://localhost:8000
3. **Authenticate**: 
   - Get CSRF token from login page
   - Use cookies for session authentication
4. **Test Endpoints**: Use the examples provided

---

## API Versioning

Currently using URL-based versioning:
```
/api/v1/users/
/api/v1/messages/
```

Can be implemented in the future for backward compatibility.

---

## CORS Policy

CORS is enabled for local development. Configure in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
]
```

---

## Best Practices

1. **Always use HTTPS** in production
2. **Keep CSRF token fresh** for security
3. **Validate input** on both client and server
4. **Use WebSocket** for real-time features
5. **Implement rate limiting** for production
6. **Log API usage** for debugging
7. **Use meaningful status codes**
8. **Document API changes** in this file

---

## Troubleshooting

### 401 Unauthorized
- Make sure you're logged in
- Session cookie might have expired
- Clear browser cookies and login again

### 403 Forbidden
- Check CSRF token is correct
- Ensure proper authentication

### CORS Error
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `settings.py`
- Only for development, not needed for same-origin requests

### WebSocket Connection Failed
- Check if Daphne/Channels is running
- Verify WebSocket URL is correct
- Check browser console for detailed errors

---

## Support

For more information:
- See README.md
- Check Django REST Framework docs: https://www.django-rest-framework.org/
- Check Django Channels docs: https://channels.readthedocs.io/
