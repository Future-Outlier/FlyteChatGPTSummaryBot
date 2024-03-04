import flytekit
from flytekit import ImageSpec, Secret, task, workflow
from flytekitplugins.chatgpt import ChatGPTTask

flytekit_master = "git+https://github.com/flyteorg/flytekit.git@master"
chatgpt_plugin = "git+https://github.com/flyteorg/flytekit.git@master#subdirectory=plugins/flytekit-openai"
image = ImageSpec(
    apt_packages=["git"],
    packages=[
        flytekit_master,
        chatgpt_plugin,
        "requests",
        "slack_sdk",
    ],
    registry="futureoutlier",
)

chatgpt_job = ChatGPTTask(
    name="gpt-3.5-turbo",
    openai_organization="org-NayNG68kGnVXMJ8Ak4PMgQv7",
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)


@task(
    container_image=image,
    secret_requests=[Secret(key="token", group="github-api")],
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
    container_image=image,
    secret_requests=[Secret(key="token", group="slack-api")],
)
def post_message_on_slack(channel: str, message: str):
    from slack_sdk import WebClient

    token = flytekit.current_context().secrets.get("slack-api", "token")
    client = WebClient(token=token)
    client.chat_postMessage(channel=channel, text=message)


@workflow
def wf(owner: str = "flyteorg", repo: str = "flyte", channel: str = "demo"):
    message = get_github_latest_release(owner=owner, repo=repo)
    message = chatgpt_job(message=message)
    post_message_on_slack(channel=channel, message=message)


if __name__ == "__main__":
    wf()
