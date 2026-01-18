import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def register(self, username, password):
        url = f"{self.base_url}/register"
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=payload)
        print("Register status:", response.status_code)

    def login(self, username, password):
       url = f"{self.base_url}/login"
       response = requests.post(url, auth=(username, password))

       if response.status_code != 200:
           raise Exception(f"Login failed: {response.status_code} - {response.text}")

       data = response.json()
       self.token = data["token"]
       print("Login successful, token received")


    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._headers())
        return response.json()

    def put(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=payload, headers=self._headers())
        return response.json()
