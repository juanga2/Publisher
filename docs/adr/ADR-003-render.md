# ADR-003: Render Strategy (REST primary, action=parse fallback)

## Decision
Render wikitext to HTML using MediaWiki REST API as the primary method.
Fallback to MediaWiki action API `action=parse` when REST is unavailable or fails.

## Rationale
- REST HTML endpoints are designed for rendering and are generally preferred
- `action=parse` provides a reliable fallback
- Ensures MVP includes render panel even if REST differs by wiki

## Consequences
- Must implement and test fallback behavior
- Must sanitize HTML output in the frontend
