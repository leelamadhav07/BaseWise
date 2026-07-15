# Basewise Backend (FastAPI)

Not built yet — this comes after the core `basewise` package (in
`src/basewise/`) has real working logic behind it.

When we get here, this folder will contain a **thin FastAPI layer**
that:

- Imports and calls into the `basewise` package (installed via
  `pip install -e .` from the repo root)
- Exposes HTTP endpoints the React frontend can call
- Contains **no business logic of its own** — no SQL generation, no
  schema introspection, no query execution code. All of that lives in
  the package. This folder just adapts the package's Python API into
  a web API.

This constraint is deliberate: it's what makes `basewise` genuinely
reusable outside of this one demo app.
