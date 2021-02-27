'''
이것은 프로세카 보더봇의 변수를 설정하는 곳입니다.
여기서 지금 진행중인 이벤트 정보와 보더를 올릴 트위터 API 토큰을 입력합니다.

먼저 config_example.py 파일을 복제하여 config.py 파일을 만드십시오.
그런 다음 아래에 정보를 입력한 다음 봇을 시동하십시오.

날짜 형식은 YYYY-MM-DD HH:MM 형식이어야 합니다 (예: 2021-01-31 16:00).
'''

#Event Variable Setting
current_event_id='' #지금 진행중인 이벤트 ID
current_event_name = '' #지금 진행중인 이벤트 이름
event_start_date = '' #이벤트 시작하는 날짜
event_end_date = '' #이벤트 끝나는 날짜

#Twitter API Token
twtr_consumer_key = '' #Twitter Consumer Key
twtr_consumer_secret = '' #Twitter Consumer Secret
twtr_access_token = '' #Twitter Access Token
twtr_access_secret = '' #Twitter Access Secret