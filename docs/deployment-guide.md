# SchoMatch-AI Deployment Guide

This guide covers deploying SchoMatch-AI in production using Docker Compose and optionally Google Cloud Run.

## Prerequisites

- **Docker** ≥ 24.0 and **Docker Compose** ≥ 2.20
- A **Google AI Studio API key** → [Get one here](https://aistudio.google.com/app/apikey)
- (Optional) A **Google Cloud** project for Cloud Run deployment

---

## 1. Docker Compose Deployment (Recommended)

### Step 1 — Clone and Configure

```bash
git clone https://github.com/your-org/SchoMatch-AI.git
cd SchoMatch-AI
cp .env.example .env
```

Edit `.env` and set the required values:

```dotenv
# Required — your Google AI Studio API key
GOOGLE_API_KEY=your_actual_key_here

# Database password (change for production)
DB_PASSWORD=a_strong_random_password

# Security key (change for production)
SECRET_KEY=a_strong_random_secret
```

### Step 2 — Build and Start

```bash
docker-compose up --build -d
```

This starts three services:

| Service    | Port  | Description                       |
|------------|-------|-----------------------------------|
| `backend`  | 8000  | FastAPI backend with ADK agents   |
| `frontend` | 5173  | React + Vite frontend             |
| `postgres` | 5432  | PostgreSQL 16 database            |

The backend automatically waits for PostgreSQL to be healthy before starting.

### Step 3 — Verify

```bash
# Check all services are running
docker-compose ps

# Test the health endpoint
curl http://localhost:8000/api/health

# Seed the database with sample opportunities
docker-compose exec backend python -m app.db.seed
```

Access the UI at **http://localhost:5173**

### Step 4 — View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend
```

---

## 2. Environment Variables Reference

| Variable              | Required | Default                    | Description                          |
|-----------------------|----------|----------------------------|--------------------------------------|
| `GOOGLE_API_KEY`      | ✅       | —                          | Google AI Studio API key             |
| `DATABASE_URL`        | No       | `sqlite+aiosqlite:///...`  | Database connection string           |
| `DB_PASSWORD`         | No       | `schomatch_secret`         | PostgreSQL password                  |
| `PRIMARY_MODEL`       | No       | `gemini-2.0-flash`         | Primary Gemini model                 |
| `REASONING_MODEL`     | No       | `gemini-2.5-flash`         | Reasoning-capable model              |
| `ALLOWED_ORIGINS`     | No       | `http://localhost:5173,...` | CORS allowed origins (comma-sep)     |
| `RATE_LIMIT_REQUESTS` | No       | `10`                       | Max requests per window              |
| `RATE_LIMIT_WINDOW`   | No       | `60`                       | Rate limit window in seconds         |
| `SECRET_KEY`          | No       | `dev-secret-...`           | Application secret key               |

> ⚠️ **Production**: Always set `GOOGLE_API_KEY`, `DB_PASSWORD`, and `SECRET_KEY` to strong, unique values.

---

## 3. Database Setup

### Automatic Table Creation

Tables are created automatically on startup via SQLAlchemy's `create_all()`. No manual migration is needed for initial deployment.

### Seeding Sample Data

```bash
# Via Docker
docker-compose exec backend python -m app.db.seed

# Local development
cd backend && python -m app.db.seed
```

This inserts 15 sample scholarships, internships, fellowships, and research opportunities for demonstration purposes.

### PostgreSQL Direct Access

```bash
docker-compose exec postgres psql -U schomatch -d schomatch
```

---

## 4. Google Cloud Run Deployment (Optional)

### Step 1 — Install gcloud CLI

Follow the [official guide](https://cloud.google.com/sdk/docs/install).

### Step 2 — Build and Push Backend Image

```bash
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/schomatch-backend
```

### Step 3 — Deploy to Cloud Run

```bash
gcloud run deploy schomatch-backend \
  --image gcr.io/YOUR_PROJECT_ID/schomatch-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=your_key,DATABASE_URL=your_cloud_sql_url" \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 5
```

### Step 4 — Set Up Cloud SQL

For production, use [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres) with a private IP or Cloud SQL Auth Proxy.

---

## 5. Health Checks and Monitoring

### Health Endpoint

```
GET /api/health
```

Returns `200 OK` with service status. Use this for load balancer health checks and uptime monitoring.

### API Documentation

- **Swagger UI**: `http://your-host:8000/docs`
- **ReDoc**: `http://your-host:8000/redoc`

### Recommended Monitoring

- Set up alerts on the `/api/health` endpoint (e.g., via UptimeRobot, Google Cloud Monitoring)
- Monitor PostgreSQL connection pool usage
- Track rate limit 429 responses to detect abuse

---

## 6. Stopping and Cleanup

```bash
# Stop services (preserves data)
docker-compose down

# Stop and delete all data (including database volume)
docker-compose down -v
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend can't connect to PostgreSQL | Ensure `DATABASE_URL` uses `postgres` as hostname (Docker service name), not `localhost` |
| `GOOGLE_API_KEY` errors | Verify the key at [AI Studio](https://aistudio.google.com/app/apikey) |
| Rate limit errors (429) | Default is 10 requests/minute per IP. Adjust `RATE_LIMIT_REQUESTS` in `.env` |
| Frontend shows blank page | Check CORS — ensure `ALLOWED_ORIGINS` includes the frontend URL |
