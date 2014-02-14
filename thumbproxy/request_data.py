import re
import logging

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
		logger.debug('url: %s', self.url)
		
		
		try:
			self._validate_request_params()
			self.invalid = False
		except Exception, e:
			logger.error('params not validated: %s', repr(e))
			self.invalid = True
		
	def _validate_request_params(self):
		assert re_URL.match(self.url)
		
		
		
		
		
		
		