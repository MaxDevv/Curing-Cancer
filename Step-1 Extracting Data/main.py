import praw, json, time
import os
from dotenv import load_dotenv


load_dotenv()



clientId = os.getenv("REDDIT_CLIENT_ID")
clientSecret = os.getenv("REDDIT_CLIENT_SECRET")

reddit = praw.Reddit(
    client_id=clientId,
    client_secret=clientSecret,
    user_agent = os.getenv("REDDIT_USER_AGENT")
)

cancer = reddit.subreddit("cancer")

results = []
cnt = 0
for post in cancer.search("how found", limit=None):
    cnt += 1
    try:
        res = {
            # "post": post,
            "title": post.title,
            "text": post.selftext,
            "comments": [comment.body for comment in post.comments.list() if isinstance(comment, praw.models.Comment)]
        }
        results.append(res)
        # print(res)
        with open("subreddit.cancer", "a") as f:
            f.write("\n\n\n!@#$%^&*()\n" + json.dumps(res))
        print(f"Post #{str(cnt)}:\n    comments: {str(len(res["comments"]))}")
        time.sleep(0.75)
    except Exception as e:
        print("An error occured:", str(e))
        time.sleep(180)