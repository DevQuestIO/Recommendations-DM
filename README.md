# LeetCode Problem Recommender System

## Overview
LeetCode is a popular platform for enhancing coding and algorithmic skills, especially for technical interview preparation. With over 3,000 programming challenges, users often find it difficult to select the right problems that align with their learning goals and expertise. This project leverages data analysis and recommender systems to guide users in choosing LeetCode problems tailored to their needs.

## Core Objective
**Primary Goal:** Enhance user experience by providing personalized problem recommendations based on user performance and problem popularity.

## Features
- **Data Acquisition:** Extracts comprehensive problem details from LeetCode, including titles, descriptions, difficulty levels, topic tags, and engagement metrics.
- **Data Preprocessing:** Cleans and formats the data to ensure consistency and usability for analysis.
- **Exploratory Data Analysis (EDA):** Identifies patterns and trends within the dataset to inform recommendation algorithms.
- **Recommender System:** Suggests tailored problem sets to users based on their recent submissions and problem popularity.
- **Interactive Dashboard:** Offers a user-friendly interface built with Streamlit, allowing users to input their LeetCode username and receive personalized recommendations.

## Data Collection
Data was sourced by scraping approximately 60 pages on LeetCode, encompassing around 3,000 problems. Key attributes collected include:
- **Problem Details:** Title, description, difficulty level, and URLs.
- **Engagement Metrics:** Acceptance rates, submission counts, likes, dislikes, and discussion counts.
- **Additional Information:** Topic tags, premium status, and related problems.

## Data Preparation
The collected data underwent several preprocessing steps to ensure quality and relevance:
- **Handling Missing Values:** Filled or imputed missing data points to maintain dataset integrity.
- **Feature Engineering:** Created new features such as `popularity_score` by combining acceptance rates, likes, and submissions.
- **Data Formatting:** Converted data types for consistency and optimized the dataset for analysis and modeling.

## Recommender System
The recommender system operates on a hybrid approach:
- **Content-Based Filtering:** Utilizes TF-IDF vectorization of problem descriptions to find similarities between problems.
- **Popularity-Based Ranking:** Sorts problems based on a calculated `popularity_score` to prioritize highly engaged challenges.
- **Hybrid Recommendations:** Combines both approaches to deliver balanced and relevant problem suggestions.

## Interactive Dashboard
Built with Streamlit, the dashboard provides an intuitive interface for users to interact with the recommender system:
- **User Input:** Users enter their LeetCode username to fetch their recent submissions.
- **Recommendations Display:** Presents recommended problems with details such as title, difficulty, topic tags, and direct links to the problem.
- **Error Handling:** Gracefully manages scenarios like invalid usernames or absence of recent submissions, providing clear feedback to the user.

## Installation
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/leetcode-recommender.git
    cd leetcode-recommender
    ```
## Usage
1. **Run the Streamlit App:**
    ```bash
    streamlit run main.py
    ```
2. **Interact with the Dashboard:**
    - Enter your LeetCode username in the input field.
    - View personalized problem recommendations based on your recent activity and problem popularity.

## Error Handling
The application includes robust error handling to ensure a smooth user experience:
- **Invalid Inputs:** Checks for empty or invalid usernames before processing.
- **API Errors:** Handles API request failures gracefully, informing users of connectivity issues or invalid responses.
- **Data Integrity:** Ensures that all required data fields are present before generating recommendations to avoid runtime errors.

## Future Directions
- **Enhanced Personalization:** Incorporate user behavior data to refine recommendation accuracy.
- **Advanced NLP Techniques:** Utilize more sophisticated natural language processing methods to better match user interests with problem statements.
- **Continuous Data Updates:** Implement automated data scraping and updating mechanisms to keep the dataset current with LeetCode’s evolving problem library.
- **Expanded Features:** Add functionalities such as progress tracking, bookmark capabilities, and personalized study plans.

## Conclusion
This project simplifies the problem selection process on LeetCode by offering data-driven, personalized recommendations. Users can efficiently navigate through thousands of problems, focusing on challenges that best fit their skill levels and learning objectives. Future enhancements aim to further personalize and enrich the user experience, making LeetCode an even more effective tool for coding practice and interview preparation.

---
