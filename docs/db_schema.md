# Database Schema (v1)

IDs: Use UUID or ULID. Prefer ULID for time-ordered inserts.

## Tables

### users
- id (pk)
- email (nullable; single-user may omit)
- display_name
- created_at

Indexes:
- unique(email) if email used

### wikis
- id (pk) e.g. eswiki
- name
- api_base
- rest_base
- created_at

### linked_accounts
- id (pk)
- user_id (fk users)
- wiki_id (fk wikis)
- mw_username
- oauth_token_encrypted
- oauth_token_secret_encrypted
- scopes (json/text)
- created_at, updated_at

Indexes:
- unique(user_id, wiki_id)

### feed_skips
- id (pk)
- user_id
- wiki_id
- page_id
- task_type
- skipped_at

Indexes:
- (user_id, wiki_id, task_type, skipped_at)
- optional unique(user_id, wiki_id, page_id, task_type)

### drafts
- id (pk)
- user_id
- wiki_id
- page_id
- title
- base_rev_id
- task_type
- status (editing|ready|blocked|published|abandoned)
- wikitext (text)
- created_at, updated_at

Indexes:
- (user_id, wiki_id, updated_at)
- (wiki_id, page_id)

### proposals
- id (pk)
- draft_id (fk drafts)
- provider
- model
- prompt_version
- request_payload (json)  # no secrets
- response_payload (json)
- created_at

Indexes:
- (draft_id, created_at)

### validations
- id (pk)
- draft_id (fk drafts)
- status (pass|fail)
- issues (json)
- metrics (json)
- created_at

Indexes:
- (draft_id, created_at)

### publications
- id (pk)
- draft_id (fk drafts)
- user_id
- wiki_id
- page_id
- old_rev_id
- new_rev_id
- edit_summary
- minor (bool)
- status (success|failed)
- error (json/text)
- created_at

Indexes:
- (user_id, created_at)
- (wiki_id, page_id, created_at)

### user_reputation
- user_id (pk, fk users)
- published_count
- reverted_count (post-MVP)
- level (int)
- updated_at

### guardrail_policies
- id (pk)
- name (e.g. default)
- config (json)  # rules, thresholds, unlock levels
- created_at, updated_at

### user_guardrail_settings
- id (pk)
- user_id
- policy_id
- overrides (json)
- updated_at
