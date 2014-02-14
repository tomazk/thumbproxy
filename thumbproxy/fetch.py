import urllib2
import logging

logger = logging.getLogger(__name__)

def url(url, timeout=10):
	try:
		response = urllib2.urlopen(url, timeout=timeout)
		assert response.code == 200
		return response
	except Exception, e:
		logger.error('error when fetching url: %s error: %s', url, repr(e))
		raise