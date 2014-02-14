import os
import logging
import traceback

from flask import Flask
from flask import make_response

from thumbproxy.request_data import RequestData
from thumbproxy import fetch
from thumbproxy import thumbnail

app = Flask(__name__)

# api endpoints

@app.route('/api/', methods=('GET',))
def main_api_method():
	app.logger.debug('call to api')
	
	request_data = RequestData()
	if request_data.invalid:
		return 'parameters are invalid', 500
	
	try:
		fetch_response = fetch.url(request_data.url, app.config['FETCH_TIMEOUT'])
	except:
		return 'not found', 404
	
	try:
		thumbnail_image = thumbnail.create(fetch_response, request_data)
	except Exception, e:
		traceback.print_exc()
		app.logger.error('error when creating thumbnail: %s', repr(e))
		return 'error', 500
	
	response = make_response(thumbnail_image)
	response.headers['Content-Type'] =  'image/jpeg'

	return response


# Configuration

app.config.from_object('settings')

if 'FLASK_PROD_SETTINGS' in os.environ:
	app.config.from_envvar('FLASK_PROD_SETTINGS')
	
thumbproxy_logger = logging.getLogger('thumbproxy')
formatter = logging.Formatter('%(asctime)s %(module)s %(levelname)s: %(message)s [in %(filename)s:%(funcName)s:%(lineno)d]')

filehandler = logging.FileHandler(os.path.join(app.config['LOG_DIR'], 'api.aplication.log'))
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)

if not app.config['DEBUG']:
	app.logger.setLevel(logging.INFO)
	app.logger.addHandler(filehandler)
	
	thumbproxy_logger.setLevel(logging.DEBUG)
	thumbproxy_logger.addHandler(filehandler)
else:
	app.logger.setLevel(logging.DEBUG)
	
	thumbproxy_logger.setLevel(logging.DEBUG)
	streamhandler = logging.StreamHandler()
	streamhandler.setLevel(logging.DEBUG)
	streamhandler.setFormatter(formatter)
	thumbproxy_logger.addHandler(streamhandler)


if __name__ == '__main__':
	app.run(debug=True)