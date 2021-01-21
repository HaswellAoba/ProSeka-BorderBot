import os
import sys
import json
import tweepy
import requests
import PIL
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime

#Variable Setting
current_event_id='11' #지금 진행중인 이벤트 ID
current_event_name = 'Colour of Myself !' #지금 진행중인 이벤트 이름

today = datetime.today().strftime('%Y-%m-%d %H:%M')
dataurl = 'https://bitbucket.org/sekai-world/sekai-event-track/raw/main/event{0}.json'.format(current_event_id)
template_image = Image.open(os.path.join(sys.path[0], 'frame_{0}.png').format(current_event_id))
font = ImageFont.truetype(os.path.join(sys.path[0], 'SeoulNamsanB.ttf'),24)
message = '이벤트 "{0}" 순위 경계 정보입니다. (기준시간 {1})'.format(current_event_name, today)
tokens = {'consumer_key': '', 'consumer_secret': '', 'access_token': '', 'access_token_secret': ''}

#Read token from txt
seq_no=0
with open(os.path.join(sys.path[0], 'token.txt')) as f:
   for line in f:
        tokens[seq_no] = line.rstrip('\n')
        seq_no+=1

#Twitter Status Update Setup
auth = tweepy.OAuthHandler(tokens[0], tokens[1])
auth.set_access_token(tokens[2], tokens[3])
api = tweepy.API(auth)

#Image Setup
draw = ImageDraw.Draw(template_image)
name_dx = 92
score_dx = 382
dy = 305

#Get Current Ranking Data
print("프로젝트 세카이 현재 이벤트 랭킹 파서")
print()
print('랭킹 데이터 요청')
response = requests.get(dataurl)
print('data.json 파일에 기록합니다...')
open(os.path.join(sys.path[0], 'data.json'), 'wb').write(response.content)

#Load Local JSON File
with open(os.path.join(sys.path[0], 'data.json'), 'r', encoding="UTF-8") as f:
    json_data = json.load(f)

#Array
Top3Array = json_data.get('first10')
Top10Array = ''
Top100Array = ''
Top1000Array= ''
Top10000Array= ''

#Prompt
print('준비 완료')
print()

#Rank Top 3
print ("Top 3")
seq_no=1
for list in Top3Array:
    print('{0}위: {1} - {2}pt'.format(seq_no, list.get('name'), list.get('score')))
    print('Template에 순위를 작성합니다')
    draw.text((name_dx,(dy-seq_no)),list.get('name'),fill="black",font=font,align='center')
    draw.text((score_dx,(dy-seq_no)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    seq_no+=1
    dy+=38
    if(seq_no==4):
        break
print()

#Rank 10~50
print ("10~50위 포인트 리스트")
rank_specify=20
dy=445
#Specificy for Rank 10
for i in Top3Array:
    if i['rank'] == 10:
        print('10위: {0} - {1}pt'.format(i['name'], i['score']))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx,(dy-1)),i['name'],fill="black",font=font,align='center')
        draw.text((score_dx,(dy-1)),str(i['score'])+"pt",fill="black",font=font,align='center')
        dy+=34

for i in range(1, 5):
    TempArray = json_data.get('rank{0}'.format(rank_specify))
    for list in TempArray:
        print('{0}위: {1} - {2}pt'.format(rank_specify, list.get('name'), list.get('score')))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx,(dy-i)),list.get('name'),fill="black",font=font,align='center')
        draw.text((score_dx,(dy-i)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    dy+=34
    rank_specify+=10
print()

#Rank 100~500
print("100~500위 포인트 리스트")
rank_specify=100
dy=640
for i in range(1, 6):
    TempArray = json_data.get('rank{0}'.format(rank_specify))
    for list in TempArray:
        print('{0}위: {1} - {2}pt'.format(rank_specify, list.get('name'), list.get('score')))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx,(dy-i)),list.get('name'),fill="black",font=font,align='center')
        draw.text((score_dx,(dy-i)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    dy+=34
    rank_specify+=100
print()

#Rank 1000~5000
print("1000~5000위 포인트 리스트")
rank_specify=1000
dy=834
for i in range(1, 6):
    TempArray = json_data.get('rank{0}'.format(rank_specify))
    for list in TempArray:
        print('{0}위: {1} - {2}pt'.format(rank_specify, list.get('name'), list.get('score')))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx,(dy-i)),list.get('name'),fill="black",font=font,align='center')
        draw.text((score_dx,(dy-i)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    dy+=34
    rank_specify+=1000
print()

#Rank 10000~50000
print("10000~50000위 포인트 리스트")
dy=1019
rank_specify=10000
for i in range(1, 6):
    TempArray = json_data.get('rank{0}'.format(rank_specify))
    for list in TempArray:
        print('{0}위: {1} - {2}pt'.format(rank_specify, list.get('name'), list.get('score')))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx,(dy-i)),list.get('name'),fill="black",font=font,align='center')
        draw.text((score_dx,(dy-i)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    dy+=34
    rank_specify+=10000
print()

#완성된 파일 저장
template_image.save(os.path.join(sys.path[0], 'border.png'))

#트윗
print('트윗으로 작성합니다, 조금만 기다려 주십시오...')
media_ids = []
borderimg = api.media_upload(os.path.join(sys.path[0], 'border.png'))
media_ids.append(borderimg.media_id)
print(('미디어 업로드 OK : {0}').format(media_ids))
api.update_status(status=message, media_ids=media_ids)
print('Tweet OK')
