# ADR-001: MediaWiki OAuth 1.0a

## Decision
Use MediaWiki OAuth 1.0a for authentication against Wikipedia.

## Rationale
- Supported by MediaWiki for user-authorized edit access
- Avoids storing user passwords
- Enables least-privilege scopes

## Consequences
- Requires consumer key/secret setup per wiki
- Must securely store user access tokens (encrypted)

## Implementation Notes
- Secrets only in backend
- Tokens encrypted at rest in DB
