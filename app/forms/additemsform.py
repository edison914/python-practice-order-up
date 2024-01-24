from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class AddItemForm (FlaskForm):
    order_id = SelectField('Employee id', validators=[DataRequired()])
    menu_item_ids = SelectMultipleField('Menu items')
    submit = SubmitField('Confirm Adding Items')
