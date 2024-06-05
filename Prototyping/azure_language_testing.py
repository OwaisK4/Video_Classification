import os, typing
from dotenv import load_dotenv
load_dotenv()
from azure.ai.textanalytics import TextAnalyticsClient, RecognizeEntitiesResult
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["LANGUAGE_ENDPOINT"]
key = os.environ["LANGUAGE_KEY"]

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
reviews = ["Hey, the fellow travelers Mark here with Walters World and say we're here in Toronto, Canada."
, "And today we're going to talk about are some of the domes that tours should know before they come to Toronto"
, "so they can have a great time. And my first dump for you is don't add that second tee to Toronto"]
# reviews = []
# with open("Output.txt", "r") as f:
#     for line in f:
#         reviews.append(line.strip())
# print(reviews)
results = []

for i in range(0, len(reviews), 5):
    k = min(i + 5, len(reviews))
    result = text_analytics_client.recognize_entities(reviews[i:k])
    result = [review for review in result if not review.is_error]
    results += result

for review in results:
    print(review.entities)
    for entity in review.entities:
        print(f"Entity: '{entity.text}' has category '{entity.category}'")