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

2. 🔄 **Step 2: Symptom Extraction** - In Progress
   - Using Google's Gemini AI to extract symptoms from patient anecdotes
   - Categorizing symptoms as "minor" (initially dismissed) or "major" (prompted immediate concern)
   - Tracking when symptoms appeared and how patients initially perceived them
   - Also extracting lifestyle and behavioral changes mentioned

### Data Scale:
- Total Posts: 494
- Total Comments: 12,499 (first-level only)
- Total Tokens: ~1.2 million
- Average Tokens Per Post: ~465
- Average Comments Per Post: ~25
- Average Tokens Per Comment: ~78

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

The symptom extraction process involves:
1. Formatting posts and comments into a structured format
2. Chunking data to fit within AI context windows
3. Processing through Gemini AI with a specialized prompt
4. Storing extracted symptoms in a structured JSON format

## Project Goals

The ultimate aim of this project is to create a free, accessible tool that can help identify cancer risk factors earlier than traditional methods. By analyzing a large dataset of patient experiences, we hope to uncover subtle patterns that might otherwise be missed.

## Disclaimer

This project is for research purposes and is not intended to replace professional medical advice or diagnosis. Always consult with healthcare professionals regarding any health concerns.


Made with &#x2764; by MaxDevv :D