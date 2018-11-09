from pymongo import MongoClient

def get_url():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.thehackernews
    my_set = db.list_1106_1718
    article_set = db.article_1106_1757
    for x in my_set.find():
        print("------------------------------------------------------------------------------------------------")
        if article_set.find({'url':x['post_url']}).count() == 0:
            save_mongo(x)

def save_mongo(dict):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.thehackernews
    my_set = db.last_list_1107_0910
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')


if __name__ == '__main__':
    get_url()