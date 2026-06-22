# SchoMatch-AI 🎓✨

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Vite + React](https://img.shields.io/badge/Vite%20+%20React-Premium%20UI-646CFF?logo=vite)](https://vitejs.dev/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-EA4335?logo=google)](https://google.github.io/adk-docs/)
[![MCP](https://img.shields.io/badge/MCP-Servers-black?logo=model-context-protocol)](https://modelcontextprotocol.io/)

A production-ready, portfolio-quality AI platform that helps students discover personalized scholarships, internships, research opportunities, fellowships, exchange programs, and summer schools worldwide.

## 🌟 The Core Problem

Students struggle to find opportunities matching their academic profile because information is scattered across thousands of websites, eligibility requirements are complex, and manual searching is time-consuming. SchoMatch-AI automates this discovery process using specialized AI agents.

## 🏗️ Architecture Overview

SchoMatch-AI leverages a robust, modern tech stack:

- **Agent Engine**: Google Agent Development Kit (ADK) using `SequentialAgent` for pipeline orchestration.
- **AI Models**: Google Gemini 2.0 Flash (fast generation) and Gemini 2.5 Pro (complex matching/reasoning).
- **Backend**: FastAPI with async SQLAlchemy and SlowAPI rate limiting.
- **Frontend**: React + Vite with a custom, premium glassmorphism dark theme UI.
- **Tools**: Model Context Protocol (MCP) servers for Search, Knowledge, File Processing, and External APIs.
- **Deployment**: Fully dockerized via `docker-compose`.

## 🤖 The Multi-Agent Pipeline

When a student submits their profile, SchoMatch-AI triggers a `SequentialAgent` pipeline with 5 specialized sub-agents:

1. **Profile Analysis Agent**: Extracts eligibility attributes and builds a structured candidate profile.
2. **Opportunity Discovery Agent**: Queries the Search MCP to find potential matches.
3. **Eligibility Matching Agent**: Compares requirements using the Knowledge MCP and ranks opportunities.
4. **Career Advisor Agent**: Explains recommendations and suggests profile improvements.
5. **Deadline Tracker Agent**: Organizes application deadlines into a timeline.

## 🚀 Quickstart

SchoMatch-AI is designed for easy evaluation.

### Prerequisites
- Docker and Docker Compose
- A Google AI Studio API Key (`GOOGLE_API_KEY`)

### Running with Docker

1. Clone the repository
2. Copy `.env.example` to `.env` and add your `GOOGLE_API_KEY`
3. Run: `docker-compose up -d`
4. Access the UI at `http://localhost:5173`

For detailed setup instructions without Docker, see [docs/setup-guide.md](docs/setup-guide.md).

## 📊 Features

- **Multi-Step Profile Building**: Input your university, GPA, skills, and preferred countries.
- **Live Agent Pipeline**: Watch the AI agents work in real-time as they process your profile.
- **Match Scoring**: Get percentage-based match scores highlighting exactly why an opportunity is a good fit.
- **Personalized Action Plans**: Receive step-by-step guidance on how to improve your application.
- **Eligibility Gap Analysis**: Clearly see any missing requirements (e.g., GPA or language thresholds).

## 🔒 Security

- Rate limiting to prevent API abuse
- Input validation via strict Pydantic schemas
- Environment variable-based secret management
- Parameterized database queries to prevent SQL injection
- Stateless agent sessions for privacy

## 📚 Documentation

- [Setup Guide](docs/setup-guide.md)
- [Deployment Guide](docs/deployment-guide.md)
- [5-Minute Demo Plan](docs/demo-plan.md)
- [Kaggle Writeup](docs/kaggle-writeup.md)
