import unittest
import httpx


class RequestAdapter:
    def __init__(self, host_url):
        self.session = httpx.Client()
        self.host_url = host_url
        self.api = ""
        self.req_body = {}
        self.method = "GET"

    def build_request(
        self,
    ):
        request = self.session.build_request(
            method=self.method, url=f"{self.host_url}/{self.api}", json=self.req_body
        )
        return request

    def set_api(self, api):
        self.api = api
        return self

    def set_req_body(self, body):
        self.req_body = body
        return self

    def set_method(self, method):
        if method.lower() not in ["post", "get", "put", "delete" "patch", "trace"]:
            raise NotImplementedError
        self.method = method.upper()
        return self

    def send(self):
        request = self.build_request()
        response = self.session.send(request)
        return response.json()





class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host_url = "http://127.0.0.1:8000"
        cls.username = "admin"
        cls.password = "1234567"
        cls.fetcher = RequestAdapter(cls.host_url)

    def test_login(self):
        api = "login"
        response = (
            self.fetcher.set_api(api)
            .set_method("get")
            .set_req_body({"username": "admin", "password": "1234567"})
            .send()
        )

        assert response["code"] == 0
        assert response["message"] == "success"
        assert response["data"]
        assert response["data"]["token"]

        self.assertEqual(len(response["data"]["token"]), 14)

        response = self.fetcher.set_req_body({"": "", "passwrod": ""}).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "empty username")
        self.assertFalse(response.get("data"))

        response = self.fetcher.set_req_body(
            {"username": "aksdja", "password": ""}
        ).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "empty password")
        self.assertFalse(response.get("data"))

        response = self.fetcher.set_req_body(
            {"username": "aksdja", "password": "aksdjaklsjd"}
        ).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "wrong account info")
        self.assertFalse(response.get("data"))

    def test_signup(self):
        api = "signup"
        method = "POST"

        response = (
            self.fetcher.set_api(api)
            .set_method(method)
            .set_req_body({"username": "guest", "password": "7777777"})
            .send()
        )

        self.assertEqual(response["code"], 0)
        self.assertEqual(response["message"], "success")

        response = self.fetcher.set_req_body({"username":"askjda"}).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "fields should not empty")

        response = self.fetcher.set_req_body({"username":"adminnn", "password": ""}).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "fields should not empty")

        response = self.fetcher.set_req_body({"username":"admin", "password": ""}).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "fields should not empty")

        response = self.fetcher.set_req_body({"username":"admin", "password": "aksdj"}).send()
        self.assertEqual(response["code"], 101)
        self.assertEqual(response["message"], "username already exists")

if __name__ == "__main__":
    unittest.main()
