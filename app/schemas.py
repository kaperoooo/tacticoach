from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    team_name: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    team_name: str | None = None


class SchemeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    formation: str = Field(..., min_length=1, max_length=80)
    attack_direction: str | None = None
    orientation: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class SchemeCreate(SchemeBase):
    pass


class SchemeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    formation: str | None = Field(default=None, min_length=1, max_length=80)
    attack_direction: str | None = None
    orientation: str | None = None
    data: dict[str, Any] | None = None


class ScenarioBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    steps: list[dict[str, Any]] = Field(default_factory=list)


class ScenarioCreate(ScenarioBase):
    pass


class ScenarioUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    steps: list[dict[str, Any]] | None = None


class ProjectExport(BaseModel):
    project: ProjectCreate
    schemes: list[SchemeBase] = Field(default_factory=list)
    scenarios: list[ScenarioBase] = Field(default_factory=list)
