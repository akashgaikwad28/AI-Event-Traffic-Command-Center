# FOUNDATION_SETUP_PROMPT.md

```md id="0ag6kr"
You are a senior staff-level backend/platform engineer.

Follow ALL rules defined in:
- AI_AGENT_RULES.md
- PROJECT_CONTEXT.md
- IMPLEMENTATION_ROADMAP.md

STRICT REQUIREMENTS:
- minimal code
- no unnecessary abstractions
- no duplicate files
- production-grade architecture
- maintainability first
- concise implementations
- no tutorial-style code
- use modern best practices
- use minimal tokens in code generation

TASK:
Implement the complete engineering foundation for this project.

PROJECT NAME:
GRIDWISE AI

TECH STACK:
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker
- Poetry
- Ruff
- Black
- MyPy
- Pre-commit

DO NOT implement business logic.
DO NOT implement AI models yet.
DO NOT implement frontend yet.

ONLY implement foundational engineering setup.

==================================================
PHASE 0.5 IMPLEMENTATION REQUIREMENTS
==================================================

IMPLEMENT THESE FILES:

ROOT:
- pyproject.toml
- .gitignore
- .env.example
- docker-compose.yml
- Makefile
- .pre-commit-config.yaml

CONFIGS:
- configs/settings.yaml
- configs/logging.yaml

REQUIREMENTS:
- requirements/base.txt
- requirements/dev.txt
- requirements/prod.txt

BACKEND CORE:
- backend/app/main.py
- backend/app/core/config.py
- backend/app/core/logger.py
- backend/app/core/middleware.py
- backend/app/core/constants.py

API:
- backend/app/api/router.py
- backend/app/api/v1/endpoints/health.py

UTILS:
- backend/app/utils/response.py

EXCEPTIONS:
- backend/app/exceptions/base.py
- backend/app/exceptions/handlers.py

==================================================
IMPLEMENTATION DETAILS
==================================================

1. pyproject.toml
Use Poetry.

Include:
- FastAPI
- uvicorn
- sqlalchemy
- asyncpg
- pydantic
- pydantic-settings
- python-dotenv
- structlog
- loguru
- redis
- pandas
- geopandas
- scikit-learn

Dev dependencies:
- black
- ruff
- mypy
- pytest
- pre-commit

Configure:
- black
- ruff
- mypy

Use clean modern configuration.

==================================================

2. .gitignore

Must include:
- python artifacts
- env files
- logs
- notebook checkpoints
- docker artifacts
- IDE files
- cache
- datasets except keep sample placeholders

==================================================

3. .env.example

Include:
- APP_NAME
- APP_ENV
- DEBUG
- API_V1_PREFIX
- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- REDIS_HOST
- REDIS_PORT
- LOG_LEVEL

Use safe example values.

==================================================

4. docker-compose.yml

Create minimal production-style setup.

Services:
- backend
- postgres
- redis

Backend should:
- mount source
- support hot reload

Use clean networking.

==================================================

5. Makefile

Include commands:
- install
- run
- lint
- format
- test
- migrate
- docker-up
- docker-down

Keep concise.

==================================================

6. .pre-commit-config.yaml

Configure:
- black
- ruff
- end-of-file-fixer
- trailing-whitespace

==================================================

7. configs/settings.yaml

Include:
- app settings
- logging settings
- API settings

Keep minimal.

==================================================

8. configs/logging.yaml

Implement structured logging config.

Support:
- console logging
- file logging

Minimal but production-grade.

==================================================

9. backend/app/main.py

Implement:
- FastAPI app
- lifespan handler
- middleware registration
- router registration

Add:
- health endpoint registration

NO business logic.

==================================================

10. backend/app/core/config.py

Implement:
- pydantic settings
- environment loading
- typed config object

Use singleton-style settings loader.

==================================================

11. backend/app/core/logger.py

Implement centralized structured logging.

Requirements:
- reusable logger
- request-safe
- production-grade formatting

NO print statements.

==================================================

12. backend/app/core/middleware.py

Implement:
- request timing middleware
- request logging middleware

Keep lightweight.

==================================================

13. backend/app/api/router.py

Implement:
- API router aggregation
- v1 router registration

==================================================

14. backend/app/api/v1/endpoints/health.py

Implement:
GET /health

Response:
{
  "status": "healthy"
}

==================================================

15. backend/app/utils/response.py

Implement standardized API response helper.

==================================================

16. backend/app/exceptions/base.py

Implement base custom exception.

==================================================

17. backend/app/exceptions/handlers.py

Implement:
- global exception handlers
- validation error handling
- internal error handling

==================================================

ADDITIONAL RULES
==================================================

- Use async FastAPI patterns.
- Use type hints everywhere.
- Keep implementations concise.
- Avoid unnecessary comments.
- Avoid placeholder code.
- Avoid giant files.
- Reuse utilities.
- No dead code.
- No duplicate config logic.
- No fake enterprise abstractions.

==================================================
EXPECTED FINAL RESULT
==================================================

After implementation:
- project should boot successfully
- docker-compose should run
- /health endpoint should work
- linting should work
- formatting should work
- pre-commit should work
- logging should work
- centralized config should work
- exception handling should work

Return:
1. Complete file implementations
2. Any required commands
3. Minimal setup instructions

Do NOT generate explanations unless necessary.
Focus on implementation quality.
```
