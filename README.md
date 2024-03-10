# DDD Cargo App
Implementation of the Cargo Shipping System described in "Domain Driven Design - Tackling Complexity in the Heart of Software" chapter 7.

## Run application
```bash
docker-compose build
docker-compose up
```

## Development

### Run tests
```bash
source ./venv/Scripts/activate
pip install -r requirements.txt
pytest
```

### Connect to mongo
```bash
docker exec -it ddd-cargo-app-mongodb-1 bash
mongo -u myuser -p mypass
use cargo_shipping
db.booking.find()
```

## Todo
- [x] pymongo
- [x] fast api
- [x] implement loading
- [x] implement unloading
- [] implement received (current location must equal delivery specification)
- [] error handling
- [] fix typing
- [] configure git pre-commit hooks, code quality and coverage
