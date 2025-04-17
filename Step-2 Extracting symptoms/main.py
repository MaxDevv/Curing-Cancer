#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Description
------------------
Processes and analyses anecdotes to extract scale data and symptoms
"""

import sys, json, os, re, time
from typing import Optional, Any
from vertexai.preview import tokenization
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv


# ===== Configuration =====
class Config:
    """Global settings (variables instead of constants)."""
    defaultValue = 42
    verbose = True
    UseArgParse = True  # Enable to activate CLI parsing
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    prompt = """You are an expert medical research assistant helping analyze cancer patient anecdotes. Your task is to carefully extract ALL symptoms and bodily changes mentioned in these posts, with special attention to the subtle, early warning signs that patients initially dismissed or didn't recognize as significant.

For each post and relevant comment, extract:
1. ALL symptoms mentioned (both subtle/minor and obvious/major)
2. WHEN they appeared in the patient's journey (pre-diagnosis, during diagnosis, etc.)
3. How the patient PERCEIVED the symptom initially (dismissed, concerned, etc.)
4. Any LIFESTYLE or BEHAVIORAL changes mentioned

IMPORTANT GUIDELINES:
- Include EVERY symptom mentioned, no matter how seemingly insignificant
- Be VERY, VERY, VERY, Detailed when describing every symptom, do not lose or simplify any symptom whatsover.
- For symptoms where timing/perception isn't specified, use "unknown"
- If no symptoms or lifestyle changes are mentioned in a comment or post, leave the array empty
- Classify symptoms as "minor" if the patient initially dismissed them or didn't seek immediate medical attention
- Classify symptoms as "major" if they prompted immediate medical concern
- In cases of uncertainty about classification, classify as minor

Here are the posts to analyze:
"""

    # Ngl I really hate this indent structure
    structure = """{
  "type": "object",
  "properties": {
    "posts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "post": {
            "type": "object",
            "properties": {
              "post_id": {
                "type": "string"
              },
              "symptoms": {
                "type": "object",
                "properties": {
                  "minor": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "symptom": {
                          "type": "string"
                        },
                        "timing": {
                          "type": "string"
                        },
                        "initially_perceived_as": {
                          "type": "string"
                        }
                      }
                    }
                  },
                  "major": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "symptom": {
                          "type": "string"
                        },
                        "timing": {
                          "type": "string"
                        },
                        "initially_perceived_as": {
                          "type": "string"
                        }
                      }
                    }
                  }
                }
              },
              "lifestyle_changes": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "comments": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "comment_id": {
                      "type": "string"
                    },
                    "symptoms": {
                      "type": "object",
                      "properties": {
                        "minor": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "symptom": {
                                "type": "string"
                              },
                              "timing": {
                                "type": "string"
                              },
                              "initially_perceived_as": {
                                "type": "string"
                              }
                            }
                          }
                        },
                        "major": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "symptom": {
                                "type": "string"
                              },
                              "timing": {
                                "type": "string"
                              },
                              "initially_perceived_as": {
                                "type": "string"
                              }
                            }
                          }
                        }
                      }
                    },
                    "lifestyle_changes": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "comment_id",
                    "symptoms",
                    "lifestyle_changes"
                  ]
                }
              }
            },
            "required": [
              "post_id",
              "symptoms",
              "lifestyle_changes"
            ]
          }
        },
        "required": [
          "post"
        ]
      }
    }
  },
  "required": [
    "posts"
  ]
}"""


class Utils:
    def chunk(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


class Gemini:
    """
    Home baked wrapper for interacting with gemini api
    """

    def __init__(self, apiKey: str, verbose: bool = False):
        self.verbose = verbose
        self.key = apiKey



    def extractSymptoms(self, posts: str) -> dict:
        client = genai.Client(
            api_key=self.key,
        )
        model = "gemini-2.0-flash-lite"
        model = "gemini-2.0-flash"
        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=Config.prompt+posts),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                            type = genai.types.Type.OBJECT,
                            required = ["posts"],
                            properties = {
                                "posts": genai.types.Schema(
                                    type = genai.types.Type.ARRAY,
                                    items = genai.types.Schema(
                                        type = genai.types.Type.OBJECT,
                                        required = ["post"],
                                        properties = {
                                            "post": genai.types.Schema(
                                                type = genai.types.Type.OBJECT,
                                                required = ["post_id", "symptoms", "lifestyle_changes"],
                                                properties = {
                                                    "post_id": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                    "symptoms": genai.types.Schema(
                                                        type = genai.types.Type.OBJECT,
                                                        properties = {
                                                            "minor": genai.types.Schema(
                                                                type = genai.types.Type.ARRAY,
                                                                items = genai.types.Schema(
                                                                    type = genai.types.Type.OBJECT,
                                                                    properties = {
                                                                        "symptom": genai.types.Schema(
                                                                            type = genai.types.Type.STRING,
                                                                        ),
                                                                        "timing": genai.types.Schema(
                                                                            type = genai.types.Type.STRING,
                                                                        ),
                                                                        "initially_perceived_as": genai.types.Schema(
                                                                            type = genai.types.Type.STRING,
                                                                        ),
                                                                    },
                                                                ),
                                                            ),
                                                            "major": genai.types.Schema(
                                                                type = genai.types.Type.ARRAY,
                                                                items = genai.types.Schema(
                                                                    type = genai.types.Type.OBJECT,
                                                                    properties = {
                                                                        "symptom": genai.types.Schema(
                                                                            type = genai.types.Type.STRING,
                                                                        ),
                                                                        "timing": genai.types.Schema(
                                                                            type = genai.types.Type.STRING,
                                                                        ),
                                                                        "initially_perceived_as": genai.types.Schema(
                                                                            type = genai.types.Type.STRING,
                                                                        ),
                                                                    },
                                                                ),
                                                            ),
                                                        },
                                                    ),
                                                    "lifestyle_changes": genai.types.Schema(
                                                        type = genai.types.Type.ARRAY,
                                                        items = genai.types.Schema(
                                                            type = genai.types.Type.STRING,
                                                        ),
                                                    ),
                                                    "comments": genai.types.Schema(
                                                        type = genai.types.Type.ARRAY,
                                                        items = genai.types.Schema(
                                                            type = genai.types.Type.OBJECT,
                                                            required = ["comment_id", "symptoms", "lifestyle_changes"],
                                                            properties = {
                                                                "comment_id": genai.types.Schema(
                                                                    type = genai.types.Type.STRING,
                                                                ),
                                                                "symptoms": genai.types.Schema(
                                                                    type = genai.types.Type.OBJECT,
                                                                    properties = {
                                                                        "minor": genai.types.Schema(
                                                                            type = genai.types.Type.ARRAY,
                                                                            items = genai.types.Schema(
                                                                                type = genai.types.Type.OBJECT,
                                                                                properties = {
                                                                                    "symptom": genai.types.Schema(
                                                                                        type = genai.types.Type.STRING,
                                                                                    ),
                                                                                    "timing": genai.types.Schema(
                                                                                        type = genai.types.Type.STRING,
                                                                                    ),
                                                                                    "initially_perceived_as": genai.types.Schema(
                                                                                        type = genai.types.Type.STRING,
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ),
                                                                        "major": genai.types.Schema(
                                                                            type = genai.types.Type.ARRAY,
                                                                            items = genai.types.Schema(
                                                                                type = genai.types.Type.OBJECT,
                                                                                properties = {
                                                                                    "symptom": genai.types.Schema(
                                                                                        type = genai.types.Type.STRING,
                                                                                    ),
                                                                                    "timing": genai.types.Schema(
                                                                                        type = genai.types.Type.STRING,
                                                                                    ),
                                                                                    "initially_perceived_as": genai.types.Schema(
                                                                                        type = genai.types.Type.STRING,
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ),
                                                                    },
                                                                ),
                                                                "lifestyle_changes": genai.types.Schema(
                                                                    type = genai.types.Type.ARRAY,
                                                                    items = genai.types.Schema(
                                                                        type = genai.types.Type.STRING,
                                                                    ),
                                                                ),
                                                            },
                                                        ),
                                                    ),
                                                },
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
        # return json.loads(response.text)



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
    
    def tempDisableVerbosity(self) -> None:
        if not hasattr(self, "wasVerbose"):
            self.wasVerbose = self.verbose
        self.verbose = False

    def restoreVerbosity(self) -> None:
        self.verbose = self.wasVerbose

    def mergeChunks(self, chunks, maxTokens = 6144) -> list:
        """
        Description:
                    - Merges chunks of text together if their combined token count is under the limit
                Args:
                    - chunks: List of text chunks to potentially merge
                Returns:
                    - List of merged chunks that fit within token limits
        
        """
        self.tempDisableVerbosity()
        chunks = [[self.countTokens(chunk), chunk] for chunk in chunks]
        self.restoreVerbosity()
        for i in range(len(chunks)):
            chunk = chunks[i]
            if (chunk[0] == 0):
                continue
            if chunk[0] < maxTokens:
                for y in range(len(chunks)):
                    c = chunks[y]
                    if (y == i) or (c[0] == 0):
                        continue
                    if (c[0] + chunk[0] + 1) <= maxTokens:
                        chunks[i] = [chunk[0] + c[0] + 1, chunk[1] +"\n"+ c[1]]
                        chunks[y] = [0, ""]
                        chunk = chunks[i]

        chunks = [chunk[1] for chunk in chunks if chunk[0]]
        return chunks        
        
    def run(self) -> None:
        """
        Description:
            - The main logic for this module.
        Args:
            - An imaginary argument
        """
        # self.loadDump()
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


        # Raaahhh I knew the 1 million token window was too good to be true
        # google.genai.errors.servererror:%20503%20UNAVAILABLE.%20%7B'error'%3A%20%7B'code'%3A%20503,%20'message'%3A%20'The%20model%20is%20overloaded.%20Please%20try%20again%20later.',%20'status'%3A%20'UNAVAILABLE'%7D%7D
        # we'll need to break them down into smaller chunks, lets go for 128k        
        # Token Sizes, In Order: 256987 268988 253182 288039 288417
        # chunks = [
        #     "\n".join([self.formatPost(i) for i in range(000, 39)]),
        #     "\n".join([self.formatPost(i) for i in range(39, 90)]),
        #     "\n".join([self.formatPost(i) for i in range(90, 160)]),
        #     "\n".join([self.formatPost(i) for i in range(160, 205)]),
        #     "\n".join([self.formatPost(i) for i in range(205, 235)]),
        #     "\n".join([self.formatPost(i) for i in range(235, 250)]),
        #     "\n".join([self.formatPost(i) for i in range(250, 290)]),
        #     "\n".join([self.formatPost(i) for i in range(290, 330)]),
        #     "\n".join([self.formatPost(i) for i in range(330, 375)]),
        #     "\n".join([self.formatPost(i) for i in range(375, 435)]),
        #     "\n".join([self.formatPost(i) for i in range(435, 470)]),
        #     "\n".join([self.formatPost(i) for i in range(470, 494)]),
        # ]
        # chunks = []
        # c = [range(0, 15), range(15, 30), range(30, 45), range(45, 60), range(60, 75), range(75, 90), range(90, 105), range(105, 120), range(120, 135), range(135, 150), range(150, 165), range(165, 180), range(180, 195), range(195, 210), range(210, 225), range(225, 240), range(240, 245), range(245, 255), range(255, 270), range(270, 285), range(285, 300), range(300, 315), range(315, 330), range(330, 345), range(345, 360), range(360, 375), range(375, 390), range(390, 405), range(405, 420), range(420, 435), range(435, 450), range(450, 465), range(465, 480), range(480, 494)]
        # for chunk in c:
        #     chunks.append("\n".join([self.formatPost(i) for i in chunk]))
        
        
        
        # new chunking technique, see self.mergeChunks
           
        # self.tempDisableVerbosity()
        # chunks = [self.formatPost(i) for i in range(494)]
        # chunks = self.mergeChunks(chunks)
        # self.restoreVerbosity()

        # print([i[0] for i in chunks])
        # print(sum([i[0] for i in chunks]), sum([len(i[1]) for i in chunks]))
        # print(sum([i[0] for i in chunks]), sum([len(i[1]) for i in chunks]))
        # print(chunks)
        # exit()
        
        # hello chat
        # errorPosts = [48, 49, 50, 51, 52, 239, 240, 241, 242, 276, 476]
        # # subtract 1 cuz indeces are counted from zero
        # errorPosts = [i-1 for i in errorPosts]
        # errorPosts = [self.formatPost(i) for i in errorPosts]
        # for idx, post in enumerate(errorPosts):
        #     if self.countTokens(post) > 4096:
        #         # break post into chunks of 20 comments
        #         post = post.splitlines()
        #         postHeader = "\n".join(post[:3])
        #         comments = post[3:]
        #         comments = Utils.chunk(comments, 20)
        #         posts = [postHeader + "\n" + "\n".join(chunk) for chunk in comments]
        #         errorPosts.extend(posts)
        #         errorPosts[idx] = ""
        
        # errorPosts = [p for p in errorPosts if p]
        # chunks = errorPosts
        # chunks = self.mergeChunks(chunks, 4096)
        # print(len(chunks))
        # exit()
        # yknow given how short the data is, I don't even gotta use the api
        # simply convert them into 5 prompts
        # actually nvm, too much work
        # apiiii

        # self.gemini = Gemini(os.getenv("GEMINI_KEY"))
        # gemini = self.gemini

        # test
        # symptoms = gemini.extractSymptoms("\n".join([self.formatPost(i) for i in range(000, 5)]))
        # with open("test.json", "w+") as f:
        #     json.dump(symptoms, f)
        # Nice it worked :D, first try aswell, now for everything'

        # for idx, chunk in enumerate(chunks):
        #     if self.verbose:
        #         print(f"Processing chunk {idx+1}...")
        #     try:
        #         symptoms = gemini.extractSymptoms(chunk)
        #     except Exception as e:
        #         print(e)
        #         symptoms = f"Error here, {str(e)}, chunk:\n{chunk}"
            
        #     if self.verbose:
        #         print(f"Chunk {idx+1} processed :D, storing chunk...")

        #     with open(f"chunk-{idx+1}.json", "w+") as f:
        #         # json.dump(symptoms, f)
        #         f.write(symptoms)

        #     if self.verbose:
        #         print(f"Chunk {idx+1} stored :D, waiting 5s...")

        #     time.sleep(5)
        # finally done :D
        # now lets combine the chunks into one
        # posts = []
        # for i in range(195):
        #     with open(os.path.join(Config.SCRIPT_DIR, "processed-anecdotes", f"chunk-{i+1}.json"), "r") as f:
        #         try:
        #             chunk = json.load(f)
        #             posts.extend(chunk["posts"])
        #         except Exception as e:
        #             print("Error in chunk", i+1, "please check manually")

        # with open(os.path.join(Config.SCRIPT_DIR, "processed-anecdotes-combined.json"), "w+") as f:
        #     json.dump(posts, f)
        # Errors discovered in rlly long posts
        """Error in chunk 21 please check manually Deleted entire file, redo posts 48-52

            Error in chunk 87 please check manually  Deleted entire file, redo posts 239
            Error in chunk 88 please check manually  Deleted entire file, redo posts 240
            Error in chunk 89 please check manually     Deleted entire file, redo posts 241 
            Error in chunk 90 please check manually  Deleted entire file, redo posts 242
            Error in chunk 110 please check manually Post 276
            Error in chunk 190 please check manually Post 476
        """
        # I think the solution is the break the comments down into chunks of 20, then attach the post to each chunk, and then rerun that through the AI
        # see line 597 for the updates I made to account for these errors
        # adding those to the ones we got.

        # posts = []
        # for i in range(33):
        #     with open(os.path.join(Config.SCRIPT_DIR, "processed-anecdoes-that-had-errors-but-fixed", f"chunk-{i+1}.json"), "r") as f:
        #         try:
        #             chunk = json.load(f)
        #             posts.extend(chunk["posts"])
        #         except Exception as e:
        #             print("Error in chunk", i+1, "please check manually")

        # with open(os.path.join(Config.SCRIPT_DIR, "processed-anecdoes-total-combined.json"), "w+") as f:
        #     json.dump(posts, f)

        # print(self.countTokens("\n".join([self.formatPost(i) for i in range(000, 494)])))
        # with open(os.path.join(Config.SCRIPT_DIR, "formatted-posts.txt"), "w+") as f:
        #     f.write("\n".join([self.formatPost(i) for i in range(000, 494)]))


# ===== Main Function =====
def main() -> int:
    """Entry point with optional CLI args."""
    verbose = False
    load_dotenv()
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