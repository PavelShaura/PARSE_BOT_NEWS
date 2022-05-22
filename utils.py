import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_first_news():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05) '
    }
    url = 'https://www.gazeta.ru/tech/'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    article_card = soup.find_all('div', class_='row')

    news_dict = {}

    for article in article_card:
        article_title = article.find('div', class_='b_ear-title').text.strip()
        article_intro = article.find('div', class_='b_ear-intro').text.strip()
        article_url_in = article.find('a', class_='b_ear-image').get('href')
        article_url = f'https://www.gazeta.ru{article_url_in}'

        article_date_timestamp = article.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(article_date_timestamp)
        date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
        article_date_time = time.mktime(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())

        article_id = article_url.split('/')[-1]
        article_id = article_id[:-6]

        # print(f'{article_title}\n{article_intro}\n{article_url}\n{article_date_time}\n{article_id}')

        news_dict[article_id] = {
            'article_date_time': article_date_time,
            'article_title': article_title,
            'article_url': article_url,
            'article_intro': article_intro,
        }
    with open('news_dict.json', 'w', encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05) '
    }
    url = 'https://www.gazeta.ru/tech/'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    article_cards = soup.find_all('div', class_='row')

    fresh_news = {}

    for article in article_cards:
        article_url_in = article.find('a', class_='b_ear-image').get('href')
        article_url = f'https://www.gazeta.ru{article_url_in}'
        article_id = article_url.split('/')[-1]
        article_id = article_id[:-6]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find('div', class_='b_ear-title').text.strip()
            article_intro = article.find('div', class_='b_ear-intro').text.strip()

            article_date_timestamp = article.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(article_date_timestamp)
            date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
            article_date_time = time.mktime(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())

            news_dict[article_id] = {

                'article_title': article_title,
                'article_url': article_url,
                'article_intro': article_intro,
            }
            fresh_news[article_id] = {
                'article_date_time': article_date_time,
                'article_title': article_title,
                'article_url': article_url,
                'article_intro': article_intro,
            }
    with open('news_dict.json', 'w', encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    get_first_news()
    check_news_update()


if __name__ == '__main__':
    main()
