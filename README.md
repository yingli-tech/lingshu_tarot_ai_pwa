# Lingshu Tarot AI (Prototype)

Lingshu is an AI-powered tarot interpretation system that blends symbolic reasoning with modern language models. It generates context-aware readings based on user questions and tarot card inputs.

> This repository contains the **initial prototype** built with a monolithic architecture using Streamlit.
> A redesigned production-oriented version (decoupled architecture) is under development and will be released in a separate repository.

## Live Demo

https://aethercode-ai-tarot.onrender.com/

> Note: The demo may experience cold-start delays due to free-tier hosting.

## Prototype Features

- Interactive tarot reading interface built with Streamlit
- Supports single-card and three-card spreads
- AI-generated interpretations using LLMs
- Manual or random card input
- Stateful conversational follow-up

## Tech Stack (Prototype)

- Frontend + Backend: Streamlit (monolithic)
- Language: Python
- AI: OpenAI API

## Next Version (In Progress)

The system has been redesigned with a scalable, production-oriented architecture:

- Decoupled frontend and backend
- RESTful API design for tarot reading services
- Serverless backend using AWS Lambda
- Cloud storage (S3) for tarot assets
- Database integration for persistent user readings

This version improves scalability, maintainability, and deployment efficiency.

> A new repository will be published for this version.

## Motivation

This project explores how structured symbolic systems (tarot) can be combined with LLMs to produce meaningful, context-aware interpretations, while balancing determinism (card structure) and generative reasoning.

This project was also motivated by observing real user demand for tarot and reflective tools in everyday contexts.