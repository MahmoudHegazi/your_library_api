import unittest
import json
from flaskr import create_app
from flaskr.models import setup_db, Book

class AppNameTestCase(unittest.TestCase):
    """This class represents the ___ test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.client = self.app.test_client
        self.database_name = "bookshelf"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.newbook = {'title':'test_book','author':'some_one','rating':5}
        #pass

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_normal_get(self):
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)
        self.assertTrue(data[0]['total_books'])
        self.assertTrue(len(data[0]['books']))


    def test_failed_one(self):
        res = self.client().get('/books?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_path_request(self):
        the_data = json.dumps(dict(rating=4))
        res = self.client().patch('/books/18',json=the_data,content_type='application/json')
        data = json.loads(res.data)
        book = Book.query.filter_by(id=18).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 4)
        #print(book.format()['rating'])

    def test_404_path_request(self):
        the_data = json.dumps(dict(rating=5))
        res = self.client().patch('/books/10001',json=the_data,content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_400_path_request(self):
        res = self.client().patch('/books/18')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    #def test_delete_request(self):
    #    res = self.client().delete('/books/12')
    #    data = json.loads(res.data)
    #    print(data)
    #    confirm_delete = Book.query.filter_by(id=12).one_or_none()
    #    self.assertEqual(res.status_code, 200)
    #    self.assertEqual(data['success'], True)
    #    self.assertEqual(data['deleted'], 12)
    #    self.assertTrue(data['total_books'])
    #    self.assertTrue(len(data['books']))
    #    self.assertEqual(confirm_delete, None)

    def test_422_book_not_exist_request(self):
        res = self.client().delete('/books/10001')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    def test_post_request(self):
        the_data = json.dumps(dict(title='Full Stack', author='Mahmoud', rating=5))
        res = self.client().post('/books',json=the_data,content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_wrong_post_create_error_request(self):
        the_data = json.dumps(dict(title='Full Stack', author='Mahmoud', rating=5))
        res = self.client().post('/books/1',json=the_data,content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # bad request request becuase it can not convert this to json
    #def test_422_post_request(self):
    #    the_data = json.dumps(dict(title='Full Stack', author='Mahmoud', rating=5))
    #    res = self.client().post('/books',json='',content_type='application/json')
    #    data = json.loads(res.data)
    #    self.assertEqual(res.status_code, 400)
    #    self.assertEqual(data['success'], False)
    #    self.assertEqual(data['message'], 'unprocessable')


    def test_search_book(self):
        the_data = json.dumps(dict(search='full stack'))
        res = self.client().post('/books',json=the_data,content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(data['books'])

    def test_search_not_found_book(self):
        the_data = json.dumps(dict(search='worngbook'))
        res = self.client().post('/books',json=the_data,content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # big important not if result = 0 even if True it will equal to false
        # another note dont use assertTrue if u know the result is false
        self.assertEqual(data['total_books'],0)
        # small note books will return empty list do not test it direct test the len or just add []
        self.assertEqual(data['books'],[])
        self.assertEqual(len(data['books']),0)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    unittest.main()
