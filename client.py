import httplib2

HTTP_OK = 200

class Client:
    _headers: str
    _http: httplib2.Http
    _user_name: str
    _password: str

    def connect(self, user_name: str, password: str) -> bool:
        self._headers = {"Content-Type": "application/json", "Origin": "https://ticktick.com"}
        url = "https://api.ticktick.com/api/v2/user/signon?wc=true&remember=true"
        self._http = httplib2.Http('.cache')

        self._user_name = user_name
        self._password = password
        body = '{"username":"%s","password":"%s"}' % (user_name, password)
        response, content = self.post(url, body)

        if response.status == HTTP_OK:
            self._headers.update({'Cookie': response['set-cookie']})
            print('Connected')
            return True
        else:
            print('Connect error:')
            print(response)
            print(content)
            return False

    def reconnect(self) -> bool:
        print('try reconnect...')
        return self.connect(self._user_name, self._password)

    def post(self, url: str, body: dict) -> (any, any):
        return self._request("POST", url, body)

    def get(self, url: str) -> (any, any):
        return self._request("GET", url, None)

    def _request(self, method, url: str, body: dict) -> (any, any):
        response, content = self._http.request(
            uri=url,
            method=method,
            body=body,
            headers=self._headers
        )
        return response, content
