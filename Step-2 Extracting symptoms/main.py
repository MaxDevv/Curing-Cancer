#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Description
------------------
A brief description of what this module/script does.
"""

import sys, json, os
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
            # cnt += self.countTokens(post["title"])
            # cnt += self.countTokens(post["text"])
            for comment in post["comments"]:
                cnt += self.countTokens(comment)
        self.verbose = self.wasVerbose

        print(cnt)
        
        print("Total tokens counted:", cnt)

        return cnt

        
    def run(self) -> None:
        """
        Description:
            - The main logic for this module.
        Args:
            - An imaginary argument
        """
        self.loadDump()
        # print(self.countComments())
        print(self.getTotTokens())
        pass

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