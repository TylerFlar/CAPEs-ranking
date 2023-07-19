from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import os

class CourseScraper:
    TIMEOUT_SECONDS = 10

    def __init__(self):
        # Load credentials and chrome profile from file
        with open('credentials.txt', 'r') as f:
            self.username = f.readline().strip()
            self.password = f.readline().strip()
            chromeprofile = f.readline().strip()
        
        # Setup the webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=" + chromeprofile)
        self.driver = webdriver.Chrome(options=options)

        self.first_run = True
        self.departments = self.fetch_departments()

    def fetch_departments(self):
        self.driver.get("https://educationalinnovation.ucsd.edu/_files/prereq-diffs.html")
        sidebar = WebDriverWait(self.driver, self.TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.CLASS_NAME, "sidebar")))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        sidebar = soup.find('nav', class_='sidebar')

        return {
            details.find('summary').text: [
                li.text.replace(details.find('summary').text + ' ', '')
                for li in details.find_all('li')
            ]
            for details in sidebar.find_all('details') # type: ignore
        }

    def login(self):
        WebDriverWait(self.driver, self.TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.ID, "ssousername")))
        username_field = self.driver.find_element(By.ID, "ssousername")
        password_field = self.driver.find_element(By.ID, "ssopassword")
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        login_button = self.driver.find_element(By.NAME, "_eventId_proceed")
        login_button.click()

    def scrape(self):
        for dept_code, course_numbers in self.departments.items():
            directory = f"evals/{dept_code.lower()}"
            os.makedirs(directory, exist_ok=True)

            for course_number in course_numbers:
                self.driver.get(f"https://cape.ucsd.edu/responses/Results.aspx?courseNumber={dept_code}+{course_number}")

                if self.first_run:
                    self.login()
                    self.first_run = False

                WebDriverWait(self.driver, self.TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_gvCAPEs")))
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find('table', {'class': 'styled'})

                headers, rows = [], []
                for row in table.find_all('tr'): # type: ignore
                    tds = row.find_all('td')
                    if len(tds) > 1:
                        if dept_code + " " + course_number + " -" in tds[1].text:
                            rows.append([td.text for td in tds])
                    else:
                        headers = [header.text for header in row.find_all('th')]

                df = pd.DataFrame(rows, columns=headers)
                df = df.dropna(how='all')

                if not df.empty:
                    df.to_csv(f"{directory}/{dept_code.lower()}-{course_number}.csv", index=False)

        self.driver.quit()

if __name__ == "__main__":
    scraper = CourseScraper()
    scraper.scrape()