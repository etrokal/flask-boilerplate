
from flask import Blueprint, render_template


bp = Blueprint(name="home", import_name=__file__, url_prefix="/")


@bp.route("/", methods=['GET'])
def index():
    return render_template('home/index.jinja')
