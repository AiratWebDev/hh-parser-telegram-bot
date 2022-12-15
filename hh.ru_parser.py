import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import hh_ru_parser_soup
from key import bot_key
from webdriver_manager.chrome import ChromeDriverManager # для автоапдейта версии движка хрома

hh_bot = telebot.TeleBot(bot_key)
option = webdriver.ChromeOptions()
option.add_argument('headless')


@hh_bot.message_handler(commands=['start'])
def start(message):
    msg = hh_bot.send_message(message.chat.id, text='Укажите желаемую вакансию')
    hh_bot.register_next_step_handler(msg, seek_job)


def seek_job(message):
    hh_bot.send_message(message.chat.id, text='Немного подождите')
    driver_hh = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver_hh.get('https://izhevsk.hh.ru/')

    search = driver_hh.find_element(By.XPATH,
                                    value='/html/body/div[5]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/form/div/div[1]/fieldset/input')

    search.send_keys(f'{message.text}')
    search.send_keys(Keys.ENTER)

    page_url = driver_hh.current_url
    _dict = hh_ru_parser_soup.soup_vacancy_seek(page_url)
    """
    Заголовок, Зарплата, Фирма, Город, Текст, Ссылка
    vacancies_dict[header] = [salary, company, city, info1, info2, link]
    в цикле перебирается словарь из списков с информацией о конкретной вакансии
    """
    for i in range(5):
        hh_bot.send_message(message.chat.id,
                            text=f'<b>{list(_dict.keys())[i]}\n{list(_dict.values())[i][0]}</b>\n{list(_dict.values())[i][1]} \n\n{list(_dict.values())[i][4]} \n\n{list(_dict.values())[i][5]}',
                            parse_mode='html')

    driver_hh.quit()


hh_bot.polling()
