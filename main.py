import os
import sys
import time
import json
import tweepy
import requests
import config
import initial_functions
import main_functions
from datetime import datetime

def download_data(dataurl):
    time.sleep(5)
    response = requests.get(dataurl)
    response.encoding = 'utf-8'
    resp_data = response.content
    print('data.json 파일에 기록합니다...')
    j = json.loads(resp_data)
    open(os.path.join(sys.path[0], 'resources/data.json'), 'w').write(json.dumps(j, sort_keys=True, indent=4, ensure_ascii=False))

def tweet(message, image):
    print('트윗으로 작성합니다, 조금만 기다려 주십시오...')
    auth = tweepy.OAuthHandler(config.twtr_consumer_key, config.twtr_consumer_secret)
    auth.set_access_token(config.twtr_access_token, config.twtr_access_secret)
    api = tweepy.API(auth)
    media_ids = []
    borderimg = api.media_upload(os.path.join(sys.path[0], image+'.png'))
    media_ids.append(borderimg.media_id)
    print(('미디어 업로드 OK : {0}').format(media_ids))
    api.update_status(status=message, media_ids=media_ids)
    print('Tweet OK')

def main(status):
    #Variables
    dataurl = 'https://bitbucket.org/sekai-world/sekai-event-track/raw/main/event{0}.json'.format(config.current_event_id)
    message = '이벤트 "{0}" 순위 경계 정보입니다. (기준시간 {1})'.format(config.current_event_name, today)
    if (status==1):
        message = '이벤트 "{0}" 에 대한 마지막 경계 정보입니다.'.format(config.current_event_name)

    print('\n랭킹 데이터 다운로드')
    download_data(dataurl)

    #Load Local JSON File
    with open(os.path.join(sys.path[0], 'resources/data.json'), 'r', encoding="UTF-8") as f:
        json_data = json.load(f)
        json_data = json_data.get('data').get('eventRankings')
 
    #Trying with older data json
    try:
        with open(os.path.join(sys.path[0], 'resources/data_old.json'), 'r', encoding="UTF-8") as f:
            json_old = json.load(f)
            json_old = json_old.get('data').get('eventRankings')
            is_initial = 0
    except FileNotFoundError:
        print('구 데이터가 아직 없습니다.')
        is_initial = 1

    #Data Download to Frame
    if (is_initial==1):
        initial_functions.main(json_data)
    else:
        main_functions.main(json_data, json_old)

    #Tweet
    tweet(message, 'border')

    #Move current file to legacy
    try:
        os.rename(os.path.join(sys.path[0], 'resources/data.json'), os.path.join(sys.path[0], 'resources/data_old.json'))
    except FileExistsError:
        os.remove(os.path.join(sys.path[0], 'resources/data_old.json'))
        os.rename(os.path.join(sys.path[0], 'resources/data.json'), os.path.join(sys.path[0], 'resources/data_old.json'))

    print("완료됨")
    return

global today
today = datetime.today().strftime('%Y-%m-%d %H:%M')
print('프로젝트 세카이 현재 이벤트 랭킹 파서')
if (today < config.event_start_date):
    print("[경고] 아직 이벤트가 시작하지 않았습니다. 파싱을 하지 않습니다.")
elif (today > config.event_start_date and today < config.event_end_date):
    print('현재 이벤트 진행 중')
    main(0)
elif (today == config.event_end_date):
    print('이벤트 종료!')
    main(1)
else:
    print('[경고] 만료된 이벤트에 대해 시도하고 있습니다. 파싱을 하지 않습니다.')