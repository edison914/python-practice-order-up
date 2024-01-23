from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AssignTableForm (FlaskForm):
    employee_id = SelectField('Employee id', validators=[DataRequired()])
    table_id = SelectField('Table id', validators=[DataRequired()])
    submit = SubmitField('Confirm')
