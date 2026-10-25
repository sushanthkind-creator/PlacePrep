# PlacePrep API

Base URL (local): `http://localhost:5000/api`

All requests and responses are JSON. Private endpoints need the header
`Authorization: Bearer <access_token>` from register or login.

## Errors

Every error has the same shape:

```json
{ "error": { "code": "validation_error", "message": "Please fix the highlighted fields.", "fields": { "mobile": "Enter a valid 10-digit Indian mobile number starting with 6, 7, 8 or 9." } } }
```

`fields` appears only for form validation errors.

| Status | When |
| --- | --- |
| 400 | Invalid input (`validation_error`, `invalid_body`, `invalid_option`, `invalid_question`) |
| 401 | Missing, expired, revoked or invalid token (`auth_required`, `token_expired`, `token_revoked`, `invalid_token`), or wrong login (`invalid_credentials`) |
| 404 | Not found, including another student's attempt (`not_found`) |
| 409 | Duplicate account (`duplicate_account`), test already submitted (`already_submitted`), results requested before submission (`not_submitted`) |
| 500 | Unexpected server error (`server_error`); details are logged, never returned |

---

## Authentication

### `POST /auth/register`
Create an account and log in.

```json
{
  "full_name": "Asha Verma",
  "mobile": "+91 98765 43210",
  "email": "asha@college.edu",
  "college_name": "Govt Engineering College",
  "password": "Placement2024",
  "confirm_password": "Placement2024"
}
```

- Mobile: 10 digits starting 6–9; `+91`, `91` or `0` prefixes and spaces are accepted and removed.
- Email: any valid address (no fixed college domain), stored lowercase.
- Password: 8–128 characters with at least one letter and one number. Stored as a Werkzeug hash.

`201 Created`

```json
{ "access_token": "eyJ…", "user": { "id": 1, "full_name": "Asha Verma", "email": "asha@college.edu", "mobile": "9876543210", "college_name": "Govt Engineering College", "auth_provider": "password", "has_password": true, "email_verified_by_google": false, "profile_complete": true, "created_at": "2026-10-25T12:00:00Z" } }
```

`409` if the email or mobile number is already registered.

### `POST /auth/login`
`{ "email": "asha@college.edu", "password": "Placement2024" }` → `200` with the same body as register.
Wrong email or password → `401 invalid_credentials` (same message for both).

### `POST /auth/logout` (private)
Revokes the current token on the server. → `200 { "message": "Logged out." }`

### `GET /auth/me` (private)
→ `200 { "user": { … } }`

### `GET /auth/config`
→ `200 { "google_enabled": false, "google_client_id": null }`

### `POST /auth/google`
`{ "credential": "<Google ID token>" }`. Available only when `GOOGLE_CLIENT_ID` is set (otherwise `404 google_disabled`).
The token is verified with Google's library; the email must be verified by Google. Returns a session like login
(`201` for a new account). New Google accounts have `profile_complete: false` until mobile and college are added.

## Profile (private)

### `GET /profile`
→ `200 { "user": { … } }`

### `PATCH /profile`
Any of `full_name`, `mobile`, `college_name`. Email cannot be changed. → `200 { "user": { … } }`

### `POST /profile/password`
`{ "current_password": "…", "new_password": "…", "confirm_password": "…" }`
(`current_password` is not needed for Google-only accounts setting a first password.) → `200`

---

## Learning content (private)

### `GET /sections`
The three sections with the student's progress.

```json
{ "sections": [ { "slug": "quant", "name": "Quantitative Aptitude", "short_name": "Quant", "color": "#3b82f6", "description": "…",
  "topics_total": 14, "topics_completed": 1, "practice_attempted": 3, "practice_correct": 2, "practice_total": 56,
  "test_questions": 5, "test_correct": 1, "test_percentage": 20.0,
  "topics": [ { "slug": "percentages", "name": "Percentages", "completed": true } ] } ] }
```

### `GET /sections/<slug>`
One section; `topics` contains full per-topic progress:

```json
{ "slug": "percentages", "name": "Percentages", "summary": "…", "section_slug": "quant", "completed": true, "completed_at": "…",
  "practice": { "attempted": 2, "correct": 1, "total": 4 }, "tests": { "total": 5, "correct": 1, "percentage": 20.0 }, "best_topic_test": 20.0 }
```

### `GET /topics/<slug>`
Lesson, solved examples, progress and neighbouring topics. Also records that the lesson was viewed.

```json
{ "topic": { "slug": "percentages", "name": "Percentages", "summary": "…", "section": { … },
  "lesson": { "concept": "Paragraphs separated by blank lines", "key_points": ["…"], "formulas": [ { "label": "Percentage change", "formula": "(new − old) / old × 100", "note": null } ], "tips": ["…"] },
  "examples": [ { "id": 1, "problem": "…", "steps": ["…"], "answer": "…" } ],
  "progress": { … }, "previous": null, "next": { "slug": "profit-and-loss", "name": "Profit and Loss" } } }
```

### `GET /topics/<slug>/examples`
→ `{ "examples": [ … ] }`

### `POST /topics/<slug>/progress`
`{ "completed": true }` → `{ "progress": { … } }`

### `GET /progress/topics`
Progress for all 36 topics → `{ "topics": [ … ] }`

## Practice (private)

### `GET /topics/<slug>/practice`
Practice questions **without answer keys**. `review` is filled only for questions the student has already checked.

```json
{ "topic": { … }, "questions": [ { "id": 401, "prompt": "What is 15% of 240?", "table": null, "passage": null, "difficulty": "easy",
  "topic": { "slug": "percentages", "name": "Percentages" },
  "options": [ { "id": 1601, "label": "A", "text": "32" }, … ], "review": null } ] }
```

### `POST /practice/answers`
`{ "question_id": 401, "option_id": 1601 }` → evaluated on the server and recorded.

```json
{ "question_id": 401, "review": { "selected_option_id": 1601, "is_correct": false, "correct_option_id": 1602, "explanation": "240 × 15/100 = 36." } }
```

Only practice-pool questions can be checked here; test questions return `404`.

---

## Tests (private)

Test scopes: `topic` (one topic), `section` (all topics in a section), `mixed` (full placement mock).

### `GET /tests?scope=&section=&topic=`
```json
{ "tests": [ { "id": 15, "slug": "topic-percentages", "title": "Percentages test", "scope": "topic", "section_slug": "quant", "topic_slug": "percentages",
  "description": "…", "default_question_count": 5, "default_duration_minutes": 7, "available_questions": 6, "question_count_range": [3, 6],
  "my_stats": { "attempts": 1, "best": 20.0, "last": 20.0 }, "active_attempt_id": null } ] }
```

### `GET /tests/<id>`
Same card plus `instructions` (list of strings) and `duration_range` (`[1, 180]` minutes).

### `POST /tests/<id>/attempts`
`{ "question_count": 5, "duration_minutes": 7 }` (both optional; defaults apply). Questions are drawn at random,
spread evenly across topics. If the student already has an unfinished attempt of this test, it is returned
instead (`200`, `"resumed": true`); otherwise `201`.

```json
{ "resumed": false, "attempt": { "id": 1, "status": "in_progress", "question_count": 5, "duration_seconds": 420,
  "started_at": "…", "expires_at": "…", "server_time": "…", "remaining_seconds": 420,
  "questions": [ { "id": 421, "position": 1, "prompt": "…", "options": [ { "id": 1681, "label": "A", "text": "24,000" } ], "selected_option_id": null, … } ] } }
```

No correct answers or explanations are included.

### `GET /attempts/<id>`
In progress: the same shape as above, with saved selections and the server's remaining time.
If the timer plus a 15-second grace period has passed, the attempt is first submitted automatically with the
saved answers, and a summary is returned (`status: "submitted"`, no `questions`).

### `PUT /attempts/<id>/answers`
`{ "question_id": 421, "option_id": 1683 }` (use `null` to clear) → `200`. Rejected with `409` once submitted.

### `POST /attempts/<id>/submit`
`{ "answers": [ { "question_id": 421, "option_id": 1683 }, … ] }` (optional; saved answers are used for anything not sent).

- Every question and option ID is validated against the attempt (`400` otherwise).
- Scoring happens only on the server; any score fields in the request are ignored.
- Submitting twice returns `409 already_submitted`. The status change is atomic, so two simultaneous submits still create one result.
- After the timer plus grace has expired, newly sent answers are ignored, only answers saved in time count, and `auto_submitted` is `true`.

Response: the full result (see below).

### `GET /attempts/<id>/result`
```json
{ "attempt": { "id": 1, "test": { … }, "status": "submitted", "question_count": 5, "duration_seconds": 420,
  "started_at": "…", "submitted_at": "…", "auto_submitted": false,
  "correct": 1, "incorrect": 1, "unanswered": 3, "percentage": 20.0, "time_taken_seconds": 45,
  "questions": [ { "id": 421, "position": 1, "prompt": "…", "options": [ … ], "selected_option_id": 1683, "correct_option_id": 1683, "is_correct": true, "explanation": "…" } ],
  "breakdown": { "sections": [ { "slug": "quant", "name": "Quantitative Aptitude", "total": 5, "correct": 1, "incorrect": 1, "unanswered": 3, "percentage": 20.0 } ],
                 "topics": [ { "slug": "percentages", "name": "Percentages", "section_slug": "quant", "total": 5, "correct": 1, "incorrect": 1, "unanswered": 3, "percentage": 20.0 } ] } } }
```

`409 not_submitted` while the attempt is still in progress.

### `GET /attempts?page=1&per_page=20`
Submitted attempts, newest first. `change` is the difference from the previous attempt of the same test (`null` for a first attempt).

```json
{ "attempts": [ { "id": 2, "test": { … }, "percentage": 60.0, "change": 40.0, … } ], "page": 1, "per_page": 20, "total": 2 }
```

---

## Dashboard (private)

### `GET /dashboard`
```json
{ "user": { "full_name": "Asha Verma", "college_name": "…" },
  "tests_attempted": 2, "average_percentage": 60.0,
  "progress": { "topics_completed": 1, "topics_total": 36, "practice_attempted": 3, "practice_total": 144, "percent": 3 },
  "strongest_section": { "slug": "quant", "name": "Quantitative Aptitude", "percentage": 100.0 },
  "weak_topics": [ { "slug": "syllogisms", "name": "Syllogisms", "section_slug": "logical", "percentage": 20.0, "questions": 5 } ],
  "recent_results": [ { …attempt summary…, "change": null } ],
  "trend": [ { "id": 1, "title": "Percentages test", "percentage": 100.0, "submitted_at": "…" } ],
  "sections": [ …same as GET /sections… ],
  "thresholds": { "min_section_questions": 5, "min_topic_questions": 3, "weak_below": 70.0 } }
```

- `strongest_section` is `null` until a section has at least 5 graded test questions.
- `weak_topics` lists topics with at least 3 graded test questions and under 70% accuracy.
- A new student gets zeros, `null` and empty lists. Nothing is invented.

### `GET /dashboard/sections`
→ `{ "sections": [ … ] }`

### `GET /dashboard/topics`
→ `{ "topics": [ … ] }`

### `GET /health`
→ `{ "status": "ok" }` (public)
