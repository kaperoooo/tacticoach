from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import create_db_and_tables, get_db
from app.models import Project, Scenario, Scheme
from app.schemas import (
    ProjectCreate,
    ProjectExport,
    ProjectUpdate,
    ScenarioCreate,
    ScenarioUpdate,
    SchemeCreate,
    SchemeUpdate,
)

app = FastAPI(title='TactiCoach', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

create_db_and_tables()
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')


@app.get('/')
def index() -> FileResponse:
    return FileResponse(Path(__file__).parent / 'static' / 'index.html')


@app.get('/api/health')
def health() -> dict[str, str]:
    return {'status': 'ok', 'app': 'TactiCoach'}


@app.get('/api/projects')
def list_projects(db: Session = Depends(get_db)) -> list[dict]:
    records = db.scalars(select(Project).order_by(Project.created_at.desc())).all()
    return [record.to_dict() for record in records]


@app.post('/api/projects', status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> dict:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project.to_dict()


@app.get('/api/projects/{project_id}')
def get_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    return project.to_dict()


@app.put('/api/projects/{project_id}')
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project.to_dict()


@app.delete('/api/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    db.delete(project)
    db.commit()


@app.get('/api/projects/{project_id}/schemes')
def list_schemes(project_id: int, db: Session = Depends(get_db)) -> list[dict]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    records = db.scalars(select(Scheme).where(Scheme.project_id == project_id).order_by(Scheme.created_at.desc())).all()
    return [record.to_dict() for record in records]


@app.post('/api/projects/{project_id}/schemes', status_code=status.HTTP_201_CREATED)
def create_scheme(project_id: int, payload: SchemeCreate, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    scheme = Scheme(project_id=project_id, **payload.model_dump())
    db.add(scheme)
    db.commit()
    db.refresh(scheme)
    return scheme.to_dict()


@app.get('/api/projects/{project_id}/schemes/{scheme_id}')
def get_scheme(project_id: int, scheme_id: int, db: Session = Depends(get_db)) -> dict:
    scheme = db.get(Scheme, scheme_id)
    if not scheme or scheme.project_id != project_id:
        raise HTTPException(status_code=404, detail='Scheme not found')
    return scheme.to_dict()


@app.put('/api/projects/{project_id}/schemes/{scheme_id}')
def update_scheme(project_id: int, scheme_id: int, payload: SchemeUpdate, db: Session = Depends(get_db)) -> dict:
    scheme = db.get(Scheme, scheme_id)
    if not scheme or scheme.project_id != project_id:
        raise HTTPException(status_code=404, detail='Scheme not found')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(scheme, field, value)
    db.commit()
    db.refresh(scheme)
    return scheme.to_dict()


@app.delete('/api/projects/{project_id}/schemes/{scheme_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_scheme(project_id: int, scheme_id: int, db: Session = Depends(get_db)) -> None:
    scheme = db.get(Scheme, scheme_id)
    if not scheme or scheme.project_id != project_id:
        raise HTTPException(status_code=404, detail='Scheme not found')
    db.delete(scheme)
    db.commit()


@app.get('/api/projects/{project_id}/scenarios')
def list_scenarios(project_id: int, db: Session = Depends(get_db)) -> list[dict]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    records = db.scalars(select(Scenario).where(Scenario.project_id == project_id).order_by(Scenario.created_at.desc())).all()
    return [record.to_dict() for record in records]


@app.post('/api/projects/{project_id}/scenarios', status_code=status.HTTP_201_CREATED)
def create_scenario(project_id: int, payload: ScenarioCreate, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    scenario = Scenario(project_id=project_id, **payload.model_dump())
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    return scenario.to_dict()


@app.get('/api/projects/{project_id}/scenarios/{scenario_id}')
def get_scenario(project_id: int, scenario_id: int, db: Session = Depends(get_db)) -> dict:
    scenario = db.get(Scenario, scenario_id)
    if not scenario or scenario.project_id != project_id:
        raise HTTPException(status_code=404, detail='Scenario not found')
    return scenario.to_dict()


@app.put('/api/projects/{project_id}/scenarios/{scenario_id}')
def update_scenario(project_id: int, scenario_id: int, payload: ScenarioUpdate, db: Session = Depends(get_db)) -> dict:
    scenario = db.get(Scenario, scenario_id)
    if not scenario or scenario.project_id != project_id:
        raise HTTPException(status_code=404, detail='Scenario not found')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(scenario, field, value)
    db.commit()
    db.refresh(scenario)
    return scenario.to_dict()


@app.delete('/api/projects/{project_id}/scenarios/{scenario_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_scenario(project_id: int, scenario_id: int, db: Session = Depends(get_db)) -> None:
    scenario = db.get(Scenario, scenario_id)
    if not scenario or scenario.project_id != project_id:
        raise HTTPException(status_code=404, detail='Scenario not found')
    db.delete(scenario)
    db.commit()


@app.get('/api/formations')
def list_formations() -> dict[str, list[str]]:
    return {
        'formations': ['4-3-3', '4-4-2', '4-2-3-1', '3-5-2', '3-4-3', '4-1-4-1']
    }


@app.get('/api/projects/{project_id}/export')
def export_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    schemes = db.scalars(select(Scheme).where(Scheme.project_id == project_id)).all()
    scenarios = db.scalars(select(Scenario).where(Scenario.project_id == project_id)).all()
    return {
        'project': project.to_dict(),
        'schemes': [scheme.to_dict() for scheme in schemes],
        'scenarios': [scenario.to_dict() for scenario in scenarios],
    }


@app.post('/api/projects/import')
def import_project(payload: ProjectExport, db: Session = Depends(get_db)) -> dict:
    project = Project(**payload.project.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)

    for scheme in payload.schemes:
        db.add(Scheme(project_id=project.id, **scheme.model_dump()))

    for scenario in payload.scenarios:
        db.add(Scenario(project_id=project.id, **scenario.model_dump()))

    db.commit()
    return project.to_dict()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
