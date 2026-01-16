import pytest

def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "Hello World"

def test_route_overlap_throws_exception(api):
    @api.route("/test")
    def home(req, resp):
        resp.text = "First handler"

    # Test that duplicate route raises AssertionError
    with pytest.raises(AssertionError):
        @api.route("/test")
        def home2(req, resp):
            resp.text = "Second handler"

def test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "Hello from test client"

    @api.route("/test")
    def test_handler(req, resp):
        resp.text = RESPONSE_TEXT

    response = client.get("http://testserver/test")
    assert response.text == RESPONSE_TEXT

def test_parameterized_route(api, client):
    @api.route("/hello/{name}")
    def hello(req, resp, name):
        resp.text = f"Hello {name}"

    # Test multiple parameter values
    assert client.get("http://testserver/hello/Alice").text == "Hello Alice"
    assert client.get("http://testserver/hello/Bob").text == "Hello Bob"
    assert client.get("http://testserver/hello/Charlie").text == "Hello Charlie"

def test_default_404_response(client):
    response = client.get("http://testserver/nonexistent")
    
    assert response.status_code == 404
    assert response.text == "Not found."

def test_class_based_handler_get(api, client):
    response_text = "This is a GET request"

    @api.route("/books")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    response = client.get("http://testserver/books")
    assert response.text == response_text

def test_class_based_handler_post(api, client):
    response_text = "This is a POST request"

    @api.route("/books")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    response = client.post("http://testserver/books")
    assert response.text == response_text

def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/books")
    class BookResource:
        def post(self, req, resp):
            resp.text = "Only POST allowed"

    # This should raise AttributeError (method not implemented)
    with pytest.raises(AttributeError):
        client.get("http://testserver/books")
