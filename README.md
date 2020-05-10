# qihoo360-problem


## Install

1. install python3, redis
2. pip3 install redis, tornado

## Run
1. python main.py

## Apis

root_url: `http://localhost:8888`
method: get/post
body: json encoded string
api_url: different apis

Recommend to use curl or postman to call apis
url = ${root_url}/${api_url}

#### User Profile

add user:
* api_url: `api/feed/add_user_data`
* body: `{"uid":"10001","name":"zdking01","icon":"http://fs.test.com/001.jpg"}`
* responce: null

get_user:
* api_url: `api/feed/get_user_data`
* body: `{"uid":"10001"}`
* responce: `{"uid":"10001","name":"zdking01","icon":"http://fs.test.com/001.jpg"}`

delete_user:
* api_url: `api/feed/delete_user_data`
* body: `{"uid":"10001"}`
* responce: null

#### Feed

follow:
* api_url: `api/feed/follow`
* body: `{"uid":"10001","follow_uid":"10002"} // 10001 follows 10002
* responce: 404 if uid/follow_uid not exists. 200 if success

unfollow: `api/feed/unfollow`
* body: `{"uid":"10001","follow_uid":"10002"} // 10001 follows 10002
* responce: 404 if uid/follow_uid not exists. 200 if success

**get feed timeline**:
* api_url: `api/feed/get_feed`
* body: `{"uid":"10001","cursor":null}`
* responce: {`timeline`: timelines, `new_cursor`: cursor}`

for callers, cursor = null for first fetch, otherwise cursor should be new_cursor in last responce. 
if all timelines returned and no need to next call, cursor in responce will be null.  

Each timeline has format like this:
```
{
    "profile": {
        "uid":"10002", 
        "name":"zdking02", 
        "icon": "http://fs.test.com/002.jpg"
    },
    "feed": {
        "feed_id": "10002.qWqxg0Moew89snLa", 
        "timestamp": 1589084823744, 
        "type": "push_commits", 
        "uid": "10002", 
        "data": feed_data
    }
]
```



