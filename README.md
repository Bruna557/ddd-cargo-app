# DDD Cargo App
Implementation of the Cargo Shipping System described in "Domain Driven Design - Tackling Complexity in the Heart of Software" chapter 7.

## Code Quality

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7cfb5f6a05814a8890430aa724bd313f)](https://app.codacy.com/gh/Bruna557/ddd-cargo-app/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7cfb5f6a05814a8890430aa724bd313f)](https://app.codacy.com/gh/Bruna557/ddd-cargo-app/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)


## Run Application

```bash
docker compose up --build
```

## Development

### Run Tests

```bash
source ./venv/Scripts/activate
pip install -r requirements.txt
pytest
```

### Connect to MongoDB

```bash
docker exec -it ddd-cargo-app-mongodb-1 bash
mongo -u myuser -p mypass
use cargo_shipping
db.booking.find()
```

## Todo

- [ ] error handling
- [ ] fix typing
- [ ] configure github actions, code quality and coverage
- [ ] open api
