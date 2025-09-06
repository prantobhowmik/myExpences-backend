# MyExpences Backend

This is the backend for the MyExpences app, built with FastAPI and MongoDB Atlas. It provides RESTful APIs for expense management and uses JWT authentication for user login and signup. No server-side session is used; all authentication is stateless and secure with JWT.

## Features
- User signup and login with JWT authentication
- Protected expense and summary routes
- MongoDB for data storage
- Dockerized for easy development


## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.13 (for local development)
- MongoDB Atlas account (for production)

### Setup & Run (Development)
1. **Clone the repository:**
   ```bash
   git clone https://github.com/prantobhowmik/myExpences-backend.git
   cd myExpences-backend
   ```
2. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   - Backend runs on `http://localhost:8000`
   - By default, uses local MongoDB. For Atlas, set `MONGODB_URL` in `docker-compose.yml` or `.env`.

3. **Environment Variables:**
   - Set `MONGODB_URL` to your MongoDB Atlas connection string for production.

---

## Deploying to Render

1. **Create a new Web Service on Render**
2. **Connect your GitHub repo**
3. **Set environment variable:**
   - `MONGODB_URL` = your MongoDB Atlas connection string
4. **Dockerfile is ready for production (uses gunicorn/uvicorn)**
5. **Expose port 8000**

---


### API Endpoints

#### Auth
- `POST /signup` — Register a new user
   - Body: `{ "full_name": "your name", "username": "yourname", "email": "your@email.com", "mobile": "1234567890", "date_of_birth": "YYYY-MM-DD", "password": "yourpassword" }`
- `POST /login` — Login and get JWT token
   - Body: `{ "identifier": "yourname or email or mobile", "password": "yourpassword" }`
   - Response: `{ "access_token": "...", "token_type": "bearer" }`

#### Expenses (All require JWT in `Authorization: Bearer <token>` header)
- `POST /expenses` — Add a new expense
- `GET /expenses` — List expenses (optionally filter by month/year)
- `GET /expenses/{expense_id}` — Get a specific expense
- `PUT /expenses/{expense_id}` — Edit an expense
- `DELETE /expenses/{expense_id}` — Delete an expense
- `GET /summary/latest` — Get summary for current month
- `GET /summary/{year}/{month}` — Get summary for any month


### Frontend Integration
- After login, store the JWT token in localStorage or memory.
- Send the token in the `Authorization` header for all protected requests:
   ```js
   fetch('http://localhost:8000/expenses', {
      headers: { 'Authorization': 'Bearer <token>' }
   })
   ```
- If the backend returns 401 Unauthorized, redirect the user to the login page. JWT expiration is handled by the backend.
- No Google OAuth or social login is required.


### Development Notes
- All user and expense data is stored in MongoDB Atlas. No in-memory or fake DB is used.
- All code changes are auto-reloaded in Docker during development.

### Contributing
Pull requests and issues are welcome!

### License
MIT
```
