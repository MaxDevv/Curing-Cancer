# Curing Cancer Project

## Overview

This project aims to develop a data-driven approach to early cancer detection by analyzing anecdotal evidence from cancer patients. The goal is to identify subtle, early warning signs that might be overlooked by traditional diagnostic methods, ultimately creating a free, accessible tool for cancer risk assessment.

## Current Status: Work in Progress

This project is currently in active development. We have completed the initial data collection phase and are now in the process of extracting and analyzing symptoms from patient anecdotes.

### Progress So Far:

1. ✅ **Step 1: Data Collection** - Completed on April 15, 2025
   - Successfully extracted 494 posts and 12,499 first-level comments from the r/cancer subreddit
   - Used search terms like "how found", "my story", "signs I ignored", and "what symptoms"
   - Data stored in JSON format for further processing

2. ✅ **Step 2: Symptom Extraction** - Completed on April 23, 2025
   - Used Google's Gemini AI to extract symptoms from patient anecdotes
      - Categorized symptoms as "minor" (initially dismissed) or "major" (prompted immediate concern)
      - Tracked when symptoms appeared and how patients initially perceived them
      - Also extracted lifestyle and behavioral changes mentioned
   - Encountered and resolved issues with processing larger posts (posts #48-52, #239-242, #276, #476

### Data Scale:
- Total Posts: 494
- Total Comments: 12,499 (first-level only)
- Total Tokens: ~1.2 million
- Average Tokens Per Post: ~465
- Average Comments Per Post: ~25
- Average Tokens Per Comment: ~78
## Progress Report

### Development Timeline

#### April 23, 2025
- Completed Step 3: Symptom Reduction and Categorization
- Extracted symptoms from the combined JSON data
- Implemented text normalization to reduce duplicate symptoms
- Reduced symptom count from 1697 to 1167 through deduplication
- Reformatted symptoms into standardized question format for questionnaire development
- Used AI to rewrite symptoms into clear, medically appropriate terminology

#### April 17, 2025
- Combined and fixed errors in anecdotes, merging them into one comprehensive source
- Implemented chunk merging functionality to optimize processing
- Added error handling for exceptionally long posts by splitting them into smaller comment chunks
- Successfully completed Step 2 of the project plan

#### April 16, 2025
- Added project README documentation
- Completed extraction of symptoms using AI processing
- Created backup of processed data before final combination
- Successfully got processing pipeline working after multiple iterations
- Generated formatted posts for AI processing
- Added statistics about data scale and processing requirements

#### April 15, 2025
- Downloaded approximately 500 posts with 12,500 comments making up 13000 anecdotes from Reddit for symptom identification
- Transformed anecdotes into structured JSON format
- Completed Step 1 of the project plan (Data Collection)
- Made initial project commit and repository setup

### Data Collection Phase
- Set up Reddit API access using PRAW
- Implemented search functionality targeting the r/cancer subreddit
- Used "how found" as the primary search term to gather relevant anecdotes
- Added error handling and rate limiting to comply with API restrictions
- Successfully extracted 494 posts with their associated comments
- Stored raw data in JSON format for further processing

### Symptom Extraction Phase
- Developed a token counting system to manage AI context window limitations
- Implemented text cleaning functions to handle special characters and emojis
- Created a chunking system to process large posts within AI token limits
- Integrated Google's Gemini AI with a specialized medical research prompt
- Structured output in JSON format with detailed symptom categorization
- Identified and resolved issues with processing exceptionally large posts (posts #48-52, #239-242, #276, #476)
- Implemented a solution to break down large comment sections into manageable chunks
- Combined processed chunks into a comprehensive dataset

### Symptom Reduction Phase
- Extracted all symptoms from the processed anecdotes
- Implemented text normalization to remove punctuation and standardize case
- Successfully reduced symptom count from 1697 to 1167 through deduplication
- Created a standardized question format for each symptom:
  "On a scale of 1-10, how severely have you experienced an abnormal onset or worsening of this symptom within the last 6 months: {symptom}"
- Used AI to reformat symptoms into clear, medically appropriate terminology
- Stored the reduced symptom list for questionnaire development

### Technical Challenges Overcome
- Managed token limitations of AI models by implementing dynamic chunking
- Developed a merging algorithm to optimize chunk sizes while staying within token limits
- Handled special characters and emoji cleaning to ensure text compatibility
- Implemented error recovery for failed processing attempts
- Created a system to track and reprocess problematic posts
- Addressed overloaded model errors by reducing chunk sizes and implementing wait periods
- Developed efficient symptom deduplication techniques

## Planned Next Steps:

3. **Step 3: Symptom Reduction and Categorization**
   - Group similar symptoms to create a manageable dataset

4. **Step 4: Questionnaire Development**
   - Create a comprehensive questionnaire (100-1000 questions) based on extracted symptoms

5. **Step 5: Data Collection from Diverse Demographics**
   - Gather responses from both cancer patients and non-cancer individuals
   - Ensure diversity in economic, racial, and geographical demographics

6. **Step 6: AI Model Training**
   - Train an AI model to identify patterns in symptoms and lifestyle factors

7. **Step 7: Questionnaire Optimization**
   - Use AI insights to refine the questionnaire

8. **Step 8: Public Release**
   - Develop a completely free website for cancer risk assessment

9. **Step 9: Medical Collaboration**
   - Partner with medical institutions to validate and improve the model

10. **Step 10: Project Completion**
    - Finalize and maintain the tool for public benefit

## Technical Implementation

The project uses Python with several key libraries:
- PRAW for Reddit API access
- Google's Gemini AI for natural language processing
- JSON for data storage and manipulation
- VertexAI tokenization for token counting
- Regular expressions for text cleaning

The symptom extraction process involves:
1. Formatting posts and comments into a structured format
2. Chunking data to fit within AI context windows (targeting ~6144 tokens per chunk)
3. Processing through Gemini AI with a specialized prompt
4. Storing extracted symptoms in a structured JSON format
5. Combining processed chunks into a comprehensive dataset

## Project Goals

The ultimate aim of this project is to create a free, accessible tool that can help identify cancer risk factors earlier than traditional methods. By analyzing a large dataset of patient experiences, we hope to uncover subtle patterns that might otherwise be missed.

## Disclaimer

This project is for research purposes and is not intended to replace professional medical advice or diagnosis. Always consult with healthcare professionals regarding any health concerns.



Made with &#x2764; by MaxDevv :D
