#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Description
------------------
A brief description of what this module/script does.
"""

import sys, os, json
from typing import Optional, Any
from numba import jit

# ===== Configuration =====
class Config:
    """Global settings (variables instead of constants)."""
    defaultValue = 42
    verbose = True
    UseArgParse = True  # Enable to activate CLI parsing
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class Utils:
    def chunkArr(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


# ===== Numba-Accelerated Functions =====
@jit(nopython=True)
def fastSquare(x: float) -> float:
    """Compute x² (optimized with Numba)."""
    return x * x

# ===== Main Class =====
class MainClass:
    """
    Core processing class with configurable workflow.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.result = None
        with open(os.path.join(Config.SCRIPT_DIR, "processed-anecdoes-total-combined.json"), "r") as f:
            self.anecdotes = json.load(f)


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


    def extractSymptoms(self, post: dict) -> list:
        """
        Description:
            - Extract the symptoms detailed into a string list
        Args:
            - Post, an objcect representing the post
        """
        # print(post)
        if self.verbose:
            print("Processing post...")

        
        symptoms = []
    
        def getSymptoms(symptomList: list) -> list:
            l = symptomList.get("major", []) + symptomList.get("minor", [])
            return [i["symptom"] for i in l]
        
        symptoms.extend(getSymptoms(post["symptoms"]))
        
        for comment in post["comments"]:
            symptoms.extend(getSymptoms(comment["symptoms"]))
        

        return symptoms
        
        
    def run(self) -> None:
        """
        Description:
            - The main logic for this module.
        Args:
            - An imaginary argument
        """
        symptoms = [self.extractSymptoms(post["post"]) for post in self.anecdotes]

        # flatten list, I have no frigging clue how this works, and im tired of reading it
        symptoms = [symptom for i in symptoms for symptom in i]

        if self.verbose:
            print("symptom count", len(symptoms))
        
        # hoping im lucky by tryna remove some duplicates
        symptoms = list(set(
            symptom.lower().replace(",", "").replace(".", "").replace("!", "").replace("?", "").replace(";", "").replace(":", "")
            for symptom in symptoms
        ))
        if self.verbose:
            print("symptom count", len(symptoms))

        # WTF THAT WORKED got it down from 1697 to 1167
        # print(symptoms[])
        with open(os.path.join(Config.SCRIPT_DIR, "symptoms-disorganized.txt"), "w+") as f:
            f.write("\n".join(f"{idx+1}). {i}" for idx, i in enumerate(symptoms)))
        # print("\n".join(symptoms))
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
