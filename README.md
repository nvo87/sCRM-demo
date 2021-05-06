# sCRM

CRM for hockey sport-sections and clubs.

## Installation
### Frontend
To install frontend, check - frontend/README.md

### Backend
```
make rebuild
```
visit - http://127.0.0.1:8002/

## Tests

We are using Pytest and coverage. To run the test use

```
pytest
```

Add `-x` flag for stoping at the first error.
` -p no:warnings ` - to hide warnings.

To look at the tests coverage use

```
coverage run --source='.' manage.py pytest
coverage report
```

or

```
pytest --cov=<your_dir or .>
```
