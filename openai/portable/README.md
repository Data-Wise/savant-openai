# Portable layer

This directory is the intended source of truth for contracts that can be
shared by ChatGPT and Codex. It must not contain host configuration, Claude
hooks, model settings, credentials, or lifecycle assumptions.

The first implementation extracts only verification statuses and the evidence
report schema. Domain-specific references are materialized into the OpenAI
skill only after contract tests exist.

Reviewed bounded-learning lessons live under `learning/approved/` and are
versioned like code. Candidate state and host configuration remain outside the
portable layer.
