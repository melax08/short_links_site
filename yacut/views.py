from http import HTTPStatus

from flask import render_template, flash, request, redirect, abort

from . import app, db
from .forms import CutForm
from .models import URLMap
from .utils import get_unique_short_id


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
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)
