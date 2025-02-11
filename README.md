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

### If make dev throws a "something is running on port 5432" error
```bash
lsof -i :5432
```

### Kill the process
```bask
kill -9 <PID>
```

### Docker commands to get docker image
```bash
docker ps
```

### Seeding the database
```bash
docker exec -it <insert-docker-image-name> python3 -m app.seed
```





