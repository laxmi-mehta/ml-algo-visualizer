from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Literal


WidgetType = Literal["slider", "number", "select", "checkbox"]


@dataclass(frozen=True)
class ParameterSpec:
    key: str
    label: str
    widget: WidgetType
    default: Any
    help_text: str
    min_value: Any | None = None
    max_value: Any | None = None
    step: Any | None = None
    options: list[Any] | None = None
    format: str | None = None


@dataclass(frozen=True)
class AlgorithmConfig:
    slug: str
    name: str
    category: str
    problem_type: str
    overview: str
    when_to_use: list[str]
    parameter_specs: list[ParameterSpec] = field(default_factory=list)
    render_page: Callable[["AlgorithmConfig"], None] | None = None
    status: str = "ready"
    short_badge: str = ""
    featured: bool = False
    maturity: str = "Core"
