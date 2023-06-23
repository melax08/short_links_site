from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional,
                                ValidationError, URL)

from .models import URLMap
from .constants import MAX_SHORT_LINK_LEN
from .utils import validate_short_link


class CutForm(FlaskForm):
    """From class for add link by user and get short link.
    User can specify his own custom short link (custom_id field)."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(-1, MAX_SHORT_LINK_LEN), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        """Validator for custom_id field.
        Checks for invalid characters and whether a short link is available."""
        if not validate_short_link(field.data):
            raise ValidationError(
                'Короткая ссылка содержит некорректные символы')
        if URLMap.query.filter_by(short=field.data).first() is not None:
            raise ValidationError(f'Имя {field.data} уже занято!')
