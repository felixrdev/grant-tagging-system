# 🎬 Loom Recording Script: Grant Tagging System UX Demo

## Setup (30 seconds)
- [ ] Open browser to http://localhost:5173
- [ ] Show backend running at http://localhost:8000/api/health
- [ ] Quick tour: "Here's the grant tagging system I built"

## Part 1: Seed Sample Data (30 seconds)
- [ ] Open terminal
- [ ] Run: `docker compose exec api python scripts/seed.py`
- [ ] Show terminal output: "Seeded 8 grants successfully"
- [ ] Refresh browser to see grants appear

## Part 2: Browse & Filter Tags (60 seconds)
- [ ] Click "Browse" in navigation
- [ ] Show 8 grants loaded with auto-assigned tags
- [ ] Point out tag diversity: agriculture, education, sustainability, etc.
- [ ] Click on "agriculture" tag → see grants filtered
- [ ] Click on "education" tag → see different grants
- [ ] Click "Clear filters" → all grants return

## Part 3: Search with Synonyms (45 seconds)
- [ ] In search box, type: "farmers"
- [ ] Show synonym resolution chip: "farmers → agriculture"
- [ ] See grants with "agriculture" tag appear
- [ ] Clear search
- [ ] Type: "youth"
- [ ] Show synonym resolution: "youth → education"
- [ ] See education grants appear
- [ ] Try multi-word: "climate change"
- [ ] Show: "climate change → sustainability"

## Part 4: Advanced Search Modes (30 seconds)
- [ ] Type: "agriculture education"
- [ ] Show default "Match any" mode → many results
- [ ] Switch to "Match all" mode
- [ ] See fewer results (only grants with BOTH tags)
- [ ] Explain: "This is the inverted index at work - instant lookups"

## Part 5: Add New Grant (60 seconds)
- [ ] Click "Add Grant" button
- [ ] Fill in grant form:
  - Name: "Youth Farm Leadership Program"
  - Description: "Teaching young people sustainable farming practices and agricultural business management"
- [ ] Click "Tag & Submit"
- [ ] Show auto-tagging in action:
  - Tags assigned: agriculture, education, youth, sustainability
  - Point out: "No LLM, pure keyword matching, instant"
- [ ] Grant appears in list with tags

## Part 6: Test Another Grant (45 seconds)
- [ ] Add another grant:
  - Name: "Water Conservation Initiative"
  - Description: "Installing drip irrigation systems for drought-affected farms"
- [ ] Tags assigned: agriculture, water-conservation, climate-resilience
- [ ] Click on "water-conservation" tag
- [ ] See only that grant (filtering works)

## Part 7: Search Edge Cases (30 seconds)
- [ ] Search: "teaching" → resolves to "education"
- [ ] Search: "crops" → resolves to "agriculture"  
- [ ] Search: "nonprofit" → resolves to "community"
- [ ] Show: "90+ synonym mappings make this smart"

## Part 8: Code Walkthrough (Optional - 60 seconds)
- [ ] Open VSCode
- [ ] Show `backend/src/synonyms.py`: "Here's the synonym map"
- [ ] Show `backend/src/search_index.py`: "Inverted index for O(1) lookups"
- [ ] Show `backend/tests/`: "48 tests, 95% coverage"
- [ ] Run: `pytest -v` → all green

## Wrap Up (30 seconds)
- [ ] "This system tags grants instantly with zero AI costs"
- [ ] "Optional LLM refinement available via USE_LLM flag"
- [ ] "Production-ready with Docker, tests, pre-commit hooks"
- [ ] "Check out the README for deployment to Fly.io/Render/Heroku"

---

## Total Time: ~6-7 minutes

## Key Points to Emphasize:
✅ Instant tagging (sub-millisecond)
✅ Smart search with 90+ synonyms
✅ Inverted index for fast filtering
✅ No hallucinations (only predefined tags)
✅ Graceful UX (debounced search, resolved tag chips)
✅ Production-ready (Docker, tests, deployment guides)
✅ Optional LLM enhancement (hybrid approach)
