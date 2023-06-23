import random
from http import HTTPStatus

from flask import render_template, flash, request, redirect, abort

from . import app, db
from .forms import CutForm
from .models import URLMap
from .constants import RANDOM_SHORT_LINK_LEN, ALLOWED_CHARACTERS


def get_unique_short_id() -> str:
    """Return random string with latin letters and numbers."""
    allowed_characters = list(ALLOWED_CHARACTERS)
    random_id = ''.join(random.choices(
        allowed_characters, k=RANDOM_SHORT_LINK_LEN))
    while URLMap.query.filter_by(short=random_id).first() is not None:
        random_id = ''.join(random.choices(
            allowed_characters, k=RANDOM_SHORT_LINK_LEN))
    return random_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Main page with from for fast create short link."""
    form = CutForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        flash('Ваша новая ссылка готова:', 'inform')
        flash(f'{request.base_url}{custom_id}', 'link')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def get_full_link(short_id):
    """Redirects the user when he visits a short link, if it exists."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
