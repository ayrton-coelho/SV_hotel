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


##-------------------##
# vvv SQLAlchemy vvv  #
##-------------------##
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

##--------------------------------------------------##
# Renderizar formulario principal y conectar con db. #
##--------------------------------------------------##
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
        return render_template('form_hotel_main.html', form=form)

##-----------------------------------------##
# Renderizar tablas de viajes para hoteles. #
##-----------------------------------------##
@app.route('/hotel', methods=['GET'])
def hotel():
    in_viajes = arribos.query.order_by(arribos.hora_creacion.desc()).all()
    out_viajes = partidas.query.order_by(partidas.hora_creacion.desc()).all()
    return render_template('tables_hotel.html', in_viajes=in_viajes, out_viajes=out_viajes)

##------------------------------------------------##
# Renderizar tablas de viajes para transportistas. #
##------------------------------------------------##
@app.route('/transporte')
def transporte():
    in_viajes = arribos.query.order_by(arribos.hora_creacion.desc()).all()
    out_viajes = partidas.query.order_by(partidas.hora_creacion.desc()).all()
    return render_template('tables_transporte.html', in_viajes=in_viajes, out_viajes=out_viajes)


##------------------------##
# Editar viajes (Hoteles). #
##------------------------##

# in #
@app.route('/hotel/editar/in/<string:id>', methods=['GET', 'POST'])
def hotel_edit_in(id):
    form = HotelForm()
    in_viaje = arribos.query.get(id)
    if request.method == 'POST':
        new_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        vuelo = form.vuelo.data
        hora = form.hora.data
        fecha = form.fecha.data
        habitacion = form.habitacion.data
        huespedes = form.huespedes.data
        puerto = form.puerto.data
        hotel = 'random'
        try:
            db.session.delete(in_viaje)
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
        return redirect('/hotel')
    else:
        return render_template('form_edit_in.html', form=form, viaje=in_viaje)

# out #
@app.route('/hotel/editar/out/<string:id>', methods=['GET', 'POST'])
def hotel_edit_out(id):
    form = HotelForm()
    out_viaje = partidas.query.get(id)
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
            db.session.delete(out_viaje)
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
        return render_template('form_edit_out.html', form=form, viaje=out_viaje)

##--------------------------------------------##
# (BTN) Eliminar un viaje de la tabla arribos. #
##--------------------------------------------##
@app.route('/hotel/eliminar/in/<string:id>')
def hotel_delete_in(id):
    try:
        row = db.session.get(arribos, id)
        db.session.delete(row)
        db.session.commit()
    except Exception:
        pass
    return redirect('/hotel')

##---------------------------------------------##
# (BTN) Eliminar un viaje de la tabla partidas. #
##---------------------------------------------##
@app.route('/hotel/eliminar/out/<string:id>')
def hotel_delete_out(id):
    try:
        row = db.session.get(partidas, id)
        db.session.delete(row)
        db.session.commit()
    except Exception:
        pass
    return redirect('/hotel')

#-----#
# Run #
#-----#
if __name__ == "__main__":
    app.run(debug=True)