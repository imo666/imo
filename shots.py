from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Sequence


@dataclass
class ProjectManifest:
    """Project-level configuration for cinematic grammar."""

    default_shot_weights: Mapping[str, float] = field(
        default_factory=lambda: {
            "wide": 0.3,
            "medium": 0.35,
            "close_up": 0.25,
            "detail": 0.1,
        }
    )
    action_shot_overrides: Mapping[str, Mapping[str, float]] = field(
        default_factory=dict
    )


@dataclass
class SceneV3:
    """Information about a scene used to shape shot generation."""

    id: str
    description: str | None = None
    action_type: str = "dialogue"
    narrative_weight: float = 0.5


@dataclass
class ShotV3:
    """Representation of a single shot within a scene."""

    id: str
    scene_id: str
    order: int
    shot_type: str
    emphasis: float
    description: str


def _normalize_weights(weights: Mapping[str, float]) -> Dict[str, float]:
    filtered = {k: v for k, v in weights.items() if v > 0}
    if not filtered:
        return {"medium": 1.0}
    total = sum(filtered.values())
    return {k: v / total for k, v in filtered.items()}


def _apply_narrative_bias(weights: Dict[str, float], importance: float) -> Dict[str, float]:
    adjusted = dict(weights)
    if importance >= 0.66:
        adjusted["close_up"] = adjusted.get("close_up", 0) + 0.15
        adjusted["detail"] = adjusted.get("detail", 0) + 0.05
    elif importance <= 0.33:
        adjusted["wide"] = adjusted.get("wide", 0) + 0.1
    return _normalize_weights(adjusted)


def _build_sequence(ordered_types: Sequence[str], counts: Dict[str, int], total: int) -> List[str]:
    sequence: List[str] = []
    while len(sequence) < total:
        for shot_type in ordered_types:
            if counts.get(shot_type, 0) > 0:
                sequence.append(shot_type)
                counts[shot_type] -= 1
                if len(sequence) == total:
                    break
    return sequence


def _allocate_counts(weights: Dict[str, float], total: int) -> Dict[str, int]:
    scaled = {k: v * total for k, v in weights.items()}
    counts = {k: int(v) for k, v in scaled.items()}
    remainder = total - sum(counts.values())
    if remainder:
        remainders = sorted(
            ((k, scaled[k] - counts[k]) for k in scaled),
            key=lambda item: (-item[1], item[0]),
        )
        for i in range(remainder):
            counts[remainders[i % len(remainders)][0]] += 1
    return counts


def generate_shots_for_scene(
    manifest: ProjectManifest,
    scene: SceneV3,
    num_shots: int = 3,
) -> List[ShotV3]:
    """
    Genera una lista de ShotV3 para una escena dada, distribuyendo los tipos de plano
    en función del peso narrativo y el tipo de acción.
    """
    if num_shots <= 0:
        return []

    base_weights = dict(manifest.default_shot_weights)
    action_weights = manifest.action_shot_overrides.get(scene.action_type)
    if action_weights:
        base_weights.update(action_weights)

    biased_weights = _apply_narrative_bias(base_weights, scene.narrative_weight)
    counts = _allocate_counts(biased_weights, num_shots)

    ordering = sorted(counts.keys(), key=lambda k: (-biased_weights[k], k))
    shot_types = _build_sequence(ordering, counts, num_shots)

    description_hint = scene.description or "momento clave"
    shots: List[ShotV3] = []
    for idx, shot_type in enumerate(shot_types, start=1):
        emphasis = biased_weights.get(shot_type, 0)
        shot_id = f"{scene.id}-shot-{idx}"
        detail = f"{shot_type.replace('_', ' ')} del/la {scene.action_type}".strip()
        full_description = f"{detail}: {description_hint}"
        shots.append(
            ShotV3(
                id=shot_id,
                scene_id=scene.id,
                order=idx,
                shot_type=shot_type,
                emphasis=emphasis,
                description=full_description,
            )
        )

    return shots
