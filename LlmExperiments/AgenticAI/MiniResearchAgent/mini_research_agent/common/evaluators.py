from __future__ import annotations

from typing import Any


def routing_accuracy(outputs: dict[str, Any], reference_outputs: dict[str, Any]) -> dict[str, Any]:
    expected = reference_outputs["searched"]
    actual = outputs.get("searched")
    return {
        "key": "routing_accuracy",
        "score": 1 if actual == expected else 0,
        "comment": f"expected searched={expected}, got searched={actual}",
    }


def clarification_accuracy(outputs: dict[str, Any], reference_outputs: dict[str, Any]) -> dict[str, Any]:
    expected = reference_outputs["interrupted"]
    actual = outputs.get("interrupted", False)
    return {
        "key": "clarification_accuracy",
        "score": 1 if actual == expected else 0,
        "comment": f"expected interrupted={expected}, got interrupted={actual}",
    }


def reflection_quality(outputs: dict[str, Any], reference_outputs: dict[str, Any]) -> dict[str, Any]:
    critique = outputs.get("critique", "")
    has_signal = len(critique.strip()) >= 12
    return {
        "key": "reflection_quality",
        "score": 1 if has_signal else 0,
        "comment": "critique contains useful signal" if has_signal else "critique is too thin",
    }
