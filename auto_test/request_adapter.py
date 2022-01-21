import httpx


class RequestAdapter:
    def __init__(self):
        self.session = httpx.Client()
        self.host_url = ""
        self.api = ""
        self.req_body = {}
        self.method = "GET"

    def set_host(self, host):
        self.host_url = host
        return self

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
