import numpy as np
from sentence_transformers import SentenceTransformer
import joblib
import pandas as pd
import os

# Exception handling for model and library loading
try:
    # Load Sentence-BERT model
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your Sentence-BERT model

    # Load trained XGBoost model and MultiLabelBinarizer
    xgb_model = joblib.load("xgb_model.pkl")  # Replace with your model file
    mlb = joblib.load("mlb.pkl")             # Replace with your saved MultiLabelBinarizer
except Exception as e:
    print(f"Error loading models: {e}")
    exit()

# Load your dataset
try:
    df = pd.read_csv("preprocessed_data.csv")  # Replace with your actual dataset file
except FileNotFoundError:
    print("Error: Dataset file not found. Please provide the correct path.")
    exit()
except Exception as e:
    print(f"Error reading dataset: {e}")
    exit()

# Output and error files
output_file = "predicted_similar_problems.txt"
error_file = "errors_log.txt"

# Open the files to save results and errors
with open(output_file, "w") as file, open(error_file, "w") as error_log:
    for idx in range(len(df)):
        try:
            print(f"Processing index: {idx}")

            # Extract inputs for the current index
            sample_title = df["title"].iloc[idx]
            sample_topic_tag = df["topic_tags"].iloc[idx]
            sample_description = df["problem_description"].iloc[idx]
            sample_id = df["id"].iloc[idx]

            # Check for missing or invalid inputs
            if not isinstance(sample_title, str) or not isinstance(sample_topic_tag, str) or not isinstance(sample_description, str):
                raise ValueError(f"Missing or invalid data at index {idx}")

            # Generate weighted Sentence-BERT embeddings
            title_embedding = sbert_model.encode([sample_title], normalize_embeddings=True) * 0.35
            tags_embedding = sbert_model.encode([sample_topic_tag], normalize_embeddings=True) * 0.35
            description_embedding = sbert_model.encode([sample_description], normalize_embeddings=True) * 0.3

            # Combine weighted embeddings
            combined_embedding = np.hstack([title_embedding, tags_embedding, description_embedding])

            # Predict using the trained model
            model_pred = xgb_model.predict(combined_embedding)
            model_predicted_labels = mlb.inverse_transform(model_pred)

            # Format and save the output
            output_line = f"Index: {idx}, ID: {sample_id}, Predicted Similar Problems: {model_predicted_labels}\n"
            print(output_line)
            file.write(output_line)

        except Exception as e:
            # Log errors for the current index
            error_message = f"Error at Index: {idx}, ID: {sample_id if 'sample_id' in locals() else 'N/A'} - {e}\n"
            print(error_message)
            error_log.write(error_message)

print(f"All predictions have been saved to {output_file}")
print(f"Any errors have been logged to {error_file}")
