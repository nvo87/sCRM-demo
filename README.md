# sCRM

CRM for hockey sport-sections and clubs.

# Tests

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
