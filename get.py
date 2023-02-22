import requests
import os
import json
import time
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = ""
start_time1='2022-02-22T00:00:00Z'

def create_url(user_id,next_token=''):
    # Replace with user ID below
    url= "https://api.twitter.com/2/users/{}/tweets?".format(user_id)

    return url

def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    query_params = {"max_results":100,'start_time':start_time1,
                 "tweet.fields": "author_id,context_annotations,conversation_id,created_at,entities,id,in_reply_to_user_id,referenced_tweets,lang,public_metrics,text,geo,source,withheld",
                 "exclude":"retweets,replies",
                
                }
    return query_params


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):

    # proxies = {'https':'http://127.0.0.1:1080'}
    #if proxies is needed ,add para in the following line
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_one(user_id,):
    token=''
    flag=1
    all_tweets=0
    while(flag):
        url = create_url(user_id,next_token=token)
        params = get_params()
        if token:
            params['pagination_token']=token
        json_response = connect_to_endpoint(url, params)
        response=json_response
        try:
            tdata = response['data']
            tmeta=response['meta']
        except: 
            print('No data')
            break
        with open ('./data/'+str(user_id)+'.txt','a+',encoding='utf-8') as f:
            for item in tdata:
                temp = json.dumps(item)
                f.write(temp+'\n')
            if ("next_token" in tmeta) and (all_tweets <3000):
                token =  tmeta["next_token"]
                print('ready for the next GET ,all='  +str(all_tweets))
                time.sleep(2)
                all_tweets += 100
            else:
                flag = 0        

if __name__ == "__main__":
    #you can search more than one user each time
    with open('./IDS.txt') as f:
        user_id=f.readlines()
    for i in user_id:
        i=i[:-1]
        get_one(i)
