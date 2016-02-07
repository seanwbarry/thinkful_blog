#integration tests for views.py

import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

#configure app to use testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        """Test setup"""                         
        self.client = app.test_client()
        #makes an interface that allows requests to be made to the server with given parameters
        #Setup tables in the database
        Base.metadata.create_all(engine)
        
        #create an example user
        self.user = User(name="Alice", email="alice@example.com",
                        password = generate_password_hash("test"))
        session.add(self.user)
        session.commit()
        
    def tearDown(self):
        """Test teardown"""
        session.close()
        #Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
    
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            #self.client.session_transaction() gets you access to a variable representing the HTTP session (recall: self.client = app.test_client() <- this is an interface that allows requests to be made 'to 'the' server with given parameters
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True
            #obviously http_session is a dict
            
    def test_add_entry(self):
        self.simulate_login()
        
        response = self.client.post("/entry/add", data = {
            "title": "Test Entry",
            "content": "Test content"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)
    
    #my integration test    
    def test_delete_entry(self):
        self.simulate_login()
        self.test_add_entry()
        entries_beginning = session.query(Entry).all()
        entry_id = str(1)
        #this is a weak point of this test - it relies on there being an entry with id 1...
        response = self.client.post("/entry/"+str(entry_id)+"/delete",
                data = entry_id)
        entries_end = session.query(Entry).all()
        self.assertEqual(len(entries_end), (len(entries_beginning)-1))



if __name__ == "__main__":
    unittest.main()
        
        