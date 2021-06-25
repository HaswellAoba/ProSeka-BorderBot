import os
import sys
from typing_extensions import final
import config
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def draw_top_3(Top3Array, Old3Array, draw, name_dx, score_dx, dy, font, scrfont):
    seq_no = 1
    for list in Top3Array:
        score = list.get('score')
        for i in Old3Array:
            if i['rank'] == seq_no:
                changed = score - i['score']
                finalstring = format(score, ',') + 'pt' + ' (+' + format(changed, ',') + 'pt)'

        print('{0}위: {1} - {2}'.format(seq_no, list.get('userName'), finalstring))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx, dy), list.get('userName'), fill="black", font=font, align='center')
        draw.text((score_dx, dy), finalstring, fill="black", font=scrfont, align='center')
        seq_no += 1
        dy += 53
        if (seq_no == 4):
            print()
            return

def draw_general(json_data, json_old, rank, draw, name_dx, score_dx, dy, font, scrfont):
    rank_specify = rank
    seq_no = 0
    for i in json_data:
        if i['rank'] >= rank_specify:
            score = i.get('score')
            for j in json_old:
                if j['rank'] == rank_specify:
                    changed = score - j['score']
                    finalstring = format(score, ',') + 'pt' + ' (+' + format(changed, ',') + 'pt)'

            print('{0}위: {1} - {2}'.format(rank_specify, i.get('userName'), finalstring))
            print('Template에 순위를 작성합니다')
            draw.text((name_dx, dy), i.get('userName'), fill="black", font=font, align='center')
            draw.text((score_dx, dy), finalstring, fill="black", font=scrfont, align='center')
            dy += 49
            rank_specify += rank
            seq_no += 1
            if (seq_no == 5):
                print()
                return

def main(json_data, json_old):
    # Image Coordinate Setup
    name_dx = 181
    score_dx = 546
    dy = 379

    # Other Image Setups
    template_image = Image.open(os.path.join(sys.path[0], 'resources/frame_{0}.png').format(config.current_event_id))
    font = ImageFont.truetype(os.path.join(sys.path[0], 'resources/NotoSansCJKkr-Regular.otf'), 30)
    scrfont = ImageFont.truetype(os.path.join(sys.path[0], 'resources/NotoSansCJKkr-Medium.otf'), 30)
    draw = ImageDraw.Draw(template_image)
    rank = 100

    # Top 3
    print("Top 3")
    draw_top_3(json_data, json_old, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 10~50
    print("10~50위 포인트 리스트")
    dy = 555
    rank = 10
    draw_general(json_data, json_old, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 100~500
    print("100~500위 포인트 리스트")
    dy = 821
    rank = 100
    draw_general(json_data, json_old, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 1000~5000
    print("1000~5000위 포인트 리스트")
    name_dx = 1057
    score_dx = 1424
    dy = 369
    rank = 1000
    draw_general(json_data, json_old, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 10000~50000
    print("10000~50000위 포인트 리스트")
    dy=632
    rank = 10000
    draw_general(json_data, json_old, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Signing Today
    texttoday = datetime.today().strftime('%Y년 %m월 %d일 %H시 %M분 기준')
    draw.text((1437, 1007), texttoday, fill="black", font=font, align='center')

    # 완성된 파일 저장
    template_image.save(os.path.join(sys.path[0], 'border.png'))

    return
