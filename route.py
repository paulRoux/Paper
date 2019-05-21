from application import app

from web.static import route_static
from web.views.index import route_index
from web.views.user import route_user

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_static, url_prefix="/static")
app.register_blueprint(route_user, url_prefix="/user")
