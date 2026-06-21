# Development Guidelines

Welcome to the GridWise AI development guidelines. This document outlines the standards and workflows we use to build and maintain the project.

## 1. Branching Strategy

We use a feature-branching model:
- `main`: The primary, production-ready branch. All code in this branch should be deployable.
- `feature/<issue-id>-<short-description>`: For developing new features.
- `bugfix/<issue-id>-<short-description>`: For fixing bugs.
- `docs/<short-description>`: For documentation updates.

## 2. Commit Messages

We strictly follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat: <description>`: A new feature.
- `fix: <description>`: A bug fix.
- `docs: <description>`: Documentation changes.
- `style: <description>`: Changes that do not affect the meaning of the code (white-space, formatting, etc).
- `refactor: <description>`: A code change that neither fixes a bug nor adds a feature.
- `test: <description>`: Adding missing tests or correcting existing tests.
- `chore: <description>`: Changes to the build process or auxiliary tools and libraries.

## 3. Code Style & Linting

### Python (Backend & ML)
- **Formatter**: We use `ruff` to format our code. 
- **Type Checking**: Use `mypy` for static typing. Type hints are mandatory for all new backend endpoints and services.

### TypeScript (Frontend)
- **Formatter/Linter**: We rely on standard ESLint rules and Prettier for code formatting.
- **Strict Typing**: TypeScript `strict` mode is enabled. Avoid using `any`; define robust interfaces or types for all payloads.

## 4. Testing

All new features or bug fixes must include corresponding automated tests. 
- **Backend**: Use `pytest` for unit and integration testing. Run `pytest` locally before submitting a PR.
- **Frontend**: Component tests and end-to-end (E2E) tests are required for critical user journeys.

## 5. Pull Requests (PRs)

1. Ensure your branch is up-to-date with `main`.
2. Run the full test suite locally.
3. Open a PR with a clear, descriptive title.
4. Fill out the PR template completely.
5. Request review from at least one maintainer.

## 6. MLOps & Data Versioning

If you are modifying models or datasets:
- Remember to track all ML experiments using our **DagsHub / MLflow** integration.
- Ensure any updated datasets or binary model weights are tracked using **DVC** (`dvc add <file>`) and push the changes to remote storage (`dvc push`). Never commit raw datasets or `.pkl` files directly to Git.
