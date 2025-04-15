import subprocess

print(subprocess.call("wc -l subreddit.cancer | cut -d' ' -f1"))
# if subprocess.call("wc -l subreddit.cancer | cut -d' ' -f1") > subprocess.call("wc -l subreddit.cancer.bak | cut -d' ' -f1"):
    # subprocess.call("cp subreddit.cancer subreddit.cancer.bak")