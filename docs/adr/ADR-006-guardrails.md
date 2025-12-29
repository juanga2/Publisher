# ADR-006: Guardrails Strategy

## Decision
Use conservative guardrails by default (Pack 1), unlockable via reputation and user overrides.

## Default Pack (MVP)
- Block biographies of living persons (BLP) using conservative heuristics (false positives OK)
- Block sensitive or current events topics (conservative heuristic)
- Max diff size: 20 lines (except references task)
- References task: add-only changes (no rewrites)

## Rationale
- Minimize reverts and protect editor reputation
- Align with Wikipedia best practices
- Reduce risk from LLM hallucinations

## Consequences
- Some false positives accepted
- Unlocking requires reputation progression

## Future
- Configurable per-task guardrails
- Reputation penalties for reverts
