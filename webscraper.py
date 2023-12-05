import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class WebScraper:
    def __init__(self, filename):
        self.filename = filename
        self.baseurl = "https://upgrader.gapminder.org/q/"
        self.gapminder_url = ""
        self.questionclass = "md:max-w-desktop-inner"
        self.answerclass = "bg-[#eef9ef]"
        self.answers = []
        self.soup = None
        self.response_soup = None
        self.quiz_data = {}
        self.answer_data = {}
        with open(self.filename, "w") as file:
            file.write("Quiz Data\n")
            file.write("---------\n")

    def load_page(self, page_number):
        self.answers = []
        self.gapminder_url = self.baseurl + page_number + "/"

        # print(self.gapminder_url)

        response = requests.get(self.gapminder_url)
        if response.status_code != 200:
            return "Failed to retrieve the page."

        self.soup = BeautifulSoup(response.text, "html.parser")

    def load_response(self, chrome_driver_path, answer):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Set up the WebDriver

        s = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=s, options=chrome_options)

        # Open the webpage
        driver.get(self.gapminder_url)

        buttons = driver.find_elements(By.Xpath, "//button[contains(.//*,'" + answer + "')]")

        # Optionally, also find all input elements of type 'button'
        #input_buttons = driver.find_elements(By.XPATH, "//input[@type='button']")
        #buttons.extend(input_buttons)

        # Iterate through the list of buttons
        for button in buttons:
            # You can add a condition to check something specific about the button
            # For example, check the button's text, if it has any
            print("[" + button.text + "]=[" + answer + "]")
            if button.text == answer:
                button.click()
                print(driver.current_url)
                # WebDriverWait(driver, 10).until(
                #    lambda x: driver.current_url == self.gapminder_url + "explanation"
                # )
                time.sleep(5)
                print(driver.current_url)
                html_content = driver.page_source
                self.response_soup = BeautifulSoup(html_content, "html.parser")
                driver.quit()
                return True

        # Get the page source after submission

        driver.quit()

        return False

    def extract_question(self):
        # Lets construct our URL with our language and page title input parameters

        # print(soup)
        main_body_text = ""

        for div in self.soup.find_all(
            "div", class_=lambda x: x and self.questionclass in x.split()
        ):
            h1s = div.find_all(
                "h1", recursive=False
            )  # Finds only direct child h1 elements
            for h1 in h1s:
                main_body_text = h1.get_text()

                # print(main_body_text)
        return main_body_text

    def extract_answers(self, answertag="button"):
        for btns in self.soup.find_all(answertag):
            for btn in btns:
                if btn is not None and btn != " ":
                    self.add_answer_list(btn.strip())
        return self.answers

    def extract_correct_answer(self):
        correct_answer = ""
        answer_text = ""
        with open("test.txt", "w") as file:
            file.write("Output\n")
            file.write("---------\n")
            file.write(self.response_soup.prettify())

        for div in self.response_soup.find_all(
            "div", class_=lambda x: x and self.answerclass in x.split()
        ):
            print("hello")
            print(div)
            h2s = div.find_all(
                "h2", recursive=False
            )  # Finds only direct child h2 elements
            for h2 in h2s:
                correct_answer = h2.get_text()
            ps = div.find_all(
                "p", recursive=False
            )  # Finds only direct child p elements
            for p in ps:
                answer_text = p.get_text()

                # print(main_body_text)
        return correct_answer, answer_text

    def extract_statistics(self, answertag="button"):
        for btns in self.soup.find_all(answertag):
            for btn in btns:
                if btn is not None and btn != " ":
                    self.add_answer_list(btn.strip())
        return self.answers

    def add_answer_list(self, answer):
        self.answers.append(answer)

    def set_quiz_data(
        self, question_num, question, answers, correct_answer, answer_text
    ):
        self.quiz_data[f"question{question_num}"] = {
            "question": question,
            "options": answers,
            "correct_answer": correct_answer,
            "answer_text": answer_text,
        }

    def write_to_file(
        self, question_num, question, answers, correct_answer, answer_text
    ):
        with open(self.filename, "a") as file:
            file.write(f"Question Number: {question_num}\n")
            file.write(f"Question: {question}\n")
            for answer in answers:
                file.write(f"- {answer}\n")
            file.write(f"Correct Answer: {correct_answer}\n")
            file.write(f"Answer Text: {answer_text}\n")
            file.write("\n")
