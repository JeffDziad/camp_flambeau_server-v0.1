import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Firefox()
driver.set_window_size(750, 1000)


class Review:
    def __init__(self, title, rating, stayed, user, content, published, response):
        self.title = title
        self.rating = rating
        self.stayed = stayed
        self.user = user
        self.content = content
        self.published = published
        self.response = response

    def toDict(self):
        dict_out = {
            "title": self.title,
            "rating": self.rating,
            "stayed": self.stayed,
            "user": self.user,
            "content": self.content,
            "published": self.published,
            "response": self.response
        }
        return dict_out

    def toString(self):
        return "Title: {}\nRating: {}\nStayed: {}\nUser: {}\nContent: {}\nPublished: {}\nResponse: {}\n" \
            .format(self.title, self.rating, self.stayed, self.user, self.content, self.published, self.response)


def getReviews(vrbo_url):
    driver.get(vrbo_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    try:
        reviews_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.LINK_TEXT, "Reviews")))
        reviews_btn.click()

        view_all_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "review-list__view-all")))
        view_all_btn.click()

        reviews = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "review__content")))
        return classifyReviews(reviews)

    finally:
        driver.quit()


def writeToJson(name, obj):
    dump = json.dumps(obj, indent=0)
    try:
        with open(name, "w") as outfile:
            outfile.write(dump)
    finally:
        print("Successfully wrote to file: " + name + ".txt")


def printToConsole(obj):
    dump = json.dumps(obj, indent=0)
    print(dump)


def classifyReviews(reviewElements):
    classified = []
    for i in range(4, len(reviewElements)):
        lines = reviewElements[i].text.splitlines()
        if len(lines) <= 0:
            continue
        title = lines[0]
        rating = lines[1].split(" ")[0]
        stayed = lines[1].split(" ", 1)
        if len(stayed) > 1:
            stayed = stayed[1]
        else:
            stayed = ""
        user = lines[2]
        content = []
        published = ""
        response = ""

        response_line = 0
        for x in range(3, len(lines)):
            line = lines[x]
            if "Published" in line:
                response_line = x + 1
                published = line
                break
            else:
                content.append(line)

        if response_line < len(lines):
            split = lines[response_line].split(":", 1)
            if len(split) > 1:
                response = split[1]

        classified.append(Review(title, rating, stayed, user, " ".join(content), published, response))

    return classified


def scrapeForReviews():
    out = "Please provide a valid url!"
    if len(sys.argv) < 2:
        printToConsole(out);
    else:
        reviews = getReviews(sys.argv[1]);
        out = [];
        for i in range(0, len(reviews)):
            out.append(reviews[i].toDict());
        # writeToJson(name, reviews_dicts)
        printToConsole(out);


scrapeForReviews()