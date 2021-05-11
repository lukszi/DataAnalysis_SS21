import praw
import json

config_path = "res/reddit_config.json"
if __name__ == '__main__':
    config_path = "../res/reddit_config.json"

with open(config_path, "r", encoding="UTF-8") as config_file:
    config = json.load(config_file)


reddit = praw.Reddit(client_id=config["client_id"], client_secret=config["client_secret"],
                     password=config["password"], user_agent="android:com.example.myredditapp:v1.2.4",
                     username=config["username"])

wsb = reddit.subreddit("WallStreetBets")
wsb_new = wsb.new(limit=256)
for submission in wsb_new:
    print(submission.score)
