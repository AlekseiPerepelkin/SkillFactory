from app import app, db
from app.forms import EditForm
from flask import render_template, redirect, request
from app.models import Flat
from sqlalchemy import func
from app.ml_model import model_prediction

@app.route('/')
@app.route('/index')
@app.route('/flats', methods=['GET','POST'])
def index():
    if request.method == 'GET':

        db_flats = Flat.query.all()
        flats = []
        for f in db_flats:
            flats.append({
                'id': f.id,
                'title': f.title,
                'city': f.city,
                'rooms': f.rooms,
                'area': f.area,
                'floor': f.floor,
                'cost': f.cost
            })
        return render_template('index.html', title='Home', flats=flats)
    else:
        flat_id = request.form['flatId']
        res = Flat.query.filter(Flat.id==flat_id).first()
        flat = {'id': flat_id,
                'title': res.title,
                'city': res.city,
                'rooms': res.rooms,
                'area': res.area,
                'floor': res.floor,
                'cost': res.cost}
        return render_template('flat.html', title='Home', flat=flat)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        form = EditForm()
        if 'id' in request.args:
            form.id = request.args['id']
            flat = Flat.query.filter(Flat.id == request.args['id']).first()
            form.title.data = flat.title
            form.city.data = flat.city
            form.rooms.data = flat.rooms
            form.area.data = flat.area
            form.floor.data = flat.floor
            form.cost.data = flat.cost
        else:
            max_id = db.session.query(func.max(Flat.id)).scalar()
            if max_id is None:
                flat_id = 0
            else:
                flat_id = max_id + 1
            form.id = flat_id
        return render_template('edit.html', title='Home', form=form)
    if request.method == 'POST':
        args = dict(request.form)
        title = args['title']
        city = args['city']
        rooms = args['rooms']
        area = args['area']
        floor = args['floor']
        cost = args['cost']
        flat_id = int(args['flatId'])

        ids = [i[0] for i in Flat.query.with_entities(Flat.id).all()]
        if flat_id in ids:
            flat = Flat.query.filter(Flat.id == flat_id).first()
            flat.title = title
            flat.city = city
            flat.rooms = rooms
            flat.area = area
            flat.floor = floor
            flat.cost = cost
            db.session.commit()
        else:
            new_flat = Flat(id=flat_id,
                                title=title,
                                city=city,
                                rooms=rooms,
                                area=area,
                                floor=floor,
                                cost=cost)
            db.session.add(new_flat)
            db.session.commit()
        return redirect('/index')
    else:
        return redirect('/index')


# html не поддерживает методы put и delete и так как мы делаем веб-версию,
# то эти методы использоватьне будем.
# Если бы к вашему приложению обращались только через API,
# можно было бы использовать PUT и DELETE
@app.route('/delete', methods=['GET'])
def delete_flat():
    form_id = request.args['id']
    Flat.query.filter(Flat.id == form_id).delete()
    db.session.commit()
    return redirect('/index')


@app.route('/predictions', methods=['GET','POST'])
def get_prediction():
    if request.method == 'GET':
        form = EditForm()
        return render_template('predict.html', form=form, cost = "")
    if request.method == 'POST':
        args = request.form
        city = args['city']
        rooms = args['rooms']
        area = args['area']
        floor = args['floor']

        form = EditForm()
        form.city.data = city
        form.rooms.data = rooms
        form.area.data = area
        form.floor.data = floor

        return render_template('predict.html', form=form, cost = str(model_prediction(city, rooms, area, floor)) + ' руб')


