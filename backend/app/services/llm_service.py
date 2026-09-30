import os
from groq import Groq

class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )
    def generate_sql(self, question: str, schema: dict) -> str:
        prompt = f"""
You are the SQL generation engine for Basewise.

Your task is to convert the user's natural-language request
into a valid PostgreSQL SQL query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

RULES:
1. Use ONLY tables and columns present in the provided schema.
2. Never invent tables or columns.
3. Generate PostgreSQL-compatible SQL.
4. Generate only one SQL statement.
5. Do not execute the query.
6. Do not modify the database schema.
7. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE,
   GRANT, REVOKE, or other destructive statements.
8. For this stage, generate read-only SQL only.
9. Return ONLY the SQL query.
10. Do not include markdown code fences.
11. Do not include explanations.

Return the SQL query now.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You generate safe, valid PostgreSQL SQL queries."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        sql = response.choices[0].message.content

        if not sql:
            raise ValueError("LLM returned an empty SQL response")

        cleaned_sql = sql.strip()
        if cleaned_sql.startswith("```"):
            lines = cleaned_sql.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned_sql = "\n".join(lines).strip()

        return cleaned_sql