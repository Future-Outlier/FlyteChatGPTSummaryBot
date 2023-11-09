import flytekit
from flytekit import ImageSpec, Secret, task, workflow
from flytekitplugins.chatgpt import ChatGPTTask

chatgpt_job = ChatGPTTask(
    name="chatgpt",
    config={
        "openai_organization": flytekit.current_context().secrets.get(
            "OPENAI_ORGANIZATION"
        ),
        "chatgpt_conf": {
            "model": "gpt-4",
            "temperature": 0.7,
        },
    },
)


@task(
    secret_requests=[Secret(key="token", group="github-api")],
    container_image=ImageSpec(
        packages=[
            "flytekit",
            "requests",
        ],
        apt_packages=["git"],
        registry="futureoutlier",
    ),
)
def get_github_latest_release(owner: str = "flyteorg", repo: str = "flyte") -> str:
    import requests

    token = flytekit.current_context().secrets.get("github-api", "token")
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    message = (
        "You are a Bot. Provide a summary of the latest Flyte Github releases for users on Slack."
        "Ensure the response fits within 4000 characters, suitable for a Slack message. "
        "Start the message with 'This is the latest Flyte Github Releases'. "
        f"End the message with 'Checkout the page here: https://github.com/{owner}/{repo}/releases'. "
        "Note: Handling via the Slack API is not required. Format the response in bullet points.\n\n"
        f"Latest Releases:\n{response.json()['body']}"
    )

    return message


@task(
    secret_requests=[Secret(key="token", group="slack-api")],
    container_image=ImageSpec(
        packages=[
            "flytekit",
            "slack_sdk",
        ],
        apt_packages=["git"],
        registry="futureoutlier",
    ),
)
def post_message_on_slack(message: str):
    from slack_sdk import WebClient

    token = flytekit.current_context().secrets.get("slack-api", "token")
    client = WebClient(token=token)
    client.chat_postMessage(channel="demo", text=message)


@workflow
def wf():
    message = get_github_latest_release(owner="flyteorg", repo="flyte")
    message = chatgpt_job(message=message)
    post_message_on_slack(message=message)


if __name__ == "__main__":
    wf()
