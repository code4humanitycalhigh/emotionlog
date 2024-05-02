import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
#verbose = 0 for flask server


from flask import Flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
import views