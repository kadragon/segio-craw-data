import requests
import csv
from fake_useragent import UserAgent
import time
import random
import math
from filedown import download_file_with_url_filename


ua = UserAgent()


def get_view(url):
    wait_time = random.uniform(2, 3)
    print(f'\n대기중... {math.floor(wait_time * 1000)}ms')
    time.sleep(wait_time)

    headers = {
        "User-Agent": ua.random  # 랜덤 User-Agent 설정
    }

    site_name = url.split("https://")[1].split(".")[0]

    try:
        response = requests.get(url, headers=headers)
        html_content = response.text
        print(
            f"loading... / {url} / User-Agent: {headers['User-Agent'].split(';')[0]}")
    except:
        return False

    cut_content = html_content.split(
        'var Posts=')[1].split('_post_list(Posts)')[0]

    list_content = cut_content.split('[[[')

    if len(list_content) < 3:
        return False

    print(
        f"parsing... / 게시물 개수: {len(list_content)-2}")

    for content in list_content[2:]:
        # print(content)
        print()
        uid = content.split(',')[0]
        view = content.split("],[")[-1].split("],")[1].split(",")[0]
        mainText = content.split('],')[1].split(',"')[3]
        attach = content.split(', "/notice.brd/')

        # write_csv(site_name, uid, view)
        print(site_name, uid, view, mainText)

        sub_url = '/'.join(url.split("/")[:-1])

        for a in attach[1:]:
            print("----------")
            split_a = a.split('",')
            file_url = f"{sub_url}/{split_a[0]}"
            file_status = split_a[2].replace(
                '["', '') + ' ' + split_a[3].replace('"', '')
            file_down = split_a[4].split(",")[1].replace('[', '')

            print(file_url, file_status, file_down)
            download_file_with_url_filename(file_url)

    return True


def write_csv(site, uid, view):
    with open(f'scraped_data_{site}.csv', mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([site, uid, view])


# 웹 페이지 URL
homepage_id = 'cedu'
board_id = 'notice'

i = 1

while True:
    url = f"https://{homepage_id}.knue.ac.kr/{board_id}.brd/0{i}"
    if not get_view(url):
        break

    i += 1
