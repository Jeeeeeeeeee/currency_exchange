# Docker Configuration

1. Install docker + docker compose depending from OS
  - Docker Installation Manuals: https://docs.docker.com/install/
  - Docker Compose Installation Manuals: https://docs.docker.com/compose/install/

2. Open command line and change current folder to folder where `docker-compose.yml` is located and run next commands:

```bash
docker volume create --name=edu-mongo-data
docker volume create --name=edu-postgre-data
docker-compose up -d
```

**CAUTIONS**
If everything previously installed then run next commands to restart docker containers

```bash
docker-compose stop
docker-compose up -d
```

# Install required modules

Open command line and change current folder to folder where `requirements.txt` is located and run next commands:

```bash
pip install -r requirements.txt
```

**CAUTIONS**
1. If you use virtual environment then you need to activate it by `source PATH/TO/VENV/bin/activate`
2. If you use python from hosted machine then use a proper `pip` version.


# Check installation

1. Run docker containers

```bash
docker-compose up -d
```

2. Run `installation_checker.py` script

```bash
python installation_checker.py
```

If configuration was properly done then you will see a log with all OK.

If there were an errors then log will contain records with errors.
