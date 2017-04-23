from pymongo import MongoClient
import pymongo
import time


HOST = '127.0.0.1'
PORT = 27017
DB = 'mapping'
COLLECTION = 'posts'
DYNAMIC_COLLECTION = 'posts_update'


def add_index_for_db(c_name, attr):

    client = MongoClient(HOST, PORT)
    db = client[DB]
    collection = db[c_name]
    collection.create_index(attr)

def generate_dynamic_collection(number):

    client = MongoClient(HOST, PORT)
    db = client[DB]
    source_collection = db[COLLECTION]
    dynamic_collection = db[DYNAMIC_COLLECTION]

    dynamic_collection.remove({})

    num = 0
    recent_arr = []

    for record in source_collection.find().sort('time_stamp', pymongo.DESCENDING):
        if num > number:
            break
        del record['_id']
        del record['map_data']
        recent_arr.append(record)
        num += 1

    recent_arr = sorted(recent_arr, key=lambda tup: tup['time_stamp'], reverse = False)
    last_time = 0
    current_arr = []
    for record in recent_arr:
        current_time = record['time_stamp']
        if last_time != current_time:
            last_time = current_time
            for cc in current_arr:
                dynamic_collection.insert(cc)
            current_arr = []

            print(record['time_stamp'])
        current_arr.append(record)
        time.sleep(1)


if __name__ == '__main__':
    # add_index_for_db(DYNAMIC_COLLECTION, 'time_stamp')
    # print('here')
    generate_dynamic_collection(10000)