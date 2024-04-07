import logging
import requests
import os

from django.conf import settings


def download_file(url, filename):
    try:
        fp = "downloads/" + filename
        response = requests.get(url, stream=True)

        # Check if the request was successful and the content is a PDF
        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            with open(fp, 'wb') as f:
                f.write(response.content)
            logging.info(f"PDF successfully downloaded and saved as '{filename}'")
        else:
            logging.error("The URL does not contain a valid PDF.")

        absolute_path = os.path.abspath(fp)
        logging.info(f"PDF successfully downloaded and saved as '{absolute_path}'")
        return absolute_path
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}", exc_info=e)


def get_openai_embeddings():
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)