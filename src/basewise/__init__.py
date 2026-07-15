"""
Basewise
--------
AI-powered natural language interface for Supabase databases.

This file is the public "front door" of the package. Anything a user
of `import basewise` should be able to access gets exposed here.
As we build out real modules (db connection, schema introspection,
NL-to-SQL, etc.) in later milestones, we will deliberately choose
what gets re-exported from this file — everything else stays
"internal" to the package.
"""

from basewise._version import __version__

__all__ = ["__version__"]
