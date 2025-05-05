from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,
from wtforms.validators import DataRequired


class PlanForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    cities = StringField('Города', render_kw={"list": "suggestions_for_wifi", "autocomplete": "off"})
    submit = SubmitField('Submit')