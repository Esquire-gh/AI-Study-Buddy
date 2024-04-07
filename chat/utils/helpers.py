import logging
import requests
import os
import json

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


def get_course_files(courses, chat=None):
    course_files = []

    for course in courses:
        course_dict = {
            "course_id": course.id,
            "course_name": course.name,
            "files": []
        }

        for file in course.coursefile_set.all():
            selected = False

            if chat and chat.indexed_file_ids and file.id in json.loads(chat.indexed_file_ids):
                selected = True

            course_dict["files"].append(
                {
                    "id": file.id,
                    "name": file.name,
                    "url": file.url,
                    "selected": selected
                }
            )
        course_files.append(course_dict)

    return course_files