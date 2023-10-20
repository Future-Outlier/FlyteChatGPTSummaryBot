import os

from flytekit import task, workflow
from flytekitplugins.chatgpt import ChatGPTTask

chatgpt_job = ChatGPTTask(
    name="chatgpt",
    config={
        "openai_organization": os.environ.get("OPENAI_ORGANIZATION"),
        "chatgpt_conf": {
            "model": "gpt-4",
            "temperature": 0.7,
        },
    },
)


@task
def get_weekly_articles_title(url: str = "https://medium.com/tag/mlops") -> str:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.get(url)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    texts = soup.stripped_strings
    all_text = " ".join(texts)

    message = (
        f"You are a Bot. Provide a summary of the latest MLOps trend for users on Medium. "
        f"Your response should fit within 280 characters for a tweet, excluding the article's title. "
        f"Start the message with '''This is the trend of MLOps on Medium this week\n'''. Note: Tweet API handling is not required."
        f"```````"
        f"Article Title: {all_text}"
    )

    return message


@task
def tweet(text: str):
    import os

    import tweepy

    TWEET_LENGTH = 280
    BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
    CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    if len(text) > TWEET_LENGTH:
        text = text[:TWEET_LENGTH]
    client.create_tweet(text=text)


@workflow
def wf(url: str = "https://medium.com/tag/mlops"):
    message = get_weekly_articles_title(url=url)
    message = chatgpt_job(message=message)
    tweet(text=message)


if __name__ == "__main__":
    wf()
