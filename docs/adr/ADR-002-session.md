# ADR-002: Session Cookie + CSRF

## Decision
Use backend-managed sessions with an HttpOnly cookie and CSRF protection for mutations.

## Rationale
- Simplifies security compared to JWT rotation
- Compatible with Next.js frontend calling FastAPI
- Reduces token leakage risk

## Consequences
- Requires CSRF token management on the frontend
- Requires sticky sessions only if horizontally scaling without shared session store (future)
