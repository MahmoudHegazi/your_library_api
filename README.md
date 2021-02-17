# Your Library API (documentation)

# Introduction:

* The Your Library is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes.
* you can use our API to Create new Books to your Library, control and organize your library by update or delete books or add new books.
* you can search books or get full pagination list of the books in your library we created this API using Python Flask.


# Getting Started:

* Base URL: localhost://5000/books
* By default, the Your Library Docs demonstrate using curl to interact with the API over HTTP.
* We have no API Keys or Authentication  so the API will accept your request without Authentication and you do not need to create new account to use it.
* In this API, you will find a setting for 2 Mobile SMS API which you can use in your app and flask-mail to send mails using your gmail account.
* in order to use the Mobile SMS you have to visit twilio or vonage to get your own API key and API pass and token in twilio.

## how to set up the local development 

* on Windows: Download GitBash, open it, ```cd [project_folder]``` run these 3 commands 
* ``` export FLASK_APP=flaskr ```
* ``` export FLASK_ENV=development ```
* ``` flask run ```
* For Linux users, you can use the same three commands to start the API

# Acknowledgements:

* https://udacity.com (advanced track)
* https://twilio.com
* https://www.vonage.co.uk/


# Errors:
* Your Library API May return 4 types of errors [404, 422, 400, 405]

### 404 Resource Not Found:

* JSON response will return and this error happend if resource not found for example request to update/delete book that not exist, or 0 books in the API
* example of the response : 
    ```json
       {
        'code':404,
        'message':'resource not found',
        'success':False
        }
    ```
    
### 422 Unprocessable:

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
    
### 400 Bad Request:

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
    
### 405 Method not allowed:
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
          - URL: http://localhost:5000/books  [GET]
                     - this will return a pagination List of group number of 8 For All Books in your Library, it accept 1 query parameter
                     which is page start from 1 to control pagination.
                     
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
                        
                   -- adding page paramter in your URL
                   -- example : curl -X GET 'http://localhost:5000/books?page=1'
                   --- success response 
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
                          "id": 16,
                          "rating": 5,
                          "title": "Into To HTML"
                        }
                      ],
                      "code": "200",
                      "success": true,
                      "total_books": 77
                    },
                    200
                  ]
                   
                        
                   - example unsuccess responses
                       if there are 0 books in your libarary it will return 404 not empty list for better handle
                       
                       ```json
                         {
                           "code": 404,
                           "message": "resource not found",
                           "success": false
                         }
                        ```
                        
                       ```json
                         {
                           "code": 405,
                           "message": "method not allowed",
                           'success': false
                         }
                        ```                   
                     


# Update books:  
     - How To:
          - URL (http://localhost:5000/books/[book_id]) [PATCH]
          
                     - This Endpoint Accept only PATCH request to update an existing book rating you should include the new rating in your request body and convert to json
                     
          - example of CURL request ```curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type:application/json" -d '{"rating":"4"}' ```
                     - example of Success response:
                     
                       ```json
                          }
                         "book_rating": 4,
                          "code": 200,
                          "id": 15,
                          "success": true
                          }
                        ```
                     - example of Falid response:

                       ```json
                          {
                             "code": 400,
                             "message": "bad request",
                             "success": false
                           }
                        ```
                        
                        
# Delete books:  
     - How To: curl -X DELETE http://127.0.0.1:5000/books/[book_id]
          - URL (http://127.0.0.1:5000/books/[15]) [DELETE]
          
                     - The book's identifier (ID) must be included in the URL 
                     - Usage: delete an existing book
                     
          - example of CURL request 
                    curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type:application/json" -d '{"rating":"4"}'
                     - example of Success response:
                     
                       ```json
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
                               "id": 16,
                               "rating": 5,
                               "title": "Into To HTML"
                             }
                           ],
                           "code": 200,
                           "deleted": 15,
                           "success": true,
                           "total_books": 74
                         }
                        ```
                     - example of Falid response:

                       ```json
                         {
                           "code": 405,
                           "message": "method not allowed",
                           "success": false
                         }
                        ```
                        
                       ```json
                         {
                           "code": 422,
                           "message": "unprocessable",
                           'success': false
                         }
                        ```
                        
                        
 # ADD books/ Search Book by title:  
     - How To: curl -X DELETE http://localhost:5000/books
          - URL (http://127.0.0.1:5000/books/) [POST]
          
                     - This Endpoint Accept only POST request to Add New Book OR search for A book using title it accept JSON body
                     - JSON body should Include at least 1 of this to continue your Request ['search', 'title','author','rating'] else it will return 404 Error
                     
          - example of CURL request To create new Book
               curl -X POST 'http://localhost:5000/books' -d '{"title":"Hello World", "rating":"1", "author":"Mahmoud Hegazi" }' -H 'Content-Type: application/json'
                     - example of Success response:
                     
                       ```json
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
                               "id": 16,
                               "rating": 5,
                               "title": "Into To HTML"
                             }
                           ],
                           "code": 200,
                           "deleted": 15,
                           "success": true,
                           "total_books": 74
                         }
                        ```
                     - example of Falid response:

                       ```json
                         {
                           "code": 405,
                           "message": "method not allowed",
                           "success": false
                         }
                        ```
                        
                       ```json
                         {
                           "code": 422,
                           "message": "unprocessable",
                           'success': false
                         }
                        ```
                --- Search by title Adding a text search query to your request for the title of the book you want to search for is not case sensitive
                --- example of POST request to search By Title case insensitive
                curl -X POST 'http://localhost:5000/books' -d '{"search":"INTO TO HTML"}' -H 'Content-Type: application/json'
                
                It might show one of two results if the API finds that a book will return a JSON response
                       {            
                            "books": [
                         {
                             "author": "mahmoud",
                             "id": 16,
                             "rating": 5,
                             "title": "Into To HTML"
                          }
                         ],
                         "code": 200,
                         "success": true,
                         "total_books": 1
                       }
                       
               If the API doesn't find that the book will return a JSON response
               
                       }               
                         "books": [],
                         "code": 200,
                         "success": true,
                         "total_books": 0
                       }
                
                

                     - example of Falid response:

                       ```json
                         {
                           "code": 405,
                           "message": "method not allowed",
                           "success": false
                         }
                        ```
                        
                       ```json
                         {
                           "code": 422,
                           "message": "unprocessable",
                           'success': false
                         }
                        ```                
 
                         
                       ```json
                         {
                           "code": 404,
                           "message": "resource not found",
                           'success': false
                         }
                        ```    
                        
  # Tests:
  * in your-library API we use unit test to make sure everything is tested before the production.
  * There are 12 functions to test Our API
  * [test_normal_get, test_failed_one, test_path_request, test_404_path_request, test_400_path_request, test_delete_request , test_422_book_not_exist_request, 
  * test_post_request, test_wrong_post_create_error_request, test_422_post_request, test_search_book, test_search_not_found_book]
  *  in order to start the test cd [project_folder] and run python test.py
  #### test results will be like this:
  ![test result]('https://github.com/MahmoudHegazi/your_library_api/test_sc.JPG')
  
  # ALl Endpoints URLS
  
  1. http://localhost:5000/books  ||  http://localhost:5000/books?page=[page_number] (GET only)   (GET BOOKS)
  2. http://localhost:5000/books [POST]  When searching abook or adding new one, body must contains one of these ['search', 'title','author','rating']  (ADD / Search BOOKS) 
  3. http://localhost:5000/books/[book_id] [DELETE] Delete an existing book
  4. http://localhost:5000/books/[book_id] [PATCH] When editing a book, the requesting body must have a rating ['rating']
