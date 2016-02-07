#unit test

import os
import unittest
import datetime


if not "CONFIG_PATH" in os.environ:
	os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

import blog
from blog.views import *

class PaginateTests(unittest.TestCase):
	def test_paginate_size(self):
		self.client = app.test_client()
		
		print('in paginate test222')
		with self.client.test_request_context():
			print('in paginate test333')
		#count_returned_entries = print(entries())
		#	print('in paginate test')
		#	self.assertEqual(count_returned_entries, 10)
###^work out how to make this work...
###http://stackoverflow.com/questions/17375340/getting-working-outside-of-request-context-error-when-accessing-session-during

#	def next_page_returns_page_increment_1(self):
#        pass

if __name__ == "__main__":
	unittest.main()