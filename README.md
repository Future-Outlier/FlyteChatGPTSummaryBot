# FlyteSummaryBot
## Demo
### Get Latest Flyte Release Summary
Execute it locally by `python`

Create the secret locally
```bash
cd /etc/secrets
mkdir slack-api
echo "SLACK_API_TOKEN" > token
```
```bash
python getFlyteLatestReleaseSummary.py
```
Or execute it remotley by `pyflyte run --remote`
```bash
kubectl create secret generic slack-api\
      --from-literal=token="SLACK_API_TOKEN"
```
```bash
pyflyte run --remote --image your-image getFlyteLatestReleaseSummary.py wf
```

Screenshot

![Alt text](./img/slackbot.png)

### Get Weekly MLOps Trend
Get the MLOps latest news from Medium and summarize it to [this Twitter Account](https://twitter.com/MLOpsTrendBot)!

https://github.com/Future-Outlier/MLOpsTrendFlyteBot/assets/76461262/ca79a0a0-2ac8-4d65-b22f-0a48506dca2d

Execute it by `python`

Create the secret locally
```bash
cd /etc/secrets
mkdir tweet-api
echo "bearer_token" > bearer_token
echo "consumer_key" > consumer_key
echo "consumer_secret" > consumer_secret
echo "access_token" > access_token
echo "access_token_secret" > access_token_secret
```
```bash
python getWeeklyMLOpsTrend.py
```
Or execute it remotley by `pyflyte run --remote`
```bash
kubectl create secret generic tweet-api\
      --from-literal=bearer_token="bearer_token"\
      --from-literal=consumer_key="consumer_key"\
      --from-literal=consumer_secret="consumer_secret"\
      --from-literal=access_token="access_token"\
      --from-literal=access_token_secret="access_token_secret"
```
```bash
pyflyte run --remote --image your-image getWeeklyMLOpsTrend.py wf --url "https://medium.com/tag/mlops"
```

Screenshot

![Alt text](./img/tweet.png)

## Motivation
In today's digital era, the sheer volume of online content has grown exponentially, making it a challenge for individuals to sift through and stay updated. This is especially true in specialized domains like MLOps, where the rapid evolution of trends, tools, and methodologies demands constant vigilance.

MLOpsTrendFlyteBot is a new tool that helps with this problem. It uses ChatGPT to find the newest and most important MLOps news articles on Medium. Then, it shortens these articles and shares the key information. It uses Flyte's machine learning workflows to do this automatically. This way, users get clear and complete updates right in their Twitter feed.

MLOpsTrendFlyteBot could also be helpful in many other situations:

- For companies - It could take long weekly updates and summarize them into shorter versions. This would help employees stay informed.
- After big events - There are usually many long articles and reports afterward. The tool could make short recaps so people can catch up fast.
- For tech products - When new software versions come out, the changes can be hard to understand. Summaries of the updates would help users.
- For brands - They could use it to sort through customer feedback from different sites. This would help them understand how people feel about their products.

The main idea behind MLOpsTrendFlyteBot is useful in lots of places.
The tool can be used in many ways, helping people handle lots of information.

## How it works
### Overview of the Workflow
![Alt text](./img/workflow.png)
### Architecture Diagram
![Alt text](./img/Architecture.png)

### Web Scraping Medium Articles
We utilize web scraping techniques to extract articles from [medium MLOps](https://medium.com/tag/mlops).

The goal is to gather relevant and latest content about MLOps from a trusted source.

### Summarization with ChatGPT (GPT-4 Model)
The extracted texts from Medium are fed into the ChatGPT model with GPT-4 architecture.

The model generates a concise summary of the articles, ensuring the essence of the content is retained.

### Tweeting the Summaries
The summarized content is then posted on Twitter, allowing followers to get quick insights into the latest MLOps articles without having to read the entire piece.

## How to setup
### 1.Start your flyte cluster.
```bash
flytectl demo start
```
This step will start your flyte cluster and agent server.
The agent server will handle the ChatGPT Task to OpenAI server.
### 2.Add the OpenAI access token
Set the secret I write in `demo` section.

```bash
kubectl edit secret flyteagent -n flyte
```
```yaml
apiVersion: v1
data:
  flyte_openai_access_token: <BASE64_ENCODED_OPENAI_TOKEN>
  username: User
```
```bash
kubectl rollout restart deployment flyteagent  -n flyte
```

## Other Use cases
### Corporate News Digest
Companies frequently release weekly and daily updates.

Using this technology, we can automate the process of summarizing these updates, providing employees and stakeholders with concise digests of essential information.

### Event Recaps
After major industry events or conferences, there's often an influx of articles, interviews, and reports.

This system can generate quick recaps, allowing interested parts to stay updated without spending hours reading.

### Product Updates
For tech companies releasing frequent product updates and patches, our solution can summarize the changelogs and release notes, making it easier for users to understand the latest changes.

### Social Media Monitoring
Brands can utilize this tool to summarize customer feedback and reviews from various platforms, helping them gain insights into customer sentiments more efficiently
