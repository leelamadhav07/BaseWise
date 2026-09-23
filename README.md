# Basewise

AI-powered natural language interface for Supabase/PostgreSQL databases. Basewise allows users to interact with a connected database using plain natural language instead of writing SQL manually.

The system automatically understands the connected database schema, interprets the user's request, generates the appropriate SQL, validates the query for safety, executes it, and returns the result in a human-readable form.

In later milestones, Basewise will also support visualizations, query history, authentication, anomaly/trend detection, role-based access control, and natural-language schema changes with preview-and-confirm safeguards.

## Project Structure

This repository is organized into the application backend, reusable core package, tests, examples, and frontend.

```text
basewise/
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── schema.py
│   │   │   └── database.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── schema_service.py
│   │   │   └── database_service.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   │
│   │   └── dependencies/
│   │       └── __init__.py
│   │
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
├── src/
│   └── basewise/            # Reusable core package
│       └── database.py
│
├── tests/                   # Automated tests
│
├── examples/                # Manual experiments/examples
│
├── frontend/                # React frontend (later milestone)
│
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
``` 

## Architecture:

User
  ↓
Natural Language Request
  ↓
FastAPI API
  ↓
Schema Understanding
  ↓
Natural Language → SQL
  ↓
SQL Safety Validation
  ↓
SQL Execution
  ↓
Result Processing
  ↓
Natural-language Answer
  ↓
Table / Visualization

## Core Workflow: 

1. User connects a PostgreSQL/Supabase database.
2. Basewise tests the database connection.
3. Basewise introspects the database schema.
4. Tables, columns, data types, and relationships are collected.
5. User submits a question in natural language.
6. Relevant schema information is prepared as context.
7. The AI layer interprets the user's request.
8. SQL is generated.
9. Generated SQL is validated before execution.
10. Safe SQL is executed against the connected database.
11. The result is processed.
12. Basewise returns a human-readable answer.
13. Results can later be represented using tables and visualizations.

## Current Features:

The current backend provides the foundation for:

FastAPI application
Health-check endpoints
PostgreSQL database connection
Supabase database connectivity
Dynamic database connection endpoint
Database schema introspection
Table discovery
Column discovery
Data-type discovery
Nullable-column information
Foreign-key relationship discovery
Unified schema representation
Swagger/OpenAPI API testing

## Planned Features:

The following features will be implemented incrementally:

Natural Language → SQL
SQL safety validation
SQL execution
Natural-language result explanation
Query history
Authentication
React frontend
Result visualization
Feedback loop
Supabase Realtime integration
Anomaly and trend alerts
Role-Based Access Control (RBAC)
Natural-language schema modification
Migration preview and confirmation
Migration/audit logging
Reusable Python package

## Technology Stack:

### Backend:
Python
FastAPI
Uvicorn
Pydantic
python-dotenv
psycopg2
### Database:
PostgreSQL
Supabase
Supabase Session Pooler
### Frontend:
React
TypeScript
### AI Layer:
Large Language Models
Replaceable LLM provider architecture
### Development Tools:
Git
GitHub
Swagger / OpenAPI
pytest

## Security Principles:

Database access is one of the most important security boundaries in
Basewise.

The project follows these principles:

1. Never commit database credentials.
2. Never expose database passwords.
3. Never send database credentials to an LLM.
4. Never blindly execute generated SQL.
5. Treat generated SQL as untrusted.
6. Validate SQL before execution.
7. Prefer read-only database credentials for analytics.
8. Keep different users' database contexts isolated.
9. Restrict destructive database operations.
10. Add authentication before production multi-user usage.
11. Require confirmation before schema-changing operations.
12. Maintain migration/audit records for future schema modifications.

## Research Foundation:

Basewise is based on research areas including:

1.Natural Language Interfaces for Databases
2.Text-to-SQL
3.Schema Linking
4.Large Language Models for SQL
5.Constrained SQL Generation
6.Text-to-SQL Security
7.Self-Correction
8.Database-grounded reasoning
9.Multi-agent Text-to-SQL systems

