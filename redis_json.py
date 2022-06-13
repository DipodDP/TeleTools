import json

import redis
from config import load_config
from sessions.pyroredis import RedisJSON

config = load_config(".env")

endpoint = config.redis_endpoint
password = config.redis_pass


redis_connection = redis.Redis(
    host=endpoint.split(':')[0],
    port=int(endpoint.split(':')[1]),
    password=password.strip()
)


def get_redis_json(file_name: str):
    json_file = RedisJSON(config.bot_name, file_name, redis_connection).json

    if json_file is None:

        with open(file_name, encoding='utf-8') as f:
            json_file = json.load(f)
            RedisJSON(config.bot_name, file_name, redis_connection).set_json(json_file)

    return json_file


def del_redis_json(file_name: str):
    RedisJSON(config.bot_name, file_name, redis_connection).delete()


s = get_redis_json('example.json')
print(s)

# uncomment for delete file from redis
# del_redis_json('example.json')
