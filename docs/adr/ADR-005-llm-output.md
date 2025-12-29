# ADR-005: LLM Output Format (Full Wikitext)

## Decision
LLM returns full proposed wikitext for the draft. Backend computes unified diff.

## Rationale
- Avoids broken patches/diffs from the model
- Simplifies application logic (replace-and-diff)
- Deterministic diff generation on server

## Consequences
- Larger payloads and more tokens
- Must validate strongly to avoid unintended rewrites
