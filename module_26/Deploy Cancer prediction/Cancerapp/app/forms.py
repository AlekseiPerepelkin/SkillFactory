from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    rm = FloatField('radius_mean')
    tm = FloatField('texture_mean')
    cm = FloatField('compactness_mean')
    cnm = FloatField('concavity_mean')
    cpm = FloatField('concave points_mean')
    sm = FloatField('symmetry_mean')
    ts = FloatField('texture_se')
    ps = FloatField('perimeter_se')
    rw = FloatField('radius_worst')
    tw = FloatField('texture_worst')
    cw = FloatField('concavity_worst')
    cpw = FloatField('concave points_worst')
    sw = FloatField('symmetry_worst')
    submit = SubmitField('Save')
    predict = SubmitField('Predict')
