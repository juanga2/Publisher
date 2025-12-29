# ADR-004: Reputation Model (MVP A, future B)

## Decision
MVP reputation is based only on `published_count`, mapped to levels:
0 / 10 / 25 / 50 / 100.

Future: migrate to model B where reverts penalize reputation and unlocks.

## Rationale
- Simple and predictable for MVP
- Provides progressive unlocking of guardrails
- Avoids brittle revert-detection in MVP

## Migration Plan
- Add `reverted_count` and automated revert detection
- Update level computation to incorporate revert penalties
- Keep thresholds in policy config to avoid hardcoding
