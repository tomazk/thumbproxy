import re
import logging
import hashlib

from flask import request

logger = logging.getLogger(__name__)

# django url regex 
re_URL = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE
	)

class RequestData(object):
	
	def __init__(self):
		self.url = request.values.get('u', None)
		self.action = request.values.get('a', None)
		self.width = request.values.get('w', None, type=int)
		self.height = request.values.get('h', None, type=int)
		self.signature = request.values.get('s', None) 
		
		try:
			self._validate_request_params()
			self.invalid = False
		except Exception, e:
			logger.error('params not validated: %s', repr(e))
			self.invalid = True
			
		logger.debug('request_data params: %s', repr(self.__dict__))
		
	def _validate_request_params(self):
		assert re_URL.match(self.url)
		assert self.action  in ('thumb', 'crop')
		assert isinstance(self.width, int)
		assert isinstance(self.height, int)
		
	def signature_is_valid(self, secret):
		return self.signature == generate_signature_from_query_string(request.query_string, secret)

re_SIG = re.compile('&s=[a-Z0.9]+$')

def generate_signature_from_query_string(query_string, secret):
		query_string = re_SIG.sub('', query_string)
		return hashlib.sha256(query_string + secret).hexdigest()
