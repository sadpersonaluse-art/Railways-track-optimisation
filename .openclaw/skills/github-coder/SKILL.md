# GitHub Coding Agent

## Purpose
This skill allows OpenClaw to directly edit code files inside the local repository workspace and push changes to GitHub.

---

## Capabilities

- Create new files
- Modify existing files
- Refactor code
- Run tests
- Run docker commands
- Commit changes
- Push branches to GitHub

---

## Repository Rules

- Always work inside:
  /workspace/Railways-track-optimisation

- Never modify secrets or environment credentials.

- Prefer:
  - FastAPI backend
  - Python 3.11
  - React + TypeScript frontend
  - Dockerized workflows

---

## Git Workflow

When making changes:

1. Create or checkout a feature branch
2. Edit files directly
3. Run tests if available
4. Commit changes with meaningful commit messages
5. Push to GitHub

Example:

git checkout -b feat/new-feature

git add .

git commit -m "feat: add new feature"

git push origin feat/new-feature

---

## Allowed Commands

- git
- python
- pytest
- docker
- docker compose
- pip
- uvicorn

---

## Preferred Backend Structure

backend/
├── src/
│   ├── api/
│   ├── core/
│   ├── ml/
│   └── main.py

---

## Example Tasks

- Add FastAPI endpoint
- Add ML pipeline
- Create React dashboard
- Fix Docker issues
- Add unit tests
- Update GitHub Actions workflows
