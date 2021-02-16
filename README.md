# Your Library (documentation)

# Introduction:

* The Your Library is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes.
* you can use our API to Create new Books to your Library, control and organize your library by update or delete books or add new books.
* you can search books or get full pagination list of the books in your library we created this API using Python.


# Getting Started:

* Base URL: localhost://5000/books
* By default, the Your Library Docs demonstrate using curl to interact with the API over HTTP.
* We have no API Keys or Authentication  so the API will accept your request without Authentication and you do not need to create new account to use it.


# Errors:
* Your Library API May return 4 types of errors [404, 422, 400, 405]

### 404:

* JSON response will return and this error happend if resource not found for example request to update/delete book that not exist, or 0 books in the API
* example of the response : 
    ```json
       {
        'code':404,
        'message':'resource not found',
        'success':False
        }
    ```
    
### 422:

* JSON response will return and this error happens if Your API request unprocessable That's mean The API received your request but it could not handle your request
* -- For example, if you delete a book that does not exist, 
* An example of a response: 
    ```json
       {
        'code':422,
        'message':'unprocessable',
        'success':False
        }
    ```
    
### 400:

* JSON response will return and this error happens if you send A bad request the API could not understand it 
* -- For example,  send Not JSON body to the POST / Patch endpoints,
* An example of a response: 
    ```json
       {
        'code':400,
        'message':'bad request',
        'success':False
        }
    ```
    
### 405:
* It's an HTTP response status code that indicates that the request method is known by the server but is not supported by the target resource
* -- For example,  send post request to endpoint that accept only Patch or GET requests
* JSON response will return and this error happens if used A wrong Method in your request 

* An example of a response: 
    ```json
       {
        'code':405,
        'message':'method not allowed',
        'success':False
        }
    ```
    

# Resource endpoint library:

#### All End Points:

# Get books:  
     - How To:
          - URL ```(http://localhost:5000/books) [GET] ```
          
                     - this will return a pagination List For All Books in your Library, it accept 1 query paramter which is page to control pagination.
          - example of CURL request ```curl -X GET 'http://localhost:5000/books' ```
          
                     - example of response:

                       ``` json
                         [
                          {
                            "books": [
                              {
                                "author": "some one",
                                "id": 1,
                                "rating": 4,
                                "title": "Hello World"
                              },
                              {
                                "author": "some one",
                                "id": 2,
                                "rating": 0,
                                "title": "Hello World"
                              },
                              {
                                "author": "some one",
                                "id": 5,
                                "rating": 0,
                                "title": "Hello World"
                              },
                              {
                                "author": "mahmoud",
                                "id": 10,
                                "rating": 3,
                                "title": "Hi"
                              },
                              {
                                "author": "mahmoud",
                                "id": 11,
                                "rating": 3,
                                "title": "Hi"
                              },
                              {
                                "author": "mahmoud",
                                "id": 13,
                                "rating": 3,
                                "title": "Hi"
                              },
                              {
                                "author": "mahmoud",
                                "id": 14,
                                "rating": 3,
                                "title": "Hi"
                              },
                              {
                                "author": "mahmoud",
                                "id": 15,
                                "rating": 3,
                                "title": "Hi"
                              }
                            ],
                            "code": "200",
                            "success": true,
                            "total_books": 75
                          },
                          200
                        ]
                        ```   
                     


# Update books:  
     - How To:
          - URL ```(http://localhost:5000/books/[book_id]) [PATCH] ```
                     - This Endpoint Accept only PATCH request to update an existing book rating you should include the new rating in your request body and convert to json
          - example of CURL request ```curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type:application/json" -d '{"rating":"4"}' ```
                     - example of Success response:
                     
                       ```json
                         [
                          {
                            "books": [
                              {
                                "author": "some one",
                                "id": 1,
                                "rating": 4,
                                "title": "Hello World"
                              },
                        ```
                     - example of Falid response:

                       ```json
                         [
                          {
                             "code": 400,
                             "message": "bad request",
                             "success": false
                           }
                        ```
