# Basewise

AI-powered natural language interface for Supabase databases.

Basewise lets a user ask questions about a connected database in plain
English. It figures out the schema automatically, generates and runs
the right query, and returns an answer with relevant visualizations.
It can also propose schema changes (new tables/columns) from natural
language, with a preview-and-confirm safeguard before anything is
applied.

## Project structure

This repository has two parts:

1. **`src/basewise/`** — the reusable core Python package. This is the
   part that gets published (`pip install basewise`) and can be used
   in any Python project. All the real logic (schema introspection,
   NL→SQL, query execution, visualization, schema migration, etc.)
   lives here.

2. **`backend/`** and **`frontend/`** — a demo web application (FastAPI
   + React) that showcases the package's capabilities. The demo app
   contains **no core business logic of its own** — it only calls into
   the `basewise` package. This is enforced on purpose, so the package
   stays genuinely reusable and isn't secretly tangled up with one
   particular web app.

```
basewise/
├── pyproject.toml        # package build/metadata config
├── src/basewise/         # the installable core package
├── tests/                # tests for the core package
├── backend/              # FastAPI demo app (added in a later milestone)
└── frontend/             # React demo app (added in a later milestone)
```

## Status

🚧 Early scaffolding stage (Milestone 1: packaging skeleton). No real
features implemented yet.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```
