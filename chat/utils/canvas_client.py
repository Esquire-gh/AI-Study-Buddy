import requests


class CanvasClient:
    BASE_URL = "https://morganstate.instructure.com/api/v1/"

    def __init__(self, access_token):
        self.canvas_token = access_token

    def courses(self):
        endpoint = 'courses'
        return self._make_request(endpoint)

    def course_files(self, course_id, file_type="application/pdf"):
        endpoint = f"courses/{course_id}/files?content_types={file_type}"
        return self._make_request(endpoint)

    def _make_request(self, endpoint):
        headers =  {
            "Authorization": f"Bearer {self.canvas_token}"
        }
        return requests.get(self.BASE_URL + endpoint,  headers=headers)


def get_canvas_client(user):
    return CanvasClient(user.userprofile.canvas_api_token)
