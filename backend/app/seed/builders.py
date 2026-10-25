"""Small helpers that keep the content files readable."""

LABELS = "ABCD"


def q(prompt, options, answer, explanation, difficulty="medium", table=None, passage=None, check=None):
    """A multiple-choice question. `answer` is the correct label ("A"-"D").

    `check` (quant only) is a zero-argument function returning the numeric answer; a test
    recomputes it and compares it with the number in the correct option's text.
    """
    if len(options) != 4:
        raise ValueError(f"Question needs exactly 4 options: {prompt[:60]}")
    if answer not in LABELS:
        raise ValueError(f"Answer must be A-D: {prompt[:60]}")
    return {
        "prompt": prompt,
        "options": list(options),
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "table": table,
        "passage": passage,
        "check": check,
    }


def ex(problem, steps, answer):
    return {"problem": problem, "steps": list(steps), "answer": answer}


def rule(label, formula, note=None):
    return {"label": label, "formula": formula, "note": note}


def topic(slug, name, summary, concept, key_points, formulas, tips, examples, practice, test):
    return {
        "slug": slug,
        "name": name,
        "summary": summary,
        "concept": concept.strip(),
        "key_points": key_points,
        "formulas": formulas,
        "tips": tips,
        "examples": examples,
        "practice": practice,
        "test": test,
    }


def table(columns, rows, caption=None):
    return {"columns": columns, "rows": rows, "caption": caption}
