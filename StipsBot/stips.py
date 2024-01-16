from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

question_element = "item-card[_ngcontent-c31]"
answer_element = "content[_ngcontent-c31]"
comment_element = "static-action-fab[_ngcontent-c51]"
login_URL = "https://stips.co.il/login"
explore_URL = "https://stips.co.il/explore"
PATH = "D:/PycharmProjects/StipsBot/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(PATH)


def main():
    try:
        sleep(5)
        elements = get_all_questions_elements()
        elements_index = get_all_elements_with_one_answer(elements)
        print("Get All Elements")
        enter_question(elements[elements_index[cords(elements)]])
        # enter_question(elements[elements_index[0]])
        print("Enter Element")
        sleep(2)
        send_answer()
        driver.back()
    except IndexError:
        print("No questions with 1 answer, refreshing the page.")
        driver.refresh()


def cords(elements):
    for element in elements:
        print("cords = ", element.location)
        if element.location['y'] < 1000:
            print("index = ", elements.index(element))
            return elements.index(element)


def login_stips():                                                                                               # login
    driver.get("https://stips.co.il/login")
    driver.find_element_by_name("email").send_keys("reuvenush@gmail.com")
    driver.find_element_by_id("mat-input-2").send_keys("@Re322855909")
    driver.find_element_by_class_name("mat-raised-button[_ngcontent-c19]").click()


def get_all_questions_elements():                                                    # Get the elements of all questions
    global question_element
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, question_element))
    )
    return elements


def get_question_description_by_element(element):                              # Get the description of specific element
    description = element.text.splitlines()
    description = {
        "Question": description[0],
        "Name": description[1],
        "Time": description[2],
        "Answers": description[3],
        "Thumbtack": description[4]
    }
    return description


def get_all_elements_with_one_answer(elements):                                     # Get all the elements with 1 answer
    indexes = []
    description = [get_question_description_by_element(element) for element in elements]
    for element in description:
        if element["Answers"] == "1":
            indexes.append(description.index(element))
    return indexes


def enter_question(element):                                                             # Enter the question by element
    element.click()


def get_first_answer():
    global answer_element
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, answer_element))
    )
    texts = [element.text for element in elements]
    return texts[-1]


def edited_answer(answer):
    pass


def send_answer():
    global comment_element
    answer = get_first_answer()
    print("answer = ", answer)
    driver.refresh()
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[normalize-space()="comment"]'))
    )
    #button = WebDriverWait(driver, 10).until(
    #    EC.presence_of_all_elements_located((By.CLASS_NAME, comment_element))
    #)
    button.click()
    driver.find_element_by_name("a").send_keys(answer)
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mat-icon[dir=rtl]"))
    )
    button.click()


def get_question_url():                                                                    # Get the URL of the question
    global question_element
    href = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, question_element + " [href]"))
    )
    href = href.get_attribute('href')
    href = href.split("/%", 1)
    return href[0]


login_stips()
driver.get(explore_URL)
while True:
    main()

"""try:
    # get all the questions with 1 answer and click on the first question of it
    elements = get_all_questions_elements()
    elems_index = get_all_elements_with_one_answer(elements)
    print("elems_index = ", elems_index)
    print("elems_index[0] = ", elems_index)
    print("elements in index[0] = ", elements[elems_index[0]])

    sleep(3)

    enter_question(elements[elems_index[0]])

    sleep(2)

    # try to get text of the first answer
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, answer_element))
    )
    texts = [element.text for element in elements]
    print(texts)
    print("last = ", texts[-1])

except IndexError:
    print("No questions with 1 answer.")"""



#element.click()

#search = driver.find_element_by_class_name("item-card")

#print("text = ", search.text)

#search.click()

#driver.quit()
