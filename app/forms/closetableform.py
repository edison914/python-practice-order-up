from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class CloseTableForm (FlaskForm):
    order_id = SelectField('Order Id', validators=[DataRequired()])
    submit = SubmitField('Close Table')
