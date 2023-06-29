import time
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import json

from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_table(x):
    result = x.find_element_by_id("gewaesserliste")
    return result


def main():
    baseurl = "https://www.anglermap.de/gewaesserportal/liste-stillwasser.php"
    try:
        print("Try using Firefox")
        driver = webdriver.Firefox()
        time.sleep(2)
    except:
        print("Fallback to Chrome")
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(
            options=options,
        )
        time.sleep(2)
    driver.get(baseurl)
    python_button = driver.find_element(By.ID, "ez-accept-all")
    python_button.click()

    inhalt = {}

    buchstabenliste = driver.find_elements(By.CLASS_NAME, "gewaesserabc")
    buchstaben = [x.accessible_name for x in buchstabenliste]
    for index, buchstabe in enumerate(buchstaben):
        buchstabenelement = driver.find_elements(By.CLASS_NAME, "gewaesserabc")[index]
        driver.execute_script("arguments[0].click();", buchstabenelement)

        try:
            python_button = driver.find_element(By.ID, "ez-accept-all")
            python_button.click()
        except:
            pass

        print("waiting...", end='')
        wait = WebDriverWait(driver, 2)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "liste_well_anz")))
        print("finished")
        soup = BeautifulSoup(driver.page_source)

        gewaessergrob = soup.find("div", {"id": "gewaesserliste"})
        table = gewaessergrob.find("table", {
            "class": "table table-condensed text04"})  # Replace 'table' with the appropriate HTML tag or class of the table


        for row in table.find_all("tr")[1:]:
            # Extract the data from each column
            columns = row.find_all("td")
            if len(columns) <= 5:
                continue
            name = columns[0].text.strip()
            url = urljoin(baseurl, columns[0].contents[0]['href'])
            ortslage = columns[1].text.strip()
            gastkarten = len([x for x in columns[2].children]) >= 1
            fischbestand = len([x for x in columns[3].children]) >= 1
            gewaesserinfos = len([x for x in columns[4].children]) >= 1
            inhalt[name] = {"ortslage": ortslage,
                            "gastkarten": gastkarten,
                            "fischbestand": fischbestand,
                            "gewaesserinfos": gewaesserinfos,
                            "url": url}

    with open('anglermap-de-gewaesserportal.json', 'w') as fp:
        json.dump(inhalt, fp)
    driver.close()



# url = "https://www.anglermap.de/gewaesserportal/liste-stillwasser.php"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")

if __name__ == "__main__":
    main()