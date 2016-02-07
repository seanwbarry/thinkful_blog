#acceptance tests for views.py

import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    
    def setUp(self):
        # Test setup 
        self.browser = Browser("phantomjs")
        
        #setup the tables in the database
        Base.metadata.create_all(engine)
        
        #create an example user
        
        self.user = User(name="Alice", email="alice@example.com",
                        password=generate_password_hash("test"))
        session.add(self.user)
        
        self.entry = Entry(title="test entry", content="test content")
        session.add(self.entry)
        
        session.commit()
        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)

    def tearDown(self):
        """ Test teardown """
        #Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()
        
    def test_login_correct(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        #print(self.browser.url)
        #print('asdf')
        time.sleep(1)
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
    
    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        time.sleep(1)
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")
    
    #my acceptance test
    def test_edit_entry_requires_login(self):
        self.browser.visit("http://127.0.0.1:5000/entry/1/edit")
        time.sleep(1)
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login?next=%2Fentry%2F1%2Fedit")
    
if __name__ == "__main__":
    unittest.main()
