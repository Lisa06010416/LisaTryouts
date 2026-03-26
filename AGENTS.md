# AGENTS.md

## Purpose

This repository is for fast experimentation and idea validation. Each experiment is intentionally isolated to enable quick iteration with minimal cross-impact.

## Experiment Boundary Rules

- An experiment directory MAY be single-level or multi-level.
- A directory is treated as an experiment when it has its own experiment-level `README.md`.
- A nested folder is NOT automatically a separate experiment unless it also has its own `README.md`.
- Example valid experiment paths:
  - `LlmExperiments/ImageGeneration/`
  - `LlmExperiments/Generation/ImageGeneration/`

## Change Execution Rules

- Preserve experiment isolation at all times.
- DO NOT move dependencies, config, or runtime assumptions across experiments unless explicitly requested.
- If requirements are ambiguous, create `design.md` inside the target experiment folder first, then wait for confirmation before implementation.

## Documentation Update Rules

**Do NOT update `README.md` for trivial internal edits that do not affect usage, structure, setup, or behavior.**

Update the experiment-level `README.md` when changes affect:
- experiment goal, scope, or expected output
- folder structure or key file responsibilities
- environment setup or dependency commands
- execution workflow or run commands
- major design decisions, trade-offs, or limitations

When a new experiment is added, or when an existing experiment's goal is significantly changed, you MUST also update the root `README.md` under `## Current Experiments`:
- add or update the corresponding experiment path
- add or update a short experiment description

## Environment Management Rules

- Each experiment MUST use its own UV-managed environment.
- DO NOT merge multiple experiments into a shared environment.
- When adding or removing libraries, update `pyproject.toml` in the same experiment.

## Git Credential Rules

- Store Git credentials only in the repository root `.env` file when local Git authentication is needed.
- Use `GITHUB_TOKEN` as the environment variable name for a GitHub personal access token.
- The root `.env.example` file documents the required variable names and placeholder values.
- Do NOT commit the real `.env` file or hardcode tokens in scripts, prompts, docs, or source files.
- When Git operations require authentication, load the root `.env` file first and use the token from `GITHUB_TOKEN`.
- Keep experiment-level secrets isolated unless a token is intentionally shared for repository-wide Git operations.

## Language Rules

- Use Chinese for agent-facing explanations to the user.
- Use English for code, docs, config files, and code comments.
