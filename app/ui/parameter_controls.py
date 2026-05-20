from __future__ import annotations

from typing import Any

import streamlit as st

from app.core.models import ParameterSpec


def render_parameter_controls(parameter_specs: list[ParameterSpec], namespace: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for spec in parameter_specs:
        widget_key = f"{namespace}_{spec.key}"
        if spec.widget == "slider":
            values[spec.key] = st.slider(
                spec.label,
                min_value=spec.min_value,
                max_value=spec.max_value,
                value=spec.default,
                step=spec.step,
                help=spec.help_text,
                key=widget_key,
            )
        elif spec.widget == "number":
            number_input_kwargs = {
                "label": spec.label,
                "min_value": spec.min_value,
                "max_value": spec.max_value,
                "value": spec.default,
                "step": spec.step,
                "help": spec.help_text,
                "key": widget_key,
            }
            if spec.format is not None:
                number_input_kwargs["format"] = spec.format
            values[spec.key] = st.number_input(**number_input_kwargs)
        elif spec.widget == "select":
            values[spec.key] = st.selectbox(
                spec.label,
                options=spec.options or [],
                index=(spec.options or []).index(spec.default) if spec.options else 0,
                help=spec.help_text,
                key=widget_key,
            )
        elif spec.widget == "checkbox":
            values[spec.key] = st.checkbox(
                spec.label,
                value=bool(spec.default),
                help=spec.help_text,
                key=widget_key,
            )
        else:
            raise ValueError(f"Unsupported widget type: {spec.widget}")
    return values
