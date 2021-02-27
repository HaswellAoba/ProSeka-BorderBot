import os
import sys
import config
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def draw_top_3(Top3Array, draw, name_dx, score_dx, dy, font, scrfont):
    seq_no = 1
    for list in Top3Array:
        score = format(list.get('score'), ',')
        print('{0}위: {1} - {2}pt'.format(seq_no, list.get('name'), score))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx, dy), list.get('name'), fill="black", font=font, align='center')
        draw.text((score_dx, dy), score+"pt", fill="black", font=scrfont, align='center')
        seq_no += 1
        dy += 53
        if (seq_no == 4):
            return
    print()
    return

def draw_top_10(Top3Array, json_data, draw, name_dx, score_dx, dy, font, scrfont):
    rank_specify = 20
    # Specificy for Rank 10
    for i in Top3Array:
        if i['rank'] == 10:
            score = format(i['score'], ',')
            print('10위: {0} - {1}pt'.format(i['name'], score))
            print('Template에 순위를 작성합니다')
            draw.text((name_dx, (dy - 1)), i['name'], fill="black", font=font, align='center')
            draw.text((score_dx, (dy - 1)), score+"pt", fill="black", font=scrfont, align='center')
            dy += 49

    for i in range(1, 5):
        TempArray = json_data.get('rank{0}'.format(rank_specify))
        for list in TempArray:
            score = format(list.get('score'), ',')

        print('{0}위: {1} - {2}'.format(rank_specify, list.get('name'), score))
        print('Template에 순위를 작성합니다')
        draw.text((name_dx, dy), list.get('name'), fill="black", font=font, align='center')
        draw.text((score_dx, dy), score+"pt", fill="black", font=scrfont, align='center')
        dy += 49
        rank_specify += 10
    print()
    return


def draw_general(json_data, rank, draw, name_dx, score_dx, dy, font, scrfont):
    rank_specify = rank
    for i in range(1, 6):
        TempArray = json_data.get('rank{0}'.format(rank_specify))
        for list in TempArray:
            score = format(list.get('score'), ',')
            print('{0}위: {1} - {2}'.format(rank_specify, list.get('name'), score))
            print('Template에 순위를 작성합니다')
            draw.text((name_dx, dy), list.get('name'), fill="black", font=font, align='center')
            draw.text((score_dx, dy), score+"pt", fill="black", font=scrfont, align='center')
        dy += 49
        rank_specify += rank
    print()
    return


def main(json_data):
    # Image Coordinate Setup
    name_dx = 181
    score_dx = 546
    dy = 379

    # Other Image Setups
    template_image = Image.open(os.path.join(sys.path[0], 'resources/frame_{0}.png').format(config.current_event_id))
    font = ImageFont.truetype(os.path.join(sys.path[0], 'resources/NotoSansCJKkr-Regular.otf'), 30)
    scrfont = ImageFont.truetype(os.path.join(sys.path[0], 'resources/NotoSansCJKkr-Medium.otf'), 30)
    draw = ImageDraw.Draw(template_image)
    Top3Array = json_data.get('first10')
    rank = 100

    # Top 3
    print("Top 3")
    draw_top_3(Top3Array, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 10~50
    print("10~50위 포인트 리스트")
    dy = 555
    draw_top_10(Top3Array, json_data, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 100~500
    print("100~500위 포인트 리스트")
    dy = 821
    draw_general(json_data, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 1000~5000
    print("1000~5000위 포인트 리스트")
    name_dx = 1057
    score_dx = 1424
    dy = 369
    rank = 1000
    draw_general(json_data, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Rank 10000~50000
    print("10000~50000위 포인트 리스트")
    dy=632
    rank = 10000
    draw_general(json_data, rank, draw, name_dx, score_dx, dy, font, scrfont)

    # Signing Today
    texttoday = datetime.today().strftime('%Y년 %m월 %d일 %H시 %M분 기준')
    draw.text((1437, 1007), texttoday, fill="black", font=font, align='center')

    # 완성된 파일 저장
    template_image.save(os.path.join(sys.path[0], 'border.png'))

    return
