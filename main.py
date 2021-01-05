import os
import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """Gets a random fact from http://unkno.com/"""
    response = requests.get("http://unkno.com/")

    soup = BeautifulSoup(response.content, "html.parser")
    fact = soup.find("div", id="content")

    return fact


def pig_fact(fact):
    """Translates fact to piglatin using a microservice on Heroku"""
    piglatinize_url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    request = {"input_text": fact}
    response = requests.post(piglatinize_url, request, allow_redirects=False)
    link = response.headers["Location"]

    return link


@app.route('/', methods=["GET"])
def home():
    fact = get_fact()
    link = pig_fact(fact)

    return render_template("base.jinja2", link=link)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
