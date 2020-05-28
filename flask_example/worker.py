# coding:utf-8
import os
import redis
from rq import Connection, Worker, Queue

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# returns an active Redis client
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker([Queue('default')])
        worker.work()