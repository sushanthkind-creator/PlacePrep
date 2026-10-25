# PlacePrep – Smart Placement Training Platform

PlacePrep helps college students prepare for campus placement aptitude rounds. Students register, study short lessons,
practise questions with instant explanations, take timed tests that are scored on the server, and track their progress
over time.

It covers exactly three learning sections:

| Section | Topics |
| --- | --- |
| **Qualitative Aptitude (Logical Reasoning)** | Blood Relations, Coding and Decoding, Number and Letter Series, Direction Sense, Seating Arrangements, Syllogisms, Analogies, Logical Puzzles, Statement and Conclusion, Critical Thinking |
| **Quantitative Aptitude** | Percentages, Profit and Loss, Ratios and Proportions, Averages, Time and Work, Time Speed and Distance, Simple and Compound Interest, Number Systems, Probability, Permutations and Combinations, Mixtures and Alligations, Problems on Ages, Data Interpretation, Simplification |
| **English / Verbal Ability** | Grammar, Tenses, Subject-Verb Agreement, Articles and Prepositions, Vocabulary, Synonyms and Antonyms, Sentence Correction, Error Spotting, Fill in the Blanks, Reading Comprehension, Para Jumbles, Sentence Completion |

## Features

- **Animated landing and login.** A 3D Rubik's cube (Three.js) that you can drag, which solves itself as you scroll (anime.js), ending in the login card.
- **Accounts.** Registration with full name, Indian mobile number, college email, college name and password. Passwords are hashed with Werkzeug. Duplicate emails and mobile numbers are rejected. Login checks the database. JWT sessions with server-side logout. Optional "Continue with Google".
- **36 lessons.** A beginner-friendly explanation, key points, formulas or rules, shortcuts and traps, and two solved examples with numbered steps for every topic.
- **Practice.** 4 multiple-choice questions per topic, checked on the server, with the correct answer and an explanation shown after you answer.
- **Tests.** Topic, section and full mock tests. You choose the question count and time limit. Next/Previous navigation and a question grid showing answered and unanswered questions. A countdown timer with automatic submission at zero, and manual submission with a confirmation step. Answers are saved as you go, so a reload resumes the test.
- **Server-side scoring.** Answer keys never reach the browser before submission, scores are computed only on the server, and duplicate submissions are blocked atomically.
- **Results.** Correct, incorrect and unanswered counts, percentage, time taken, section and topic breakdowns, and every question with its explanation.
- **Dashboard and progress.** Topics completed, practice answered, test history with change since the last attempt, a score trend chart, your strongest section and topics that need improvement. All of it is computed from your own recorded activity, and new students see empty states, not invented numbers.
- **Dark and light themes**, responsive layouts from phone to desktop, keyboard-accessible controls, and reduced-motion support.

All learning content is original. Each Quant question's answer is recomputed in code by the test suite.

## Tech stack

| Part | Technology |
| --- | --- |
| Frontend | React 18, Vite 6, React Router 6, Recharts, anime.js 4, Three.js |
| Backend | Python 3, Flask 3, Flask-SQLAlchemy (SQLAlchemy 2), Flask-Migrate (Alembic), Flask-JWT-Extended, Flask-CORS, Werkzeug password hashing |
| Database | SQLite for local use (switch `DATABASE_URL` to PostgreSQL later) |
| Tests | pytest (backend) |

## Folder structure

```
PlacePrep/
├── backend/
│   ├── app/
│   │   ├── __init__.py          create_app(), CLI commands (seed, init-db)
│   │   ├── config.py            settings from environment variables
│   │   ├── extensions.py        db, migrate, jwt, cors
│   │   ├── models/              user, learning (section/topic/lesson/example/passage),
│   │   │                        question (+ options), test (definition/attempt/answers), progress
│   │   ├── routes/              auth, profile, learning, practice, tests, dashboard
│   │   ├── services/            scoring, attempts (test engine), progress (stats), google_auth
│   │   ├── schemas/             request validation for auth and tests
│   │   ├── seed/                idempotent seeding + original content for all 36 topics
│   │   └── utils/               errors, JWT handlers, validation, time helpers
│   ├── migrations/              Alembic migration scripts
│   ├── tests/                   pytest suite
│   ├── run.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/                 fetch client + auth, learning, tests, dashboard calls
│   │   ├── components/          layout, sidebar, question card, timer, chart, hero/ (3D cube)
│   │   ├── context/             AuthContext, ThemeContext
│   │   ├── pages/               14 pages (landing, register, login, dashboard, sections, lesson,
│   │   │                        practice, tests, instructions, active test, results, history, profile)
│   │   ├── styles/              global, app, auth, landing, dashboard, learning, test
│   │   └── utils/               validation, formatting, hooks
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── docs/API.md                  every endpoint with request/response examples
├── .gitignore
└── README.md
```

## Prerequisites

- **Python 3.10+** (tested with 3.13)
- **Node.js 18+** and npm

## Setup

The commands below are for **Windows PowerShell**. On macOS or Linux, replace `.\.venv\Scripts\` with `.venv/bin/` and `copy` with `cp`.

### 1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
```

Open `backend/.env` and replace both secret placeholders with long random strings. Generate each one with:

```powershell
.\.venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))"
```

Create the database tables and load the learning content:

```powershell
.\.venv\Scripts\flask --app run db upgrade
.\.venv\Scripts\flask --app run seed
```

`seed` can be run any number of times. It updates content in place and never creates duplicates.

Start the API (it runs on http://localhost:5000):

```powershell
.\.venv\Scripts\python run.py
```

### 2. Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. To point the frontend at a different API address, copy `frontend/.env.example` to `frontend/.env` and edit `VITE_API_BASE_URL`.

### Environment variables

| Variable | Where | Purpose |
| --- | --- | --- |
| `SECRET_KEY`, `JWT_SECRET_KEY` | backend | Signing keys. If missing, temporary random keys are used and everyone is logged out on restart. |
| `DATABASE_URL` | backend | Defaults to `sqlite:///placeprep.db` (stored in `backend/instance/`). |
| `CORS_ORIGINS` | backend | Comma-separated frontend origins allowed to call the API. |
| `JWT_ACCESS_TOKEN_EXPIRES_HOURS` | backend | Session length, default 8. |
| `GOOGLE_CLIENT_ID` | backend | Optional. Enables "Continue with Google"; leave empty to hide the button. |
| `VITE_API_BASE_URL` | frontend | API base URL, default `http://localhost:5000/api`. |

**Optional Google sign-in:** create an OAuth 2.0 Client ID (type "Web application") in Google Cloud Console, add `http://localhost:5173` to *Authorized JavaScript origins*, and put the client ID in `GOOGLE_CLIENT_ID`. Google users add their mobile number and college once after their first sign-in.

## Running the tests

```powershell
cd backend
.\.venv\Scripts\python -m pytest
```

The suite (214 tests) covers:
- registration, validation and duplicate accounts
- login, logout and token revocation, and protected routes
- learning content for every topic
- practice evaluation, and that test answers can't leak through practice
- test scoring, the timer and grace period, and late submissions
- duplicate-submission blocking
- access control between students and CORS
- dashboard accuracy
- content integrity: 4 options and exactly 1 answer per question, recomputed Quant answer keys, and idempotent seeding

## API reference

See [docs/API.md](docs/API.md).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `cd /d …` fails in PowerShell | `/d` is Command Prompt syntax. In PowerShell use `cd D:\path\to\PlacePrep\frontend`. |
| "Can't reach the PlacePrep server" | Start the backend (`.\.venv\Scripts\python run.py` in `backend`) and check http://localhost:5000/api/health. |
| `Port 5173 is already in use` | Another dev server is running. Close that terminal, or open the URL Vite prints instead. |
| Logged out every time the backend restarts | Set `SECRET_KEY` and `JWT_SECRET_KEY` in `backend/.env`. |
| CORS error in the browser console | Add the exact frontend origin (for example `http://127.0.0.1:5173`) to `CORS_ORIGINS` and restart the backend. |
| `no such table` errors | Run `flask --app run db upgrade` and `flask --app run seed` in `backend`. |
| Start over with an empty database | Stop the backend, delete `backend/instance/placeprep.db`, then run `db upgrade` and `seed` again. |
| PowerShell blocks `Activate.ps1` | You don't need it. The commands above call `.\.venv\Scripts\python` directly. |
| No "Continue with Google" button | Expected unless `GOOGLE_CLIENT_ID` is set in `backend/.env`. |

## Known limitations

- The content is a realistic sample, not a full question bank: 10 questions per topic (4 practice and 6 test), 360 in total.
- Email and mobile numbers are format-checked only. No email or SMS verification is done, and the app never claims otherwise (except "verified by Google" for Google sign-ins).
- The session token is stored in `localStorage`. That's simple and common, but a cross-site-scripting bug could expose it. React escapes all rendered text, and the app never injects raw HTML.
- There's no rate limiting on login yet.
- SQLite suits local use and demos; use PostgreSQL for many simultaneous users.
- `npm audit` reports two moderate React Router 6 advisories that don't apply here: one needs server-side rendering, the other needs navigation to user-supplied URLs.
