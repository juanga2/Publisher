# Wikipedia Assisted Editing Tool

## Purpose
Self-hosted application to assist a human editor in contributing to Wikipedia
using MediaWiki APIs and LLMs, with mandatory human review and strict guardrails.

The system:
- suggests articles to improve (equivalent to "Ediciones sugeridas")
- proposes changes using IA (refs + maintenance initially)
- enforces Wikipedia policies (NPOV, verifiability, BLP)
- requires explicit human approval before publishing

## Non-goals (MVP)
- No autonomous editing
- No bulk edits
- No article creation
- No bypassing of Wikipedia policies
- No concealment of tool usage

## Target
- MVP: es.wikipedia.org, single-user
- Architecture prepared for multi-wiki and multi-user
