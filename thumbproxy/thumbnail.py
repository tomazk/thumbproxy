import logging
import cStringIO
import math
from PIL import Image

logger = logging.getLogger(__name__)


def _thumbnail(image, request_data):
	width = request_data.width
	height = request_data.height
	image.thumbnail((width, height), Image.ANTIALIAS)
		
	
def _crop(image, request_data):
	_,_, current_width, current_height = image.getbbox()
	
	width = min(current_width, request_data.width)
	height = min(current_height, request_data.height)
	
	width_offset = ( current_width - width ) / 2
	height_offset = ( current_height - height ) / 2
	
	box = (
		width_offset,
		height_offset,
		width_offset + width,
		height_offset + height
	)
	return image.crop(box)
	

def create(fetch_response, request_data):
	input = cStringIO.StringIO(fetch_response.read())
	image = Image.open(input, mode='r')
	if image.mode != 'RGB':
		image = image.convert('RGB')
	
	output = cStringIO.StringIO()
	
	if request_data.action == 'thumb':
		_thumbnail(image, request_data)
	elif request_data.action == 'crop':
		image = _crop(image, request_data)
	
	image.save(output, 'JPEG')
	
	thumbnail = output.getvalue()
	input.close()
	output.close()
	
	return thumbnail