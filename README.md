# sCRM [demo]

This repo is a demo version. The full project is the private repo.  
The goal of the project is to build an online CRM service for hockey clubs. Functional CRM will cover the needs of club owners for
training, attendance and income analysis. On the other hand, it will be an assistant to clients (players) in monitoring their activity and choosing available clubs.


## Technologies & Metodologies
- As a backend, I use Django and DjangoRestFramework to construct API.
- Authentication is configured via JWT with django-allauth and dj-rest-auth plugins.
- On the front I use Vue.js. It will consist of several mini-applications (multi-bundles).
They are bundled and rendered in Django using django-webpack-loader. 
- Django Templates are used only to render configured Vue.js apps.
- Component library is BootstrapVue.

Pylint, docker, makefile, coverage, git-pre-commit are configured.  
Pytest is used as the main test runner. And when it's convenient I prefer TDD.

I decompose the project into scopes, scopes - into features. All scopes, tasks and docs are in my Notion workspace.  
A separate feature is in a separate branch and is accepted through a pull request.  

- Commit naming according with [conventional commits].  
- Methods docstring according with [reStructuredText].  
- Russian doctrings and comments are permissible in code. 

- No logic in Views. Use Models or model helpers.  
- Keep DRY, KISS.  


## Installation
### Frontend
To install frontend, check - frontend/README.md

### Backend - Docker
```
make rebuild
```
visit - http://127.0.0.1:8002/  
database are working at 54321 port.

## Tests

We are using Pytest and coverage. To run the test use
```
make tests
```
To look at the tests coverage use
```
coverage run --source='.' manage.py pytest
coverage report
```
or
```
pytest --cov=<your_dir or .>
```

To make full check with tests and linting, use:
```
make precommit
```

[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/

[reStructuredText]: http://daouzli.com/blog/docstring.html
