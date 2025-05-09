# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# """
# Module Description
# ------------------
# A brief description of what this module/script does.
# """

import sys
from typing import Optional, Any
from numba import jit
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

# # ===== Configuration =====
# class Config:
#     """Global settings (variables instead of constants)."""
#     defaultValue = 42
#     verbose = True
#     UseArgParse = True  # Enable to activate CLI parsing
#     SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# class Utils:
#     def chunkArr(self, lst, n):
#         """Yield successive n-sized chunks from lst."""
#         for i in range(0, len(lst), n):
#             yield lst[i:i + n]


# # ===== Numba-Accelerated Functions =====
# @jit(nopython=True)
# def fastSquare(x: float) -> float:
#     """Compute x² (optimized with Numba)."""
#     return x * x

# # ===== Main Class =====
# class MainClass:
#     """
#     Core processing class with configurable workflow.
#     """

#     def __init__(self, verbose: bool = False):
#         self.verbose = verbose
#         self.result = None
#     '''
#     # ==== Function Boilerplate ====
#     def func(self, variable: int = 69) -> None:
#         """
#         Description:
#             - Describe this function
#         Args:
#             - variable,  an int representing a variable
#         """
#         if self.verbose:
#             print("Initializing processor...")
#     '''
#     def run(self) -> None:
#         """
#         Description:
#             - The main logic for this module.
#         Args:
#             - An imaginary argument
#         """
        
#         pass

# # ===== Main Function =====
# def main() -> int:
#     """Entry point with optional CLI args."""
#     verbose = False

#     # ===== Optional CLI =====
#     if Config.UseArgParse:
#         import argparse
#         parser = argparse.ArgumentParser(description="MainClass runner.")
#         parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug mode")
#         args = parser.parse_args()
#         verbose = args.verbose

#     # Run processor
#     processor = MainClass(verbose=(verbose or Config.verbose))
#     return processor.run()

# if __name__ == "__main__":
#     sys.exit(main())

texts = ["banana muffins? ", "banana bread? banana muffins?"]
# The dimensionality of the output embeddings.
dimensionality = 256
# The task type for embedding. Check the available tasks in the model's documentation.
task = "SEMANTIC_SIMILARITY"

model = TextEmbeddingModel.from_pretrained("text-embedding-005")
inputs = [TextEmbeddingInput(text, task) for text in texts]
kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
embeddings = model.get_embeddings(inputs, **kwargs)

print(embeddings)
