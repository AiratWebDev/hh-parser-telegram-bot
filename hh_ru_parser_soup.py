from bs4 import BeautifulSoup
import requests
from headers import browser_headers


def soup_vacancy_seek(url):
    req = requests.get(url, headers=browser_headers)

    soup = BeautifulSoup(req.text, 'lxml')

    vacancies_dict = {}
    vac_links = soup.find_all('a', {"data-qa": "serp-item__title"})

    for link in vac_links:
        link = link.get('href')
        req = requests.get(link, headers=browser_headers)
        soup = BeautifulSoup(req.text, 'lxml')

        header = soup.find('h1', {"data-qa": "vacancy-title"}).text
        salary = soup.find('span', class_="bloko-header-section-2 bloko-header-section-2_lite").text

        company = soup.find('span', class_="vacancy-company-name").text
        try:
            city = soup.find('p', {"data-qa": "vacancy-view-location"}).text
        except AttributeError:
            city = soup.find('span', {"data-qa": "vacancy-view-raw-address"}).text
        info1 = soup.find('div', class_='bloko-gap bloko-gap_bottom').find_next().text
        info2 = soup.find('div', {"data-qa": "vacancy-description"}).text
        """
        Заголовок, Зарплата, Фирма, Город, Текст, Ссылка
        """
        vacancies_dict[header] = [salary, company, city, info1, info2, link]

    return vacancies_dict
