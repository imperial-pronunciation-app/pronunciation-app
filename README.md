# Quick Start Guide

## Run Tests
```bash
make test
```

## Run Development Server
```bash
make dev
``` 


## Common Commands
### Run pre commit tests
```bash
pre-commit run --all
```

### Lints the entire project
```bash
ruff check . --fix
```

```bash
make down
```

### Seeding the database
```bash
docker exec -it <insert-docker-image-name> python3 -m app.seed
```





