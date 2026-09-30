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
You are a SQL generation assistant.
Convert the user's natural-language question into a PostgreSQL SQL query.
Use ONLY the tables and columns provided in the database schema.
Do not invent tables or columns.
Return ONLY the SQL query.
Do not use markdown code fences.
Do not provide explanations.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}
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

        return sql.strip()