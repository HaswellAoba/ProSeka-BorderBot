import os
import time
import json
import requests
import PIL
from PIL import Image,ImageDraw,ImageFont

#Beginning
unixtime = int(time.time())
print("프로젝트 세카이 현재 이벤트 랭킹 파서")
print('로컬 JSON으로 테스트 중')
print('지금 UNIX 시간 : ' + str(unixtime))
print()

#Image Setup
template_image = Image.open('C:\\Users\\guswo\\desktop\\FRAME_SAMPLE.png')
fontsFolder = 'C:\\Users\\guswo\\desktop'
font = ImageFont.truetype(os.path.join(fontsFolder,'SeoulNamsanB.ttf'),24)
draw = ImageDraw.Draw(template_image)
name_dx = 92
score_dx = 382
dy = 305

#Load Local JSON File
with open('C:\\Users\\guswo\\Desktop\\event10.json', 'r', encoding="UTF-8") as f:
    json_data = json.load(f)

#Array
Top3Array = json_data.get('first10')
Top10Array = ''
Top100Array = ''
Top1000Array= ''
Top10000Array= ''

#Rank Top 3
print ("Top 3")
seq_no=1
for list in Top3Array:
    print('{0}위: {1} - {2}pt'.format(seq_no, list.get('name'), list.get('score')))
    print('Template에 순위를 작성합니다')
    draw.text((name_dx,(dy-seq_no)),list.get('name'),fill="black",font=font,align='center')
    draw.text((score_dx,(dy-seq_no)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    seq_no=seq_no+1
    dy=dy+38
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
        dy=dy+34

for i in range(1, 5):
    TempArray = json_data.get('rank{0}'.format(rank_specify))
    for list in TempArray:
        print('{0}위: {1} - {2}pt'.format(rank_specify, list.get('name'), list.get('score')))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx,(dy-i)),list.get('name'),fill="black",font=font,align='center')
        draw.text((score_dx,(dy-i)),str(list.get('score'))+"pt",fill="black",font=font,align='center')
    dy=dy+34
    rank_specify=rank_specify+10
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
    dy=dy+34
    rank_specify=rank_specify+100
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
    dy=dy+34
    rank_specify=rank_specify+1000
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
    dy=dy+34
    rank_specify=rank_specify+10000
print()


template_image.save("C:\\Users\\guswo\\desktop\\frame_sample_python.png")
