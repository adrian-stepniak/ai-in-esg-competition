from selenium import webdriver
import argparse


def get_data_from_reviews(review):
    date = review.find_element_by_css_selector('span.authorInfo').text
    score = review.find_element_by_css_selector('span.ratingNumber').text
    desc = review.find_element_by_css_selector('a.reviewLink').text
    pros = review.find_element_by_css_selector('span[data-test="pros"]').text
    cons = review.find_element_by_css_selector('span[data-test="cons"]').text

    return ';'.join((date, score, desc, pros, cons,))+'\n'


def get_reviews(company_url, output_file, geckodriver_path = 'geckodriver.exe', pages=10):
    company_url = company_url.replace('.htm', '')
    with webdriver.Firefox(executable_path=geckodriver_path) as driver:
        for page in range(1, pages):
            driver.get(f'{company_url}_P{page}.htm')
            reviews = driver.find_elements_by_css_selector('li.empReview')
            with open(output_file, 'a+', encoding='utf8') as output_file:
                for review in reviews:
                    data = get_data_from_reviews(review)
                    output_file.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper of the company reviews on glassdoor.com')
    parser.add_argument('file', type=str,
                        help='Path to the txt file with links to companies on glassdoor.com')
    parser.add_argument('--output_file', type=str, default='glassdoor_reviews.csv',
                        help='Name of the output file')

    parser.add_argument('--executable_path', type=str, default='geckodriver.exe',
                        help='path to firefox selenium driver')

    args = parser.parse_args()

    with open(args.file, 'r+', encoding='utf8') as input_file:
        company_urls = input_file.readlines()

    for company_url in company_urls:
        get_reviews(company_url, args.output_file, geckodriver_path=args.executable_path)