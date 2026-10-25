"""Sections and the content index. Lessons and questions live in the content_* modules."""

from app.seed.content_logical import LOGICAL_TOPICS
from app.seed.content_quant import QUANT_TOPICS
from app.seed.content_verbal import VERBAL_PASSAGES, VERBAL_TOPICS

SECTIONS = [
    {
        "slug": "logical",
        "name": "Qualitative Aptitude (Logical Reasoning)",
        "short_name": "Logical",
        "description": "Spot patterns, decode relationships and reason your way to conclusions.",
        "color": "#8b7cf6",
    },
    {
        "slug": "quant",
        "name": "Quantitative Aptitude",
        "short_name": "Quant",
        "description": "Arithmetic, number sense and data skills that placement tests check most.",
        "color": "#3b82f6",
    },
    {
        "slug": "verbal",
        "name": "English / Verbal Ability",
        "short_name": "Verbal",
        "description": "Grammar, vocabulary and reading skills for the English round.",
        "color": "#22a06b",
    },
]

CONTENT = {
    "logical": LOGICAL_TOPICS,
    "quant": QUANT_TOPICS,
    "verbal": VERBAL_TOPICS,
}

PASSAGES = {**VERBAL_PASSAGES}
