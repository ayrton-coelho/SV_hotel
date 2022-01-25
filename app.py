from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from modules.form import HotelForm
from modules.comment_in import Comment_in
from modules.comment_out import Comment_out
from modules.pickup import hora_pickup
import uuid
from traceback import print_exc

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

class arribos_all(db.Model):
    __tablename__ = 'all_in'
    id = db.Column(db.String(36), primary_key=True)
    hora_creacion = db.Column(db.Time, nullable=False)
    vuelo = db.Column(db.String(128))
    hora_de_vuelo = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    nro_habitacion = db.Column(db.Integer, nullable=False)
    nro_personas = db.Column(db.Integer, nullable=False)
    origen = db.Column(db.String(128), nullable=False)
    destino = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(1024))

class partidas_all(db.Model):
    __tablename__ = 'all_out'
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
    comment = db.Column(db.String(1024))

class comentario_in(db.Model):
    __tablename__ = 'transport_comments_in'
    id = db.Column(db.String(36), db.ForeignKey('sv_hotel_in.id'), primary_key=True)
    comment = db.Column(db.String(1024))

    def __repr__(self):
        return f'id: {self.id}\ncomment: {self.comment}'

class comentario_out(db.Model):
    __tablename__ = 'transport_comments_out'
    id = db.Column(db.String(36), db.ForeignKey('sv_hotel_out.id'), primary_key=True)
    comment = db.Column(db.String(1024))

    def __repr__(self):
        return f'id: {self.id}\ncomment: {self.comment}'

##--------------------------------------------------##
# Renderizar formulario principal y conectar con db. #
##--------------------------------------------------##
@app.route("/", methods=['GET', 'POST'])
def form():
    form = HotelForm()
    if request.method == 'POST':
        arribo = arribos()
        partida = partidas()
        arribo_all = arribos_all()
        partida_all = partidas_all()
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
            arribo_all.id = id
            arribo_all.hora_creacion = created_at
            arribo_all.vuelo = vuelo
            arribo_all.hora_de_vuelo = hora
            arribo_all.fecha = fecha
            arribo_all.nro_habitacion = habitacion
            arribo_all.nro_personas = huespedes
            arribo_all.origen = puerto
            arribo_all.destino = hotel
            try:
                db.session.add(arribo)
                db.session.add(arribo_all)
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
            partida_all.id = id
            partida_all.hora_creacion = created_at
            partida_all.vuelo = vuelo
            partida_all.hora_de_vuelo = hora
            partida_all.fecha = fecha
            partida_all.hora_pickup = hora_pickup(hora, fecha)
            partida_all.nro_habitacion = habitacion
            partida_all.nro_personas = huespedes
            partida_all.nro_valijas = valijas
            partida_all.origen = hotel
            partida_all.destino = puerto
            try:
                db.session.add(partida)
                db.session.add(partida_all)
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
    in_viaje_all = arribos_all.query.get(id)
    if request.method == 'POST':
        try:
            setattr(in_viaje, 'vuelo', form.vuelo.data)
            setattr(in_viaje, 'hora_de_vuelo', form.hora.data)
            setattr(in_viaje, 'fecha', form.fecha.data)
            setattr(in_viaje, 'nro_habitacion', form.habitacion.data)
            setattr(in_viaje, 'nro_personas', form.huespedes.data)
            setattr(in_viaje, 'origen', form.puerto.data)
            setattr(in_viaje_all, 'vuelo', form.vuelo.data)
            setattr(in_viaje_all, 'hora_de_vuelo', form.hora.data)
            setattr(in_viaje_all, 'fecha', form.fecha.data)
            setattr(in_viaje_all, 'nro_habitacion', form.habitacion.data)
            setattr(in_viaje_all, 'nro_personas', form.huespedes.data)
            setattr(in_viaje_all, 'origen', form.puerto.data)
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
    out_viaje_all = partidas_all.query.get(id)
    if request.method == 'POST':
        hora = form.hora.data
        fecha = form.fecha.data
        pickup = hora_pickup(hora, fecha)
        try:
            setattr(out_viaje, 'vuelo', form.vuelo.data)
            setattr(out_viaje, 'hora_de_vuelo', hora)
            setattr(out_viaje, 'fecha', fecha)
            setattr(out_viaje, 'hora_pickup', pickup)
            setattr(out_viaje, 'nro_habitacion', form.habitacion.data)
            setattr(out_viaje, 'nro_personas', form.huespedes.data)
            setattr(out_viaje, 'nro_valijas', form.valijas.data)
            setattr(out_viaje, 'destino', form.puerto.data)
            setattr(out_viaje_all, 'vuelo', form.vuelo.data)
            setattr(out_viaje_all, 'hora_de_vuelo', hora)
            setattr(out_viaje_all, 'fecha', fecha)
            setattr(out_viaje_all, 'hora_pickup', pickup)
            setattr(out_viaje_all, 'nro_habitacion', form.habitacion.data)
            setattr(out_viaje_all, 'nro_personas', form.huespedes.data)
            setattr(out_viaje_all, 'nro_valijas', form.valijas.data)
            setattr(out_viaje_all, 'destino', form.puerto.data)
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
        comentario = comentario_in.query.get(id)
        db.session.delete(comentario)
        db.session.commit()
    except Exception:
        print_exc()
    try:
        viaje = arribos.query.get(id)
        db.session.delete(viaje)
        db.session.commit()
    except Exception:
        print_exc()

    return redirect('/hotel')

##---------------------------------------------##
# (BTN) Eliminar un viaje de la tabla partidas. #
##---------------------------------------------##
@app.route('/hotel/eliminar/out/<string:id>')
def hotel_delete_out(id):
    try:
        comentario = comentario_out.query.get(id)
        db.session.delete(comentario)
        db.session.commit()
    except Exception:
        print_exc()
    try:
        viaje = partidas.query.get(id)
        db.session.delete(viaje)
        db.session.commit()
    except Exception:
        print_exc()

    return redirect('/hotel')

##--------------------------------##
# Agregar comentario (Transporte). #
##--------------------------------##

# in #
@app.route('/transporte/comment/in/<string:id>', methods=['GET', 'POST'])
def transporte_comment_in(id):
    form = Comment_in()
    viaje = arribos.query.get(id)
    comment_in_all = arribos_all.query.get(id)
    vuelo = viaje.vuelo
    if request.method == 'POST':
        try:
            old_comment = comentario_in.query.get(id)
            if old_comment:
                db.session.delete(old_comment)
            new_comment = comentario_in()
            setattr(new_comment, 'id', id)
            setattr(new_comment, 'comment', form.comment.data)
            setattr(comment_in_all, 'comment', form.comment.data)
            db.session.add(new_comment)
            db.session.commit()
        except Exception:
            print_exc()
        return redirect('/transporte')
    else:
        return render_template('comment_in.html', form=form, id=id, vuelo=vuelo)

# out #
@app.route('/transporte/comment/out/<string:id>', methods=['GET', 'POST'])
def transporte_comment_out(id):
    form = Comment_out()
    viaje = partidas.query.get(id)
    comment_out_all = partidas_all.query.get(id)
    vuelo = viaje.vuelo
    if request.method == 'POST':
        try:
            old_comment = comentario_out.query.get(id)
            if old_comment:
                db.session.delete(old_comment)
            new_comment = comentario_out()
            setattr(new_comment, 'id', id)
            setattr(new_comment, 'comment', form.comment.data)
            setattr(comment_out_all, 'comment', form.comment.data)
            db.session.add(new_comment)
            db.session.commit()
        except Exception:
            print_exc()
        return redirect('/transporte')
    else:
        return render_template('comment_out.html', form=form, id=id, vuelo=vuelo)

##-----------------##
# Display comments. #
##-----------------##
@app.route('/comments')
def display_comments():
    comments_in = comentario_in.query.all()
    comments_out = comentario_out.query.all()
    viajes_in = arribos.query.all()
    viajes_out = partidas.query.all()
    comments_list_out = []
    comments_list_in = []
    for viaje in viajes_in:
        for comment in comments_in:
            if comment.id == viaje.id:
                comments_list_in.append((comment.comment, viaje.vuelo))
    for viaje in viajes_out:
        for comment in comments_out:
            if comment.id == viaje.id:
                comments_list_out.append((comment.comment, viaje.vuelo))

    return render_template('table_comments.html', comments_in=comments_list_in, comments_out=comments_list_out)

##------------##
# Display all. #
##------------##
@app.route('/all')
def display_all():
    all_in = arribos_all.query.order_by(arribos_all.hora_creacion.desc()).all()
    all_out = partidas_all.query.order_by(partidas_all.hora_creacion.desc()).all()
    return render_template('display_all.html', all_in=all_in, all_out=all_out)

def autorrellenar():
    vuelos = ['ABC 123', 'JBR 5443', 'HNX 890', 'KAP 314', 'UFW 427']
    hoteles = ['Radisson', 'Ibis', 'Columbia', 'Palladium', 'Holiday Inn']
    puertos = ['Aeropuerto Pde', 'Aeropuerto de Carrasco', 'Puerto', 'Aeropuerto de Carrasco', 'Aeropuerto de Carrasco']
    horas = ['23:30', '15:15', '02:00', '17:00', '11:00']
    fechas = ['2022-01-06', '2022-04-18', '2022-08-01', '2022-05-16', '2022-09-21']
    habitacion = [201, 303, 600, 116, 79]
    personas = [2, 1, 3, 2, 2]
    valijas = [2, 1, 2, 3, 2]
    for i in range(len(vuelos)):
        viaje = arribos()
        viaje.id = uuid.uuid4()
        viaje.hora_creacion = datetime.utcnow()
        viaje.vuelo = vuelos[i]
        viaje.destino = hoteles[i]
        viaje.origen = puertos[i]
        viaje.hora_de_vuelo = horas[i]
        viaje.fecha = fechas[i]
        viaje.nro_habitacion = habitacion[i]
        viaje.nro_personas = personas[i]
        try:
            db.session.add(viaje)
            db.session.commit()
        except:
            print_exc()
    for i in range(len(vuelos)):
        viaje = partidas()
        viaje.id = uuid.uuid4()
        viaje.hora_creacion = datetime.utcnow()
        viaje.vuelo = vuelos[i]
        viaje.destino = hoteles[i]
        viaje.origen = puertos[i]
        viaje.hora_de_vuelo = horas[i]
        viaje.hora_pickup = hora_pickup(horas[i], fechas[i])
        viaje.fecha = fechas[i]
        viaje.nro_habitacion = habitacion[i]
        viaje.nro_personas = personas[i]
        viaje.nro_valijas = valijas[i]
        try:
            db.session.add(viaje)
            db.session.commit()
        except:
            print_exc()



#----------------##
# Run Application #
#----------------##
if __name__ == "__main__":
    app.run(debug=True)