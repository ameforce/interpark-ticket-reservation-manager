from libs.selechecker import selechecker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import datetime
import time


def log(log_level: str, content: str):
    print(f'[{datetime.datetime.now()}] {log_level}: {content}')
    return


def get_element_by_xpath(driver: webdriver.Chrome, xpath_content: str):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath_content))
    )
    return element


def is_exist_seat_data(driver: webdriver.Chrome) -> bool and webdriver:
    element = get_element_by_xpath(driver, '/html/body/form[1]/div/div[1]/div[3]/div/'
                                           'div[1]/div/div/div/div/table/tbody/tr[2]/td[1]/div/span[2]')
    vip_seat_data = element.text
    vip_seat_data = vip_seat_data.replace('VIP석 ', '').replace('석', '')
    if vip_seat_data != '0':
        return True, element

    element = get_element_by_xpath(driver, '/html/body/form[1]/div/div[1]/div[3]/div/'
                                           'div[1]/div/div/div/div/table/tbody/tr[4]/td[1]/div/span[2]')
    r_seat_data = element.text
    r_seat_data = r_seat_data.replace('R석 ', '').replace('석', '')
    if r_seat_data != '0':
        return True, element
    return False, element


def seat_acquisition_logic(driver: webdriver.Chrome):
    seat_resource = is_exist_seat_data(driver)
    while not seat_resource[0]:
        driver.execute_script('javascript:fnRefresh()')
        random_time = random.uniform(0, 2.5)
        log('INFO', f'Waiting for {random_time}')
        time.sleep(random_time)
    log('INFO', f'Found the Seat !!!')
    seat_resource[1].click()


def init_reservation_page(driver: webdriver.Chrome):
    while len(driver.window_handles) == 1:
        time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.frame(driver.find_element(By.ID, 'ifrmSeat'))
    driver.execute_script('javascript:fnCheckOK()')


def date_selection_logic(driver: webdriver.Chrome):
    get_element_by_xpath(driver, '//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[3]/li[22]').click()
    driver.implicitly_wait(5)
    time.sleep(2)
    get_element_by_xpath(driver, '//*[@id="productSide"]/div/div[2]/a[1]/span').click()


def login_logic(driver: webdriver.Chrome, interpark_id: str, interpark_pw: str):
    get_element_by_xpath(driver, '//*[@id="userId"]').send_keys(interpark_id)
    get_element_by_xpath(driver, '//*[@id="userPwd"]').send_keys(interpark_pw)
    get_element_by_xpath(driver, '//*[@id="btn_login"]').click()


def init_variable() -> str and str and webdriver.Chrome:
    interpark_id = 'ameforce01'
    interpark_pw = '@Dlsvp2tmxm'
    url = 'https://ticket.interpark.com/Gate/TPLogin.asp?GPage=https%3A%2F%2Ftickets.interpark.com%2Fgoods%2F23005010'
    driver = webdriver.Chrome(executable_path=selechecker.driver_check())
    driver.get(url)
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
    driver.implicitly_wait(5)
    return interpark_id, interpark_pw, driver


def logic():
    interpark_id, interpark_pw, driver = init_variable()
    login_logic(driver, interpark_id, interpark_pw)
    date_selection_logic(driver)
    init_reservation_page(driver)
    seat_acquisition_logic(driver)

    time.sleep(5000)
    driver.close()
    return


def main():
    logic()
    return


if __name__ == '__main__':
    main()
