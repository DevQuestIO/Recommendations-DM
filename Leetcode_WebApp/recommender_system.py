import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import requests
import streamlit as st

current_directory = Path(__file__).resolve().parent
csv_file_path = current_directory / "preprocessed_data.csv"

# Constants
ACCEPTANCE_WEIGHT = 0.3
ENGAGEMENT_WEIGHT = 0.5
SUBMISSION_WEIGHT = 0.2
SMOOTHING_FACTOR = 100000


class TextProcessor:
    def __init__(self, text_data):
        self.text_data = text_data
        self.text_preprocessor = TfidfVectorizer(stop_words="english")

    def preprocess_text_data(self):
        self.text_data.fillna("", inplace=True)
        return self.text_preprocessor.fit_transform(self.text_data)


class PopularityCalculator:
    def __init__(self, acceptance, engagement, submission):
        self.acceptance = acceptance
        self.engagement = engagement
        self.submission = submission

    def calculate_engagement_score(self):
        total_engagement = (
            self.acceptance.fillna(0) + self.engagement.fillna(0) + SMOOTHING_FACTOR
        )
        max_engagement = total_engagement.max()
        return total_engagement / max_engagement

    def normalize_series(self, series):
        return (series - series.min()) / (series.max() - series.min())

    def calculate_popularity_score(self):
        return (
            self.normalize_series(self.acceptance) * ACCEPTANCE_WEIGHT
            + self.normalize_series(self.engagement) * ENGAGEMENT_WEIGHT
            + self.normalize_series(self.submission) * SUBMISSION_WEIGHT
        )


class ProblemRecommender:
    @staticmethod
    def recommend_similar_problems(df, problem_id, X_processed, n=10):
        idx = df[df["id"] == problem_id].index
        if len(idx) == 0:
            return pd.DataFrame()  # Return empty DataFrame if problem_id is not found
        idx = idx[0]
        sim_scores = cosine_similarity(X_processed[idx], X_processed).flatten()
        sim_scores[idx] = 0
        sim_indices = sim_scores.argsort()[-n:][::-1]
        return df.iloc[sim_indices]

    @staticmethod
    def recommend_top_problems(df, n=10):
        return df.sort_values(by="popularity_score", ascending=False).head(n)


def initialize_sync(username):
    API_BASE_URL = "http://127.0.0.1:8000"

    sync_url = f"{API_BASE_URL}/api/v1/sync/{username}?username={username}"

    headers = {
        "Content-Type": "application/json",
        "x-csrftoken": "your-csrf-token",
    }

    try:
        response = requests.post(sync_url, timeout=30)

        if not response.ok:
            print("Failed to start sync:", response.status_code, response.text)
            return None

        data = response.json()
        task_id = data.get("task_id")
        stats = data.get("stats")

        if stats:
            return stats
        else:
            return task_id

    except requests.RequestException as e:
        print("Sync initialization failed:", str(e))
        return None


def fetch_last_solved_titleSlug(username, limit):
    """
    Fetch the solved question slugs of a particular user using LeetCode GraphQL API.

    Args:
        username (str): The LeetCode username.
        offset (int): Pagination offset (default: 0).
        limit (int): Number of solved questions to fetch (default: 10).

    Returns:
        list: A list of question slugs solved by the user.
    """
    url = "https://leetcode.com/graphql"

    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
    """
    payload = {
        "operationName": "recentAcSubmissions",
        "variables": {"username": username, "limit": limit},
        "query": query,
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        recent_submissions = response.json()["data"]["recentAcSubmissionList"]
        if recent_submissions:
            return recent_submissions[0]["titleSlug"]
        else:
            print("No recent submissions found.")
    else:
        raise Exception(
            f"Failed to fetch solved questions: {response.status_code}, {response.text}"
        )


def fetch_frontend_questionID(title_slug):
    url = "https://leetcode.com/graphql"

    query = """
    query questionTitle($titleSlug: String) {
      question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        titleSlug
        isPaidOnly
        difficulty
        likes
        dislikes
      }
    }
    """

    payload = {
        "operationName": "questionTitle",
        "variables": {"titleSlug": title_slug},
        "query": query,
    }

    response = requests.post(url, json=payload, timeout=30)
    # Debug prints (remove in production)

    if response.status_code == 200 and "errors" not in response.json():
        # Extract the frontend question ID
        frontend_id = response.json()["data"]["question"]["questionFrontendId"]
        return int(frontend_id)
    else:
        raise Exception(f"Fetching suggestions")


def recommender_system(username):
    df = pd.read_csv(csv_file_path)
    df["topic_tags"] = df["topic_tags"].str.replace("'", "")

    text_processor = TextProcessor(df["problem_description"])
    X_processed = text_processor.preprocess_text_data()

    popularity_calculator = PopularityCalculator(
        df["acceptance"], df["likes"], df["submission"]
    )
    df["popularity_score"] = popularity_calculator.calculate_popularity_score()

    # data = initialize_sync(username)

    problem_id = 0
    if username:
        title_slug = fetch_last_solved_titleSlug(username, 1)
        if title_slug:
            try:
                problem_id = fetch_frontend_questionID(title_slug)
                # st.write("Problem ID:", problem_id)
                content_based_recommendations = (
                    ProblemRecommender.recommend_similar_problems(
                        df, problem_id=problem_id, X_processed=X_processed
                    )
                )
                popularity_based_recommendations = (
                    ProblemRecommender.recommend_top_problems(
                        content_based_recommendations
                    )
                )
                return popularity_based_recommendations[
                    ["title", "difficulty", "topic_tags", "problem_URL"]
                ]
            except Exception as e:
                st.error(str(e))
                pd.DataFrame()
        else:
            st.write("No recent submissions found for this user.")
            pd.DataFrame()
    else:
        st.write("Please enter a username above.")
        pd.DataFrame()
