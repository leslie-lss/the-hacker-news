# -*- coding:utf-8 -*-

import redis
from pymongo import MongoClient

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def get_id_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.thehackernews
    my_set = db.list_1106_1718
    for x in my_set.find():
        print(x['post_url'])
        r.rpush('url', x['post_url'])
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

if __name__ == '__main__':
    get_id_from_mongo()

print("success0")