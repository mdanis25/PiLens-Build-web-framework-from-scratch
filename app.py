from PiLensframe.api import API 
 

app = API()


# Function-based handlers (existing)
@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"
    

# Class-based handler (new!)
@app.route("/books")
class BooksResource:
    def get(self, request, response):
        response.text = "List all books"
    
    def post(self, request, response):
        response.text = "Create a new book"

@app.route("/users/{id:d}")
class UserResource:
    def get(self, request, response, id):
        response.text = f"Get user {id}"
    
    def put(self, request, response, id):
        response.text = f"Update user {id}"
    
    def delete(self, request, response, id):
        response.text = f"Delete user {id}"
        