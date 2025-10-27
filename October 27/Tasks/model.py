from transformers import pipeline

# Load the sentiment-analysis pipeline from Hugging Face
classifier = pipeline('sentiment-analysis')

# Example text to classify
text = "I love this product! It's amazing."

# Get the prediction
result = classifier(text)

# Output the result
print(result)
