from app import app
from app.forms import EditForm
from flask import render_template, redirect, request
from app.ml_model import model_prediction

@app.route('/')
@app.route('/index')
def index():
    if request.method == 'GET':
        return render_template('index.html', title='Home')
    else:
        return render_template('predict.html', title='Home')

@app.route('/predictions', methods=['GET','POST'])
def get_prediction():
    if request.method == 'GET':
        form = EditForm()
        return render_template('predict.html', form=form, diagnosis = "")
    if request.method == 'POST':
        args = request.form
        rm = args['rm']
        tm = args['tm']
        cm = args['cm']
        cnm = args['cnm']
        cpm = args['cpm']
        sm = args['sm']
        ts = args['ts']
        ps = args['ps']
        rw = args['rw']
        tw = args['tw']
        cw = args['cw']
        cpw = args['cpw']
        sw = args['sw']

        form = EditForm()
        form.rm.data = rm
        form.tm.data = tm
        form.cm.data = cm
        form.cnm.data = cnm
        form.cpm.data = cpm
        form.sm.data = sm
        form.ts.data = ts
        form.ps.data = ps
        form.rw.data = rw
        form.tw.data = tw
        form.cw.data = cw
        form.cpw.data = cpw
        form.sw.data = sw

        try:
            dg = str('The tumor is ' + model_prediction(rm, tm, cm, cnm, cpm, sm, ts, ps, rw, tw, cw, cpw, sw))
        except:
            dg = 'The prediction cannot be done! All values must be entered'

        return render_template('predict.html', form=form, diagnosis = dg)


