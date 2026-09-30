import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError, TokenError


class SQLSafetyService:
    """
    Defensive validation layer for generated SQL queries.
    Enforces strict read-only SELECT constraints using AST parsing and semantic inspection.
    """

    FORBIDDEN_KEYWORDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
        "COPY",
        "EXEC",
        "EXECUTE",
        "MERGE",
    }

    FORBIDDEN_AST_NODES = (
        exp.Insert,
        exp.Update,
        exp.Delete,
        exp.Drop,
        exp.Alter,
        exp.Create,
        exp.TruncateTable,
        exp.Grant,
        exp.Revoke,
        exp.Into,
        exp.Command,
        exp.Merge,
        exp.Copy,
    )

    def validate(self, sql: str) -> tuple[bool, str]:
        """
        Validates whether the provided SQL string is a safe, single, read-only SELECT query.
        Returns a tuple: (is_safe: bool, message: str).
        """
        if not sql or not sql.strip():
            return False, "SQL query is empty."

        cleaned_sql = sql.strip()

        # Handle markdown code fences if LLM wrapped SQL in ```sql ... ```
        if cleaned_sql.startswith("```"):
            lines = cleaned_sql.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned_sql = "\n".join(lines).strip()

        if not cleaned_sql:
            return False, "SQL query is empty."

        # Check for multiple statements separated by semicolon
        cleaned_no_trailing = cleaned_sql.rstrip(";").strip()
        if ";" in cleaned_no_trailing:
            return False, "Multiple SQL statements are not allowed."

        # Tokenize with PostgreSQL dialect
        try:
            tokens = sqlglot.tokenize(cleaned_sql, read="postgres")
        except (TokenError, Exception) as e:
            return False, f"Invalid SQL tokens or syntax: {str(e)}"

        # Reject SQL comments to prevent comment-based filter bypasses
        for token in tokens:
            if token.comments:
                return False, "SQL comments are not allowed."

        # Parse AST with PostgreSQL dialect
        try:
            parsed_statements = sqlglot.parse(cleaned_sql, read="postgres")
        except (ParseError, Exception) as e:
            return False, f"Invalid SQL syntax: {str(e)}"

        # Filter out None statements from trailing semicolons
        parsed_statements = [s for s in parsed_statements if s is not None]

        if not parsed_statements:
            return False, "SQL query is empty."

        if len(parsed_statements) > 1:
            return False, "Multiple SQL statements are not allowed."

        root = parsed_statements[0]

        # The root statement MUST be a SELECT query or UNION of SELECT queries
        if not isinstance(root, (exp.Select, exp.Union)):
            op_name = getattr(root, "key", type(root).__name__).upper()
            return False, f"Only SELECT queries are allowed (found {op_name})."

        # Walk the AST to detect any nested DDL/DML, INTO clauses, or forbidden operations
        for node in root.walk():
            if isinstance(node, self.FORBIDDEN_AST_NODES):
                node_type = type(node).__name__.upper()
                return False, f"Forbidden SQL operation detected: {node_type}."

        # Secondary defense-in-depth: check for forbidden keyword tokens outside literal strings
        for token in tokens:
            if token.text.upper() in self.FORBIDDEN_KEYWORDS:
                return False, f"Forbidden SQL keyword detected: {token.text.upper()}."

        return True, "SQL query passed safety validation."