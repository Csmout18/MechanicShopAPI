from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import app

ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day, 50 per hour"]) #default limit for all routes, can be overridden
cache = Cache()