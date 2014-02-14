#!/usr/local/bin/python

import secret
import hashlib
import urlparse
import sys

'''
urlparse.urlparse('http://localhost:5000/api/?u=http://venturebeat.files.wordpress.com/2013/07/arkham-origins_joker-gang.jpg&a=thumb&w=300&h=300')
Out[3]: ParseResult(scheme='http', netloc='localhost:5000', path='/api/', params='', query='u=http://venturebeat.files.wordpress.com/2013/07/arkham-origins_joker-gang.jpg&a=thumb&w=300&h=300', fragment='')
'''

url = sys.argv[1]
parsed = urlparse.urlparse(url)
signature = hashlib.sha256(parsed.query + secret) 
print parsed.scheme + '://' + parsed.netloc + parsed.path + '?' + parsed.query + '&s=' + signature

