from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from modules.form import HotelForm
from modules.pickup import hora_pickup
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ayrton:password@localhost/sv_hoteles'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = SQLAlchemy(app)

class arribos(db.Model):
    __tablename__ = 'sv_hotel_in'
    id = db.Column(db.String(36), primary_key=True)
    hora_creacion = db.Column(db.Time, nullable=False)
    vuelo = db.Column(db.String(128))
    hora_de_vuelo = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    nro_habitacion = db.Column(db.Integer, nullable=False)
    nro_personas = db.Column(db.Integer, nullable=False)
    origen = db.Column(db.String(128), nullable=False)
    destino = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'id: {self.id}\nvuelo: {self.vuelo}\nhora: {self.hora_de_vuelo}\nfecha: {self.fecha}\nhuespedes: {self.nro_personas}\nhabitacion: {self.nro_habitacion}\norigen: {self.origen}\ndestino: {self.destino}\n'

class partidas(db.Model):
    __tablename__ = 'sv_hotel_out'
    id = db.Column(db.String(36), primary_key=True)
    hora_creacion = db.Column(db.Time, nullable=False)
    vuelo = db.Column(db.String(128))
    hora_de_vuelo = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_pickup = db.Column(db.String(30), nullable=False)
    nro_habitacion = db.Column(db.Integer, nullable=False)
    nro_personas = db.Column(db.Integer, nullable=False)
    nro_valijas = db.Column(db.Integer)
    origen = db.Column(db.String(128), nullable=False)
    destino = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'id: {self.id}\nvuelo: {self.vuelo}\nhora: {self.hora_de_vuelo}\nfecha: {self.fecha}\nhuespedes: {self.nro_personas}\nhabitacion: {self.nro_habitacion}\norigen: {self.origen}\ndestino: {self.destino}\n'


# Renderizar formulario + conectar y guardar en db
@app.route("/", methods=['GET', 'POST'])
def form():
    form = HotelForm()
    if request.method == 'POST':
        arribo = arribos()
        partida = partidas()
        id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        check = form.check.data
        vuelo = form.vuelo.data
        hora = form.hora.data
        fecha = form.fecha.data
        habitacion = form.habitacion.data
        huespedes = form.huespedes.data
        valijas = form.valijas.data
        puerto = form.puerto.data
        hotel = 'random'
        if check == 'Arribo':
            arribo.id = id
            arribo.hora_creacion = created_at
            arribo.vuelo = vuelo
            arribo.hora_de_vuelo = hora
            arribo.fecha = fecha
            arribo.nro_habitacion = habitacion
            arribo.nro_personas = huespedes
            arribo.origen = puerto
            arribo.destino = hotel
            try:
                db.session.add(arribo)
                print(arribo)
                db.session.commit()
            except Exception as e:
                print(e)
        elif check == 'Partida':
            partida.id = id
            partida.hora_creacion = created_at
            partida.vuelo = vuelo
            partida.hora_de_vuelo = hora
            partida.fecha = fecha
            partida.hora_pickup = hora_pickup(hora, fecha)
            partida.nro_habitacion = habitacion
            partida.nro_personas = huespedes
            partida.nro_valijas = valijas
            partida.origen = hotel
            partida.destino = puerto
            try:
                db.session.add(partida)
                db.session.commit()
                print(partida)
            except Exception as e:
                print(e)
        return redirect('/')
    else:
        return render_template('hotel_form.html', form=form)

# Renderizar tablas de viajes para hoteles
@app.route('/hotel', methods=['GET'])
def hotel():
    viajes_in = arribos.query.order_by(arribos.hora_creacion.desc()).all()
    viajes_out = partidas.query.order_by(partidas.hora_creacion.desc()).all()
    return render_template('hotel_table.html', viajes_in=viajes_in, viajes_out=viajes_out)

# Ruta para eliminar elementos de tabla
@app.route('/hotel/eliminar/<string:id>')
def hotel_delete(id):
    try:
        row = db.session.get(arribos, id)
        db.session.delete(row)
        db.session.commit()
    except Exception:
        pass
    try:
        row = db.session.get(partidas, id)
        db.session.delete(row)
        db.session.commit()
    except Exception:
        pass
    return redirect('/hotel')

# Ruta para editar viajes
@app.route('/hotel/editar/<string:id>', methods=['GET', 'POST'])
def hotel_edit(id):
    form = HotelForm()
    check = form.check.data
    print(check)
    viaje_in = arribos.query.get(id)
    viaje_out = partidas.query.get(id)
    if request.method == 'POST':
        new_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        vuelo = form.vuelo.data
        hora = form.hora.data
        fecha = form.fecha.data
        habitacion = form.habitacion.data
        huespedes = form.huespedes.data
        valijas = form.valijas.data
        puerto = form.puerto.data
        hotel = 'random'
        try:
            db.session.delete(viaje_in)
            arribo = arribos()
            arribo.id = new_id
            arribo.hora_creacion = created_at
            arribo.vuelo = vuelo
            arribo.hora_de_vuelo = hora
            arribo.fecha = fecha
            arribo.nro_habitacion = habitacion
            arribo.nro_personas = huespedes
            arribo.origen = puerto
            arribo.destino = hotel
            db.session.add(arribo)
            db.session.commit()
        except Exception as e:
            print(e)
        try:
            db.session.delete(viaje_out)
            partida = partidas()
            partida.id = new_id
            partida.hora_creacion = created_at
            partida.vuelo = vuelo
            partida.hora_de_vuelo = hora
            partida.fecha = fecha
            partida.hora_pickup = hora_pickup(hora, fecha)
            partida.nro_habitacion = habitacion
            partida.nro_personas = huespedes
            partida.nro_valijas = valijas
            partida.origen = hotel
            partida.destino = puerto
            db.session.add(partida)
            db.session.commit()
        except Exception as e:
            print(e)
        return redirect('/hotel')
    else:
        if check == 'Arribo':
            return render_template('hotel_edit_viaje.html', form=form, viaje=viaje_in)
        else:
            return render_template('hotel_edit_viaje.html', form=form, viaje=viaje_out)

# Renderizar tablas de viajes para transportistas
@app.route('/transporte')
def transporte():
    viajes_in = arribos.query.order_by(arribos.hora_creacion.desc()).all()
    viajes_out = partidas.query.order_by(partidas.hora_creacion.desc()).all()
    return render_template('transporte_table.html', viajes_in=viajes_in, viajes_out=viajes_out)

if __name__ == "__main__":
    app.run(debug=True)