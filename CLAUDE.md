# Retrieval Service

Service responsible for:
- vector db search
- web search 

# Technology Stack
- Python 3.12+
- FastAPI
- Pydantic v2
- aiohttp
- qdrant-client
- LangChain


# Directory Structure
- `src/`: sources root 
- `src/api/v1/endpoints`: fastapi routers for endpoints
- `src/services`: scripts service layer
- `src/repositories`: scripts repository layer
- `src/depends.py`: depends
- `src/config.py`: pydantic settings

# Patterns
- DI (Dependency Injection)
- Service layers
- Repository layers

# Testing
- `tests`: base folder
- use Pytest

# Environment Variables
- `.env`

# Virtual environment
- use `uv`

# Running Locally
- `python src/main.py`

# API Endpoints
- `endpoints/search.py`
- `endpoints/websearch.py`
- `endpoints/health.py`
