import os, typing
from dotenv import load_dotenv
load_dotenv()

# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
# language_key = str(os.environ.get('LANGUAGE_KEY'))
# language_endpoint = str(os.environ.get('LANGUAGE_ENDPOINT'))

from azure.ai.textanalytics import TextAnalyticsClient, RecognizeEntitiesResult
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["LANGUAGE_ENDPOINT"]
key = os.environ["LANGUAGE_KEY"]

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
reviews = [
    """I work for Foo Company, and we hired Contoso for our annual founding ceremony. The food
    was amazing and we all can't say enough good words about the quality and the level of service.""",
]

result: list[RecognizeEntitiesResult] = text_analytics_client.recognize_entities(reviews)
result: list[RecognizeEntitiesResult] = [review for review in result if not review.is_error]

for review in result:
    print(review.entities)
    for entity in review.entities:
        print(f"Entity: '{entity.text}' has category '{entity.category}'")