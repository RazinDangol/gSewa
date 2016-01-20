from gsewa import app
from shifty.wsgi_utils import envify

app=application=envify(app)