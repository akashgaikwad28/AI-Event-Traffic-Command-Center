# AI_AGENT_RULES.md

````md id="p9z1vo"
# AI_AGENT_RULES.md

## Purpose

This project is an enterprise-grade AI Traffic Intelligence Platform built for:
- scalability
- maintainability
- modularity
- fast iteration
- hackathon execution speed
- production-style architecture

AI coding agents MUST follow these rules strictly.

Applies to:
- Claude Code
- Codex
- Cursor
- Antigravity
- Cline
- Windsurf
- Any autonomous coding agent

---

# CORE ENGINEERING PRINCIPLES

## 1. MINIMAL CODE

Always prefer:
- less code
- fewer abstractions
- smaller functions
- minimal boilerplate

DO NOT generate unnecessary enterprise complexity.

Avoid:
- overengineering
- premature optimization
- unnecessary design patterns
- useless wrappers
- deeply nested abstractions

---

## 2. NO DUPLICATION

Before creating:
- utility
- helper
- service
- schema
- model
- constant
- validation

ALWAYS search existing code first.

Never duplicate:
- logic
- configs
- response models
- DTOs
- enums
- validation rules
- transformation logic

Reuse existing modules.

---

## 3. FILE CREATION POLICY

DO NOT create new files unless absolutely necessary.

Before creating a file:
1. Check if functionality belongs in existing module
2. Reuse existing service/utils
3. Extend existing implementation

New files are allowed ONLY if:
- responsibility is clearly isolated
- module becomes too large
- separation improves maintainability

Avoid:
- helper.py explosion
- misc.py
- temp.py
- experimental.py
- duplicate service layers

---

# ARCHITECTURE RULES

## Backend Architecture

Strict layered architecture:

```txt
API → Services → Repositories → Database
                 ↓
                AI
                 ↓
              Analytics
````

Routes MUST NOT contain:

* business logic
* AI logic
* database queries

Routes should only:

* validate
* call service
* return response

---

## Service Layer

Business logic belongs ONLY in:

```txt
backend/app/services/
```

Services should:

* be stateless
* reusable
* testable
* composable

Avoid fat controllers.

---

## AI Layer

All ML/AI logic belongs ONLY in:

```txt
backend/app/ai/
```

Separate:

* training
* inference
* feature engineering
* evaluation

Never mix:

* API logic
* DB logic
* AI logic

---

## Utilities

Utilities must:

* remain pure
* have no side effects
* be generic

Allowed:

* geo calculations
* datetime transforms
* formatting
* validation

Forbidden:

* business logic
* database access

---

## Config Management

ALL configuration must come from:

* environment variables
* config.py
* settings.yaml

Never hardcode:

* API keys
* ports
* URLs
* secrets
* credentials

---

# LOGGING RULES

Use centralized structured logging only.

Use:

```python
logger.info()
logger.warning()
logger.error()
```

Never use:

```python
print()
```

Log only:

* important events
* failures
* inference timing
* API failures
* critical operations

Avoid excessive logs.

---

# EXCEPTION HANDLING

Use centralized exception handling.

Never expose raw exceptions to API clients.

All exceptions must:

* inherit from base exception
* return consistent response format
* include meaningful messages

Avoid:

* broad try/except
* silent failures
* swallowed exceptions

---

# DATABASE RULES

Use repository pattern.

Never query database directly inside:

* routes
* utilities
* AI modules

Database access allowed ONLY in:

```txt
repositories/
```

---

# FRONTEND RULES

Frontend must remain:

* component-driven
* modular
* reusable

Avoid:

* duplicated UI
* giant pages
* inline business logic

Keep:

* API calls in services/
* state centralized
* types reusable

---

# TOKEN OPTIMIZATION RULES

AI agents MUST minimize token usage.

Prefer:

* concise implementations
* reusable utilities
* existing libraries
* built-in framework features

Avoid:

* verbose comments
* unnecessary documentation
* giant generated examples
* repetitive code

DO NOT generate:

* placeholder code
* mock wrappers
* fake abstractions
* tutorial-style implementations

---

# IMPORT RULES

Avoid deep imports.

Prefer:

```python
from app.services.prediction_service import PredictionService
```

Avoid circular dependencies.

---

# FUNCTION RULES

Functions should:

* do one thing
* remain small
* be composable

Avoid:

* 300-line functions
* nested conditionals
* repeated transformations

Prefer early returns.

---

# NAMING RULES

Use consistent naming.

Examples:

* event_service.py
* congestion_model.py
* geo_utils.py

Avoid:

* helper_final.py
* utils2.py
* new_service.py
* temp_model.py

---

# TESTING RULES

Test:

* services
* AI pipelines
* analytics
* repositories

Avoid testing trivial code.

---

# PERFORMANCE RULES

Optimize for:

* clarity first
* maintainability second
* performance third

Do not prematurely optimize.

Use:

* vectorized operations
* batching
* async where appropriate

Avoid unnecessary loops.

---

# GEO RULES

Geospatial logic belongs ONLY in:

```txt
backend/app/geo/
```

Avoid duplicating:

* distance calculations
* coordinate transforms
* hotspot calculations

---

# STREAMING RULES

Websocket and streaming logic belongs ONLY in:

```txt
backend/app/stream/
```

Keep isolated from core business logic.

---

# CODE STYLE

Use:

* type hints
* pydantic schemas
* dataclasses where useful
* clean returns

Keep code:

* concise
* readable
* production-oriented

---

# WHAT AI AGENTS MUST NEVER DO

NEVER:

* create unnecessary files
* duplicate code
* create alternate implementations
* generate tutorial code
* add fake enterprise complexity
* generate dead code
* create unused abstractions
* introduce multiple patterns for same problem
* add comments explaining obvious code
* generate giant boilerplate

---

# PROJECT PRIORITY ORDER

Priority:

1. Simplicity
2. Maintainability
3. Reusability
4. Modularity
5. Performance
6. Scalability

---

# IDEAL ENGINEERING STYLE

Target style:

* Stripe
* Uber
* Linear
* Palantir
* FastAPI best practices

NOT:

* tutorial repositories
* beginner architecture
* overengineered Java-style patterns

---

# FINAL RULE

Every implementation must answer:

1. Is this the minimal clean solution?
2. Can existing code be reused?
3. Is a new file truly necessary?
4. Will this scale cleanly?
5. Is this production-quality?
6. Does this reduce future complexity?

If not:
REFACTOR SIMPLER.

```
```
