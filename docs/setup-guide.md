# SchoMatch-AI Setup Guide

This guide covers setting up SchoMatch-AI for local development and testing.

## Prerequisites

- Python 3.12+
- Node.js 20+
- A Google AI Studio API Key

## Setup Steps

### 1. Environment Configuration

Copy the example environment file and add your API key:

```bash
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY
```

### 2. Backend Setup

Open a terminal and set up the Python backend:

```bash
cd backend
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database with sample opportunities
python -m app.db.seed

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

Open a second terminal and set up the React frontend:

```bash
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

### 4. MCP Servers (Optional)

The MCP servers are defined in `backend/app/mcp_servers/`. The agent runner currently uses mocked functions for speed/reliability in the demo, but you can run the standalone MCP servers to test the protocol:

```bash
cd backend
# With virtual environment activated
python -m app.mcp_servers.search_server
```

## Troubleshooting

- **CORS Errors**: Ensure `ALLOWED_ORIGINS` in `.env` matches your frontend URL exactly.
- **Rate Limit Errors**: The API defaults to 10 requests per minute. Adjust `RATE_LIMIT_REQUESTS` in `.env` if needed.
- **Database Errors**: If the SQLite database gets corrupted, delete `backend/schomatch.db` and run the seed script again.
