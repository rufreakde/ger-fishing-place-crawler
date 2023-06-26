from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

from bs4 import BeautifulSoup

def main():
    baseurl = "https://www.anglermap.de/gewaesserportal/liste-stillwasser.php"
    driver = webdriver.Firefox()
    driver.get(baseurl)
    python_button = driver.find_element(By.ID, "ez-accept-all")
    python_button.click()

    soup = BeautifulSoup(driver.page_source)

    gewaessergrob = soup.find("div", {"id": "gewaesserliste"})
    table = gewaessergrob.find("table", {
        "class": "table table-condensed text04"})  # Replace 'table' with the appropriate HTML tag or class of the table

    inhalt = {}
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

    driver.close()



# url = "https://www.anglermap.de/gewaesserportal/liste-stillwasser.php"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")

if __name__ == "__main__":
    main()