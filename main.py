import os
import time
from datetime import datetime

#from dotenv import load_dotenv

from ops.webscraper import WebScraper

load_dotenv()


# Get the current date and time
current_time = datetime.now()

# Format as a string
timestamp_str = current_time.strftime("%Y%m%d%H%M%S")

filename = os.getenv("FILE_LOCATION") + timestamp_str + ".txt"
driver = os.getenv("CHROME_DRIVER_LOCATION")

ws = WebScraper(filename)
range_end = os.getenv("NUMBER_OF_PAGES")

print(range_end)

for page_num in range(1, int(range_end)):
    ws.load_page(str(page_num))
    question_text = ws.extract_question()
    # print(question_text)
    # print(f"Text for page number {page_num}:\n{question_text}\n{'='*30}")
    answers = ws.extract_answers()
    if ws.load_response(driver, answers[0]):
        print("yay")
        correct_answer, answer_text = ws.extract_correct_answer()
        # statistics = ws.extract_statistics()

    # print(answers)
    ws.set_quiz_data(page_num, question_text, answers, correct_answer, answer_text)
    ws.write_to_file(page_num, question_text, answers, correct_answer, answer_text)

    time.sleep(1)

print(ws.quiz_data)
