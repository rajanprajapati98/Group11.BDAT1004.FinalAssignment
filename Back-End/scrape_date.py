import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_acquisition_data_collection


def can_it_convert_to_digit(string_value):
    try:
        int_value = int(string_value.replace(',', ''))
        return int_value
    except ValueError:
        return False


def take_covid_data():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.worldometers.info/coronavirus/")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    each_row = driver.find_elements(By.XPATH, '/html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/tbody[1]/tr')
    all_countries_data = []
    count = 1
    for i in range(1, len(each_row)):
        each_column_in_row = each_row[i].find_elements(By.XPATH,
                                                       f'/html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/tbody[1]/tr[{i}]/td')
        column_data = {
            'country': '',
            'total_cases': 0,
            'total_deaths': 0,
            'total_recovered': 0,
            'active_cases': 0,
            'total_tests_1m_pop': 0,
            'deaths_1m_pop': 0,
            'total_tests': 0,
            'tests_1m_pop': 0,
            'population': 0,
        }

        column_raw_data = []
        # column index
        # 1: country
        # 2: total cases
        # 4: total deaths
        # 6: total recovered
        # 8: active cases
        # 10: total tests 1m pop
        # 11: deaths 1m pop
        # 12: total tests
        # 13 test per 1m pop
        # 14: population
        for j in [1, 2, 4, 6, 8, 10, 11, 12, 13, 14]:
            column_raw_data.append(each_column_in_row[j].text)
        for k in range(len(column_data)):
            if k == 0:
                column_data['country'] = column_raw_data[k]
            elif k == 1:
                column_data['total_cases'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 2:
                column_data['total_deaths'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 3:
                column_data['total_recovered'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 4:
                column_data['active_cases'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 5:
                column_data['total_tests_1m_pop'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 6:
                column_data['deaths_1m_pop'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 7:
                column_data['total_tests'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 8:
                column_data['tests_1m_pop'] = can_it_convert_to_digit(column_raw_data[k])
            elif k == 9:
                column_data['population'] = can_it_convert_to_digit(column_raw_data[k])
                has_all_data = True
                for key, value in column_data.items():
                    if value == '' or value == 'N/A' or value == False:
                        has_all_data = False
                else:
                    if has_all_data:
                        column_data['country_id'] = count
                        count += 1
                        all_countries_data.append(column_data)
    acquisition_data_collection = get_acquisition_data_collection()
    # delete all data from acquisition_data_collection
    acquisition_data_collection.delete_many({})
    # save all data to acquisition_data_collection
    acquisition_data_collection.insert_many(all_countries_data)
    # save list of dictionaries to csv file with headers
    column_name = all_countries_data[0].keys()
    with open('corona_affected_country.csv', 'w', newline='') as corona_affected_country_file:
        dw = csv.DictWriter(corona_affected_country_file, column_name)
        dw.writeheader()
        dw.writerows(all_countries_data)
    return True

take_covid_data()