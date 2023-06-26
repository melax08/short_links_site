from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .views import get_unique_short_id
from .constants import MAX_SHORT_LINK_LEN
from .utils import validate_short_link


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_full_url(short_id):
    """Allows to get the original link when passing a short one."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    """Allows to create a short link by passing the url."""
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if custom_id:
        if (len(custom_id) > MAX_SHORT_LINK_LEN or
                not validate_short_link(custom_id)):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    url = URLMap()
    url.from_dict(data)
    if not custom_id:
        url.short = get_unique_short_id()
    db.session.add(url)
    db.session.commit()
    return jsonify({
        "url": url.original,
        "short_link": request.host_url + url.short
    }), HTTPStatus.CREATED
