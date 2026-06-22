# Kaggle Writeup: SchoMatch-AI

## Introduction
Finding the right academic opportunities—scholarships, research grants, and exchange programs—is an exhausting, high-friction process for students. Information is siloed, requirements are complex, and determining true eligibility requires deep reading. 

SchoMatch-AI is an intelligent platform that completely automates this discovery process. Built using the Google Agent Development Kit (ADK) and Gemini models, it transforms a simple student profile into a curated, scored, and actionable roadmap of academic opportunities.

## Innovation
Most existing platforms are simple keyword search engines. SchoMatch-AI innovates by treating opportunity matching as a **multi-step reasoning problem**. 

Instead of a single LLM call, we use a specialized team of agents. The Eligibility Agent, powered by Gemini 2.5 Pro, performs complex logical deduction (e.g., "The student is in their 6th semester, so they have completed 3 years, making them eligible for the CERN program"). The Career Advisor Agent then synthesizes the results to generate a personalized action plan, converting a simple search result into active career mentorship.

## Architecture & Solution Design
SchoMatch-AI is built on a modern, robust architecture:

- **Frontend**: React + Vite with a custom premium UI.
- **Backend**: FastAPI providing async endpoints, SSE streaming for agent status, and strict rate limiting for security.
- **ADK Orchestration**: We utilize the `SequentialAgent` pattern. The orchestrator triggers five sub-agents in a deterministic pipeline, passing state via the `output_key` shared context.
- **MCP Servers**: The system architecture includes four Model Context Protocol (MCP) servers—Search, Knowledge, File (for CV parsing), and External APIs—allowing the agents to interact with live data safely.

## Effective Application of Course Concepts
This project demonstrates several advanced concepts from the Intensive Vibe Coding course:
1. **Multi-Agent Systems**: Clear separation of concerns (Profile, Discovery, Eligibility, Career, Deadlines).
2. **Tool Calling**: Agents are equipped with specific Python tools to execute their tasks.
3. **Model Selection**: We route simple extraction tasks to Gemini 2.0 Flash for speed, while routing the complex matching logic to Gemini 2.5 Pro for deep reasoning.
4. **Security & Deployment**: The app implements environment variables, CORS, rate limiting, and is fully dockerized for immediate deployment.

## Conclusion
SchoMatch-AI delivers real user value by democratizing access to global education opportunities. By combining the Google ADK's orchestration capabilities with a premium, accessible UI, it provides a portfolio-quality example of how AI agents can solve complex, real-world discovery problems.
