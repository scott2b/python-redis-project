# python-redis-project
Template for a new Python project with Redis

Until GitHub gives us [variables in templates](https://github.com/isaacs/github/issues/1716):

 - Change `redis_myproject` container name in `docker-compose.yml`
 - Change `src.myproject.mymodule` and relevant references in `tests`
 

## Quickstart

Important: See the [Redis](#redis) and [Redis Configuration](#redis-configuration)
sections below if you are already using Redis on your system.

**Note:** This project uses the [Redis stack](https://redis.io/docs/stack/) extensions
which are included in the provided docker-compose configuration.

If you just want regular Redis, change the image reference in `docker-compose.yml`

```
docker compose --profile redis up
```

Install requirements and run the tests:

```
pip install -r requirements-dev.txt
tox
```

See `tests/test_redis.py` for examples of using the Redis python client.


## Setup

### Redis

If you are already running Redis for other purposes, please see the
[Redis Configuration](#redis-configuration) section below. You may want to change the
port or the logical database number.


#### Run Redis via docker-compose

With [Docker](https://www.docker.com/) installed on your system:

```
docker-compose --profile redis up
```

If you prefer to install Redis on your system, see the
[Redis installation docs](https://redis.io/docs/getting-started/installation/)

See Redis Configuration below for more about setting up the databases.

#### Connect with redis-cli

Connect to the jobs database:

```
redis-cli
```

Defaults to logical database 0. To specify the database number:

```
redis-cli -n 0
```

#### Open Redis Insights

```
http://localhost:8001
```


## Redis Configuration

The default setup will work for most development scenarios. If you are already
running Redis on your system, you may want to modify the configurations, e.g. to
expose Redis for this project on a different port.

The following environment variables can be set (defaults are shown) and will set the
ports for exposing the redis-stack services to your system.

 - `REDIS_PORT=6379`
 - `REDISINSIGHT_PORT=8001`
