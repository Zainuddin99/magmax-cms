# API Testing Guide

This guide will help you test the MagMax API endpoints.

## Prerequisites

1. Backend server running: `python manage.py runserver`
2. At least one superuser created: `python manage.py createsuperuser`
3. Some test articles created via admin interface

---

## Quick Test Commands

### 1. Test Health / List Articles

```bash
curl http://localhost:8000/api/v1/articles/
```

**Expected**: JSON response with paginated article list

---

### 2. Get JWT Token

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your-password"
  }'
```

**Expected Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Save the access token for next requests!**

---

### 3. Create a Category

```bash
curl -X POST http://localhost:8000/api/v1/categories/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technology",
    "description": "All about tech"
  }'
```

---

### 4. Create an Article

```bash
curl -X POST http://localhost:8000/api/v1/articles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First API Article",
    "excerpt": "This article was created via API",
    "content": "Full content here. This is a test article created using the REST API.",
    "status": "published",
    "published_date": "2024-12-24T10:00:00Z",
    "meta_title": "My First API Article - SEO",
    "meta_description": "Learn how to create articles via API",
    "meta_keywords": "api, django, rest"
  }'
```

---

### 5. Get Article by Slug

```bash
curl http://localhost:8000/api/v1/articles/my-first-api-article/
```

**Note**: The slug is auto-generated from the title

---

### 6. Update an Article

```bash
curl -X PATCH http://localhost:8000/api/v1/articles/my-first-api-article/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Updated Article Title",
    "excerpt": "Updated excerpt"
  }'
```

---

### 7. Get Published Articles Only

```bash
curl http://localhost:8000/api/v1/articles/published/
```

---

### 8. Get Featured Articles (Most Viewed)

```bash
curl http://localhost:8000/api/v1/articles/featured/
```

---

### 9. Search Articles

```bash
# Search by keyword
curl "http://localhost:8000/api/v1/articles/?search=django"

# Filter by status
curl "http://localhost:8000/api/v1/articles/?status=published"

# Order by views
curl "http://localhost:8000/api/v1/articles/?ordering=-view_count"

# Combine filters
curl "http://localhost:8000/api/v1/articles/?status=published&ordering=-published_date&search=api"
```

---

### 10. Get My Articles (Authenticated User's Articles)

```bash
curl http://localhost:8000/api/v1/articles/my_articles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 11. Get Categories

```bash
curl http://localhost:8000/api/v1/categories/
```

---

### 12. Get Articles in Specific Category

```bash
curl http://localhost:8000/api/v1/categories/technology/articles/
```

---

### 13. Delete an Article

```bash
curl -X DELETE http://localhost:8000/api/v1/articles/my-first-api-article/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Get token
response = requests.post(f"{BASE_URL}/api/token/", json={
    "username": "admin",
    "password": "your-password"
})
token = response.json()["access"]

# Create article
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

article_data = {
    "title": "Python API Test",
    "content": "Created with Python requests library",
    "status": "published"
}

response = requests.post(
    f"{BASE_URL}/api/v1/articles/",
    json=article_data,
    headers=headers
)

print(response.json())

# Get articles
response = requests.get(f"{BASE_URL}/api/v1/articles/published/")
print(response.json())
```

---

## Testing with JavaScript (Node.js)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function testAPI() {
  // Get token
  const tokenResponse = await axios.post(`${BASE_URL}/api/token/`, {
    username: 'admin',
    password: 'your-password'
  });
  
  const token = tokenResponse.data.access;
  
  // Create article
  const articleData = {
    title: 'JavaScript API Test',
    content: 'Created with Axios',
    status: 'published'
  };
  
  const config = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  };
  
  const articleResponse = await axios.post(
    `${BASE_URL}/api/v1/articles/`,
    articleData,
    config
  );
  
  console.log(articleResponse.data);
  
  // Get articles
  const articlesResponse = await axios.get(`${BASE_URL}/api/v1/articles/`);
  console.log(articlesResponse.data);
}

testAPI();
```

---

## Common Response Codes

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: No permission
- `404 Not Found`: Resource doesn't exist
- `500 Server Error`: Backend error

---

## Pagination

All list endpoints support pagination:

```bash
# Get page 2
curl "http://localhost:8000/api/v1/articles/?page=2"

# Change page size (default: 10)
curl "http://localhost:8000/api/v1/articles/?page_size=20"
```

**Response includes**:
- `count`: Total items
- `next`: Next page URL
- `previous`: Previous page URL
- `results`: Array of items

---

## Tips

1. **Save your access token**: It expires after 60 minutes (configurable in settings)
2. **Use refresh token**: To get a new access token without logging in again
3. **Test in browser**: Visit http://localhost:8000/api/v1/ for browsable API
4. **Use Postman**: Import the endpoints for easier testing
5. **Check logs**: Run server with verbose output to see requests

---

## Troubleshooting

### 401 Unauthorized
- Token expired: Get a new one
- Token missing: Include `Authorization: Bearer <token>` header
- Invalid token: Re-login

### 403 Forbidden
- You don't have permission to perform this action
- Only article authors can edit/delete their articles (or staff users)

### 404 Not Found
- Check the slug/ID is correct
- Article might be draft (not published)

### 400 Bad Request
- Check request data format
- Required fields might be missing
- Slug might already exist

---

Happy Testing! 🚀



