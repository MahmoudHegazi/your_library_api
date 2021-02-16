from flask import Flask, jsonify, request, abort, make_response
import os
import json
import werkzeug
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from .models import setup_db, Book, db
from flask_mail import Mail, Message
import ast
import nexmo
import twilio
from twilio.rest import Client
import sys
import random

book_per_page = 8
auth_code = ''
for i in range(4):
    auth_code += str(random.randint(0,9))
# Mail API no need setup just JSON request to my API
def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    setup_db(app)
    CORS(app)
    # any request on /api from out soruce any domain will accepted but not allow put
    cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})
    # CORS Headers
    @app.after_request
    def after_request(response):
        #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        #response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    fakedb = []


    app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'))
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
         # load the test config if passed in
         app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # email setup
    app.config['TESTING'] = True
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_mail'
    app.config['MAIL_PASSWORD'] = 'your_pass'
    #app.config['MAIL_USE_SSL'] = True
    # Create an instance of the Mail class. I can do now every thing in python
    # updated version
    # email setup
    # run python app from any device
    # next google Auth 2

    mail = Mail(app)
    #client = nexmo.Client(key='Vonagekey', secret='Vonagesecret')

    # twilio setup


    @app.route('/')
    def home():
        #msg = Message('Hello', sender = 'mail_sender', recipients = ['reciver'])
        #msg.body = "Hi Can you help me setup flask email and login system"
        #mail.send(msg)
        return "api ready to use"
    # send message with vonage
    @app.route('/pythonking')
    def luck():
        # message cost .08 Euro u have 1.92 save it for secuirty login system
        #client.send_message({'from': 'Vonage APIs','to': 'send_to','text': 'Hello from Vonage SMS API Your are next Python King',})
        return "Real Python King Is Mahmoud Hegazi"
    # twilio Message app it give $12 free balnce
    @app.route('/pythonking1')
    def good():


        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        #account_sid = os.environ['sid']
        #auth_token = os.environ['auth_token']
        #account_sid = ""
        #auth_token  = ""
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="recipients",
            from_="tiwlo_sender_for_your_app",
            body="Hello My Friend This Advanced SMS: your Authorization CODE: %s" %auth_code)

        print(message.sid)
        html_messge = ''
        html_messge += '<form action="/authorization" method="post">'
        html_messge += '<label>Please Enter Your Awesome Authorization Code You got By Advanced SMS</label>'
        html_messge += '<input type="number" name="auth_code"><input type="submit">'
        html_messge += '</form>'
        return html_messge
        #return "Thans W3schools My Friends https://www.w3schools.com/js/js_ajax_xmlfile.asp"


    @app.route('/authorization', methods=['POST'])
    def auth1():
        if request.method == 'POST':
            auth_code = '%s' %request.form['auth_code']
            if auth_code == auth_code:
                return 'Hello You Can Access Our Awesome API'
        return 'You Are not allowed to use our API'

    def pagination_checker(page,selection):
        start = (page - 1) * book_per_page
        end = start + book_per_page
        formated_books = [book.format() for book in selection]
        pagie_list = formated_books[start:end]
        if len(pagie_list) == 0:
            return False
        else:
            return True

    def pagination_helper(request,selection):
        page = request.args.get('page',1,type=int)
        start = (page - 1) * book_per_page
        end = start + book_per_page
        formated_books = [book.format() for book in selection]
        pagie_list = formated_books[start:end]
        return pagie_list

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'code':404,
        'message':'resource not found',
        'success':False
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        'code':422,
        'message':'unprocessable',
        'success':False
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'code':400,
        'message':'bad request',
        'success':False
        }), 400

    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
        'code':405,
        'message':'method not allowed',
        'success':False
        }), 405
    @app.route('/books')
    def page():
        last_page = 1
        books = Book.query.order_by('id').all()
        books_per_request = pagination_helper(request,books)
        books_count = len(books)
        books_in_request_count = len(books_per_request)
        if len(books_per_request) == 0:
            abort(404)
        return jsonify({'code':'200','books':books_per_request,'total_books':books_count,'success':True},200)

    # update a book
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):
        try:
            body = request.get_json()
            body = json.loads(body)
        except:
            # if no data sent with request that is bad request
            abort(400)
        try:
            book = Book.query.filter_by(id=book_id).one_or_none()
            if book is None:
                #response = make_response(jsonify(message="Hello, We Did not Found that book try another one"), 404)
                abort(404)
            if 'rating' in body:
                #body.get('rating')
                book.rating = int(body['rating'])
            #return str(book.rating)
            book.update()
        except werkzeug.exceptions.NotFound:
            # if book not found in db this should returned
            abort(404)
        except:
            print(sys.exc_info())
            abort(400)
        return jsonify({'code':200,'id':book.id,'book_rating':book.rating,'success':True})



    # delete a book
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        if request.method != 'DELETE':
            abort(405)
        try:
            book = Book.query.filter_by(id=book_id).one_or_none()
            if book is None:
                abort(404)

            book.delete()
            selection = Book.query.order_by('id').all()
            current_books = pagination_helper(request,selection)
            len_books = len(selection)
            return jsonify({'code':200,
            'success':True,
            'books':current_books,
            'deleted':book_id,
            'total_books':len_books})
        except:
            abort(422)

    # create new Book
    @app.route('/books', methods=['POST'])
    def create_book():
        if request.method != 'POST':
            abort(405)
        try:
            body = request.get_json()
            json_body = json.loads(body)
        except:
            abort(422)
        # if title get it else make it None make sure title is nullable in DB title= author= rating=
        title = json_body.get('title', None)
        author = json_body.get('author', None)
        rating = json_body.get('rating', None)
        search = json_body.get('search', None)
        try:
            if search:
                selection = Book.query.filter(Book.title.ilike('%{}%'.format(search))).order_by('id').all()
                current_books = pagination_helper(request, selection)
                len_books = len(selection)
                return jsonify({'code':200,'success':True,
                'books':current_books,'total_books':len_books})
            else:
                newbook = Book(title=title, author=author,rating=rating)
                newbook.insert()

                selection = Book.query.order_by('id').all()
                current_books = pagination_helper(request, selection)
                len_books = len(selection)
                return jsonify({'code':200,'success':True,
                'books':current_books,'total_books':len_books,
                'created':newbook.id})
        except:
            abort(422)

        ## this good way to handle if all data required
        #if title == None and search == None:
        #    abort(400)
        #if author == None and search == None:
        #    abort(400)
        #if rating == None and search == None:
        #    abort(400)

        #if title == None and author == None and rating == None and search != None:
        #    try:
        #        selection = Book.query.filter(Book.title.ilike('%{}%'.format(search))).order_by('id').all()
        #        current_books = pagination_helper(request, selection)
        #        len_books = len(selection)
        #        return jsonify({'code':200,'success':True,
        #        'books':current_books,'total_books':len_books})
        #    except:
        #        # 0 books found
        #        selection = Book.query.filter_by(title=search).order_by('id').all()
        #        return jsonify({'code':200,'success':True,
        #        'books':current_books,'total_books':len_books})


        #try:
        #    newbook = Book(title=title, author=author,rating=rating)
        #    newbook.insert()

        #    selection = Book.query.order_by('id').all()
        #    current_books = pagination_helper(request, selection)
        #    len_books = len(selection)
        #    return jsonify({'code':200,'success':True,
        #    'books':current_books,'total_books':len_books,
        #    'created':newbook.id})
        #except:
        #    abort(422)
        #print('Data Received: "{data}"'.format(data=data))




    # handle form request
    @app.route('/form', methods=['POST'])
    def home_form():
            if request.method == 'POST':
                x = request.form['hello']
                return jsonify({'messsage':x})
    # handle file request
    @app.route('/file', methods=['POST'])
    def home_file():
            if request.method == 'POST':

                file = request.files['test']
                filename=secure_filename(file.filename)
                return jsonify({'messsage':filename})



    return app
