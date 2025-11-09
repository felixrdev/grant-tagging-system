# Grant Tagging System
[![CI](https://github.com/felixrdev/lasso-grant-tagging-system/workflows/CI/badge.svg)](https://github.com/felixrdev/lasso-grant-tagging-system/actions)

Deterministic grant tagging and synonym-aware search built with React and Flask.

Add grants (name + description) and automatically get tags like `agriculture`, `education`, or `soil`. Filter and search grants by tags or synonyms (e.g., "learning" → `education`, "irrigation" → `water`).  

---

## Quick Start

**Docker (recommended)**
```bash
make dev
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
````

**Bare metal**

```bash
# Backend
cd backend && pip install -e . && python app.py
# Frontend
cd frontend && pnpm install && pnpm dev
```

**Seed sample data**

```bash
docker compose exec api python scripts/seed.py
```

**Environment**

```bash
USE_LLM=false
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

**Backend `.env`**

```bash
FLASK_ENV=development
PORT=8000
ALLOWED_ORIGINS=http://localhost:5173
```

**Frontend `.env`**

```bash
VITE_API_URL=http://localhost:8000
```

---

## Stack

* Frontend: React 18, TypeScript, Vite, Tailwind, React Query, Zod
* Backend: Flask 3 (Python 3.12), file-based storage, CORS
* Tagging: Keyword matcher + synonym map + optional LLM refinement
* Tooling: pytest, ruff, black, ESLint, GitHub Actions


---

## Project Structure

```
grant-tagging-system/
├─ frontend/
│  └─ src/ (components, lib, App.tsx)
├─ backend/
│  ├─ src/
│  │  ├─ tagging.py, tags.py, synonyms.py, search_index.py
│  │  └─ models.py, store.py, app.py
│  ├─ scripts/seed.py
│  └─ tests/
├─ data/grants_seed.json
├─ docker-compose.yml
├─ Makefile
└─ README.md
```

---

## API

**GET `/api/tags`**

```json
["agriculture", "education", "water", "soil"]
```

**GET `/api/grants`**

```json
[{"grant_name":"Sustainable Agriculture Grant","tags":["agriculture","soil","research"]}]
```

**POST `/api/grants/batch`**

```json
[{"grant_name":"STEM Education Initiative","grant_description":"Programs for students"}]
```

**GET `/api/search?tags=agriculture,soil`**
Filter by multiple tags (AND logic).

**GET `/api/search/advanced?q=learning&mode=any`**
Synonym-aware search:

```json
{
  "resolved_tags": ["education"],
  "grants": [{"grant_name":"STEM Education Initiative","tags":["education","training"]}]
}
```

---

## Tagging Approach

* **Keyword Matching (default)**: deterministic tag rules; no LLM required.
* **Optional LLM Mode**: refines or reorders tags but limited to the predefined tag list.
  Add or edit tags in `tags.py`, `tagging.py`, and `synonyms.py`.

---

## Extension C: Smart Search

* `synonyms.py`: maps phrases like "local food" → `local-food`.
* `search_index.py`: maintains an in-memory inverted index.
* `/api/search/advanced`: resolves synonyms and returns matching grants.
---

## Testing

```bash
cd backend && pytest -v --cov=src
cd ../frontend && pnpm lint && pnpm build
```

---

## Development Commands

```bash
make dev        # run locally
make test       # run tests
make fmt        # format (black/ruff + prettier)
make lint       # lint code
make seed       # load sample data
```

---


## Deployment

**Docker (prod)**

```bash
docker build -f Dockerfile.backend.prod -t grant-tagging-api .
docker build -f Dockerfile.frontend.prod -t grant-tagging-web .
docker compose -f docker-compose.prod.yml up -d
```

**Fly.io / Render / Heroku**
Set environment vars:

* `FLASK_ENV=production`
* `ALLOWED_ORIGINS=https://yourfrontend.app`
* `VITE_API_URL=https://yourbackend.app`

---

## Design Decisions

**Keyword matching instead of LLM-first**

 Most grant descriptions are pretty straightforward: if it mentions "farm" or "crop", it's agriculture. We can tag 1000 grants in milliseconds for free instead of spending $10-20 on API calls. 
 
 For AI accuracy boost, I added an optional LLM refinement (USE_LLM=true) that runs after keyword matching. It can rerank or add tags, but I strictly filter its output to prevent hallucinations

**File-based storage instead of Postgres**

This is a prototype/MVP. JSON files with thread-safe locks are simple to deploy: no database migrations, no connection pools, no ORM. With 10k+ grants or if we need concurrent writes, we can swap to Postgres with the GrantStore interface (a 30-minute change).

**Inverted index for search?**

array.filter() over 1000 grants gets slow real fast. The inverted index gives us O(1) tag lookups and instant "show me all grants with agriculture AND education" queries.

**React Query instead of Redux**

Server state is different from UI state. React Query handles caching, refetching, and optimistic updates out of the box. We don't need Redux's boilerplate for this use case as grants come from the API and not from complex client-side logic.

**Pre-commit hooks**

Helps with formatting to avoid common issues in code reviews. Black/ruff/prettier run automatically so PRs stay focused on logic, not "you forgot a comma."

---

## CI/CD

GitHub Actions run linting, formatting, tests, and builds on pull requests and pushes to `main`.

---

## Roadmap

* Add frontend tests, better error handling, grant editing
* Add JWT auth, analytics dashboard
* Future: ML-based tag suggestions, vector search, multi-language support

