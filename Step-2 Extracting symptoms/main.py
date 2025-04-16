#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Description
------------------
A brief description of what this module/script does.
"""

import sys, json, os, re
from typing import Optional, Any
from vertexai.preview import tokenization

# ===== Configuration =====
class Config:
    """Global settings (variables instead of constants)."""
    defaultValue = 42
    verbose = True
    UseArgParse = True  # Enable to activate CLI parsing
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ===== Main Class =====
class MainClass:
    """
    Core processing class with configurable workflow.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.result = None
    '''
    # ==== Function Boilerplate ====
    def func(self, variable: int = 69) -> None:
        """
        Description:
            - Describe this function
        Args:
            - variable,  an int representing a variable
        """
        if self.verbose:
            print("Initializing processor...")
    '''

    def loadDump(self) -> None:
        """
        Description:
            - Loads the json dump of anecdotes
        """
        if self.verbose:
            print("Loading dump...")
        
        with open(os.path.join(Config.SCRIPT_DIR, "subreddit.cancer.json"), "r") as f:
            dump = json.load(f)["results"]
            
        self.dump = dump

    def countComments(self) -> int:
        """
        Description:
            - Returns the number of comments in the total file dump
        """
        if self.verbose:
            print("Counting comments...")
        cnt = 0

        for post in self.dump:
            cnt += len(post["comments"])

        if self.verbose:
            print(f"Total Comments: {cnt}")
        return cnt
    
    
    def countTokens(self, text: str) -> int:
        """
        Description:
            - Returns the total amount of tokens in a given text by gemini 1.5 flash model
        Args:
            - text: the given text of which to count the amount of tokens.
        """
        if self.verbose:
            print("Counting tokens...")
        if not hasattr(self, "tokenizer"):
            self.tokenizer = tokenization.get_tokenizer_for_model("gemini-1.5-flash-001")
        return self.tokenizer.count_tokens(text).total_tokens

    def formatPost(self, postIdx: int) -> str:
        """
        Description:
            - Formats a post into this format:
                ""Post 1: "{Insert Title}"
                    Body: "{Insert Body}"
                    Comments:
                        Comment 1.1: "Some Comment"
                        Comment 1.2: "Some Comment"
                ""
        Args:
            - variable,  an int representing a variable
        """
        def deEmojify(text):
            emoj = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642" 
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                            "]+", re.UNICODE)
            return re.sub(emoj, '', text)

        def cleanText(text):
            return deEmojify(text.replace("\n", " ").replace('\u2019', "'").replace('\u00a0', " ").replace('\u2013', "-").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2026', "...").replace('\ud83d\ude02', "").replace('\u2763\ufe0f', "").replace('\ud83d\udc95', ""))

        if self.verbose:
            print(f"Formatting post ({postIdx+1})...")
        post = self.dump[postIdx]
        post = f"""Post {postIdx+1}: "{cleanText(post["title"])}"
    Body: "{cleanText(post["text"])}"
    Comments:
{"\n".join([f'        Comment {postIdx+1}.{idx+1}: "{cleanText(comment)}"' for idx, comment in enumerate(post["comments"])])}
"""
        return post
        
    def getTotTokens(self) -> int:
        """
        Description:
            - Retrieves the total amount of tokens in the entire dump
        """
        if self.verbose:
            print("Counting total tokens...")

        cnt = 0
        # for my sanity
        self.wasVerbose = self.verbose
        self.verbose = False
        for post in self.dump:
            cnt += self.countTokens(post["title"])
            cnt += self.countTokens(post["text"])
            for comment in post["comments"]:
                cnt += self.countTokens(comment)
        self.verbose = self.wasVerbose
        
        if self.verbose:
            print("Total tokens counted:", cnt)

        return cnt

    # def extractSymptoms(self, )
        
    def run(self) -> None:
        """
        Description:
            - The main logic for this module.
        Args:
            - An imaginary argument
        """
        self.loadDump()
        # print(self.countComments())

        # lets test some chunk sizes, I want stuff that will fit into gemini's context window, Ik google yaps about a 1 million context window, but companies brag and exaggerate all the time so ill go for like ~300k tokens
        # chunk = "\n".join([self.formatPost(i) for i in range(100)])
        # self.verbose = False
        # print(
        #     self.countTokens("\n".join([self.formatPost(i) for i in range(100)])),
        #     self.countTokens("\n".join([self.formatPost(i) for i in range(100, 215)])),
        #     self.countTokens("\n".join([self.formatPost(i) for i in range(215, 275)])),
        #     self.countTokens("\n".join([self.formatPost(i) for i in range(275, 375)])),
        #     self.countTokens("\n".join([self.formatPost(i) for i in range(375, 494)])),
        # )
        # exit()
        # Took some finnessing but I managed to break it up into 5 relatively equal chunks of around 260k tokens

        # Token Sizes, In Order: 256987 268988 253182 288039 288417
        # chunks = [
        #     "\n".join([self.formatPost(i) for i in range(000, 100)]),
        #     "\n".join([self.formatPost(i) for i in range(100, 215)]),
        #     "\n".join([self.formatPost(i) for i in range(215, 275)]),
        #     "\n".join([self.formatPost(i) for i in range(275, 375)]),
        #     "\n".join([self.formatPost(i) for i in range(375, 494)]),
        # ]
        # print(self.countTokens("\n".join([self.formatPost(i) for i in range(000, 494)])))
        # with open(os.path.join(Config.SCRIPT_DIR, "formatted-posts.txt"), "w+") as f:
        #     f.write("\n".join([self.formatPost(i) for i in range(000, 494)]))


# ===== Main Function =====
def main() -> int:
    """Entry point with optional CLI args."""
    verbose = False

    # ===== Optional CLI =====
    if Config.UseArgParse:
        import argparse
        parser = argparse.ArgumentParser(description="MainClass runner.")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug mode")
        args = parser.parse_args()
        verbose = args.verbose

    # Run processor
    processor = MainClass(verbose=(verbose or Config.verbose))
    return processor.run()

if __name__ == "__main__":
    sys.exit(main())