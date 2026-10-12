# TactiCoach

TactiCoach is a lightweight tactical football platform for coaches, analysts and technical staff to build formations, manage player positions, create scenarios, and persist tactical work in SQLite.

## Features
- Interactive football pitch with SVG rendering
- Team and player management
- Formation presets: 4-3-3, 4-4-2, 4-2-3-1, 3-5-2, 3-4-3, 4-1-4-1
- Project, scheme and scenario creation
- JSON import/export
- PNG export of the pitch
- FastAPI backend + SQLite persistence
- pytest coverage for core API workflows

## Tech stack
- Backend: FastAPI, SQLAlchemy, Pydantic
- Database: SQLite
- Frontend: HTML, CSS, JavaScript, SVG
- Tests: pytest

## Local setup

1. Create a virtual environment
   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies
   pip install -U pip
   pip install -r requirements.txt

3. Run the app
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. Open in browser
   http://localhost:8000

5. API docs
   http://localhost:8000/docs

## Docker

docker compose up --build

## Project structure
- app/
  - config.py
  - database.py
  - main.py
  - models.py
  - schemas.py
  - static/
    - index.html
    - styles.css
    - app.js
- tests/

## API overview
- GET /api/health
- GET /api/projects
- POST /api/projects
- GET /api/projects/{project_id}
- PUT /api/projects/{project_id}
- DELETE /api/projects/{project_id}
- GET /api/projects/{project_id}/schemes
- POST /api/projects/{project_id}/schemes
- GET /api/projects/{project_id}/schemes/{scheme_id}
- PUT /api/projects/{project_id}/schemes/{scheme_id}
- DELETE /api/projects/{project_id}/schemes/{scheme_id}
- GET /api/projects/{project_id}/scenarios
- POST /api/projects/{project_id}/scenarios
- GET /api/projects/{project_id}/scenarios/{scenario_id}
- PUT /api/projects/{project_id}/scenarios/{scenario_id}
- DELETE /api/projects/{project_id}/scenarios/{scenario_id}
- GET /api/formations

## Notes
This project is configured for local development and education. It stores data in SQLite in the project directory.
