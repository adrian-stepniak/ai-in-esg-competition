from typing import Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import csv
from time import sleep


def select_inner_text(object: Tag, selector: str) -> str:
    selection = object.select_one(selector)
    selection = selection.text if selection else ''
    selection = selection.replace('\n', '').replace('\r', '')
    return selection


def scrap_review(review: Tag) -> Tuple[str, str, str, str, str, str]:
    title = select_inner_text(review, 'a.cmp-Review-titleLink')
    score = select_inner_text(review, 'button.cmp-ReviewRating-text')
    author_and_date = select_inner_text(review, 'span.cmp-ReviewAuthor')
    description = select_inner_text(review, 'span.cmp-NewLineToBr-text')
    pros = select_inner_text(review, 'div.cmp-ReviewProsCons-prosText')
    cons = select_inner_text(review, 'div.cmp-ReviewProsCons-consText')

    return score, title, author_and_date, description, pros, cons,


#
# base_url = 'https://indeed.com/cmp/Nissan/reviews?fcountry=ALL&lang=en&start='
#

def get_company_reviews(company_url, last_year=2019, output_file='reviews.csv', sleep_time=0.1):
    reviews_url = company_url + '?fcountry=ALL&lang=en&start='
    i = 0
    last_review_date = 2022
    while True:
        page = requests.get(reviews_url + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        reviews = soup.select('div.cmp-Review')
        if len(reviews) > 0:
            reviews.pop()  # drop first reviews as it is always same recommended review
            scraped_reviews = [scrap_review(review) for review in reviews]
            with open(output_file, 'a', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(scraped_reviews)

            last_review_date = int(scraped_reviews[-1][2][-4:])
        if last_review_date < last_year:
            break
        else:
            i += 20  # indeed.com has 20 reviews per page
            print(f'Exctracted {i} reviews')
            sleep(sleep_time)


companies = [
    'https://pl.indeed.com/cmp/Honda/reviews',
    'https://pl.indeed.com/cmp/Tata-Consultancy-Services-(tcs)/reviews',
    'https://pl.indeed.com/cmp/Toyota/reviews',
    'https://pl.indeed.com/cmp/Mitsubishi/reviews',
    'https://pl.indeed.com/cmp/Faurecia/reviews',
    'https://pl.indeed.com/cmp/Mahindra-&-Mahindra-Ltd/reviews'
]

for company_url in companies:
    company_name = company_url.split('/')[-2][:16]
    get_company_reviews(company_url, output_file=f'{company_name}_reviews.csv')