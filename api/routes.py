from flask import request
from flask_restx import Api, Resource, fields
from .models import db, Paciente, PAnciano, PJoven, PNinno, Consulta, Hospital

rest_api = Api(version='1.0', title='fonasa inexoos')

""" 
    Pacientes 
"""

paciente_model = rest_api.model('Paciente', {
    'id': fields.Integer(required=True, description='ID del paciente'),
    'nombre': fields.String(required=True, description='Nombre del paciente'),
    'edad': fields.Integer(required=True, description='Edad del paciente'),
    'noHistoriaClinica': fields.Integer(required=True, description='Número de Historia Clínica'),
    'tieneDieta': fields.Boolean(required=False, description='Si el paciente tiene dieta'),
    'fumador': fields.Boolean(required=False, description='Si el paciente fuma'),
    'relacionPesoEstatura': fields.Integer(required=False, description='Relación peso estatura'),
    'hospital_id': fields.Integer(required=True, description='ID del hospital')
})

pacientes_model = rest_api.model('Pacientes', {
    'pacientes': fields.List(fields.Nested(paciente_model))
})


@rest_api.route('/pacientes')
class PacientesResource(Resource):

    @rest_api.marshal_with(pacientes_model)
    def get(self):
        pacientes = Paciente.query.all()
        return {"pacientes": pacientes}

    @rest_api.expect(paciente_model)
    @rest_api.marshal_with(paciente_model)
    def post(self):
        data = request.get_json()
        if data['edad'] <= 15:
            nuevo_paciente = PNinno(nombre=data['nombre'], edad=data['edad'], noHistoriaClinica=data['noHistoriaClinica'], relacionPesoEstatura=data['relacionPesoEstatura'], hospital_id=data['hospital_id'])
        elif 16 <= data['edad'] <= 40:
            nuevo_paciente = PJoven(nombre=data['nombre'], edad=data['edad'], noHistoriaClinica=data['noHistoriaClinica'], fumador=data['fumador'], hospital_id=data['hospital_id'])
        else:
            nuevo_paciente = PAnciano(nombre=data['nombre'], edad=data['edad'], noHistoriaClinica=data['noHistoriaClinica'], tieneDieta=data['tieneDieta'], hospital_id=data['hospital_id'])
        
        try:
            db.session.add(nuevo_paciente)
            db.session.commit()
            return {"paciente": nuevo_paciente}, 201
        except Exception as e:
            return 400

"""
    Consultas
"""

consulta_model = rest_api.model('Consulta',  {
        'id': fields.Integer(required=True, description='ID de la consulta'),
        'cantPacientes': fields.Integer(required=True, description='Cantidad de pacientes'),
        'nombreEspecialista': fields.String(required=True, description='Nombre del especialista'),
        'tipoConsulta': fields.String(required=True, description='Tipo de consulta'),
        'estado': fields.String(required=True, description='Estado de la consulta'),
        'hospital_id': fields.Integer(required=True, description='ID del hospital')
    }
)

consultas_model = rest_api.model('Consultas', {
    'consultas': fields.List(fields.Nested(consulta_model)),
    'error': fields.String
})

@rest_api.route('/consultas')
class ConsultasResource(Resource):
    @rest_api.marshal_with(consultas_model)
    def get(self):
        consultas = Consulta.query.all()
        return {"consultas": consultas}

    @rest_api.expect(consulta_model)
    @rest_api.marshal_with(consulta_model)
    def post(self):
        data = request.get_json()
        nueva_consulta = Consulta(cantPacientes=data['cantPacientes'], nombreEspecialista=data['nombreEspecialista'], tipoConsulta=data['tipoConsulta'], estado=data['estado'], hospital_id=data['hospital_id'])
        try:
            db.session.add(nueva_consulta)
            db.session.commit()
            return {"consulta": nueva_consulta}, 201
        except Exception as e:
            return {"consulta": data, "error": str(e)}, 400

#Liberar consulta
@rest_api.route('/liberar_consulta/<int:id>')
class LiberarConsultaResource(Resource):
    def post(self, id):
        consulta = Consulta.query.get(id)
        consulta.estado = 'INACTIVO'
        consulta.paciente_id = None
        db.session.commit()
        return {"msg": "Consulta liberada"}, 200
    
#Liberar todas las consultas
@rest_api.route('/liberar_consultas')
class LiberarConsultasResource(Resource):
    def post(self):
        consultas = Consulta.query.all()
        for consulta in consultas:
            consulta.estado = 'INACTIVO'
            consulta.paciente_id = None
        db.session.commit()
        return {"msg": "Consultas liberadas"}, 200

#Consultas activas
consultas_activas_model = rest_api.model('ConsultasActivas', {
    'consultas': fields.List(fields.Nested(consulta_model))
})

@rest_api.route('/consultas_activas')
class ConsultasActivasResource(Resource):
    @rest_api.marshal_with(consultas_activas_model)
    def get(self):
        consultas = VerConsultasActivas()
        return {"consultas": consultas}

"""
    Hospitales
"""

hospital_model = rest_api.model('Hospital', {
    'id': fields.Integer(required=True, description='ID del hospital'),
    'nombre': fields.String(required=True, description='Nombre del hospital')
})

hospitales_model = rest_api.model('Hospitales', {
    'hospitales': fields.List(fields.Nested(hospital_model))
})

@rest_api.route('/hospitales')
class HospitalesResource(Resource):

    @rest_api.marshal_with(hospitales_model)
    def get(self):
        hospitales = Hospital.query.all()
        return {"hospitales": hospitales}

    @rest_api.expect(hospital_model)
    @rest_api.marshal_with(hospital_model)
    def post(self):
        data = request.get_json()
        nuevo_hospital = Hospital(nombre=data['nombre'])
        db.session.add(nuevo_hospital)
        db.session.commit()
        return 201
    
""" Cola de espera """

"recibe un id de un paciente y un id de hospital y lo agrega a la cola de espera del hospital correspondiente"
sala_espera_model = rest_api.model('SalaEspera', {
    'paciente_id': fields.Integer(required=True, description='ID del paciente'),
    'hospital_id': fields.Integer(required=True, description='ID del hospital'),
    'nombre': fields.String(required=True, description='Nombre del paciente'),
    'edad': fields.Integer(required=True, description='Edad del paciente'),
    'noHistoriaClinica': fields.Integer(required=True, description='Número de Historia Clínica'),
    'tipo': fields.String(required=True, description='Tipo de paciente'),
    'tieneDieta': fields.Boolean(required=False, description='Si el paciente tiene dieta'),
    'fumador': fields.Boolean(required=False, description='Si el paciente fuma'),
    'relacionPesoEstatura': fields.Integer(required=False, description='Relación peso estatura'),
    'prioridad': fields.Integer(required=True, description='Prioridad del paciente'),
    'riesgo': fields.Float(required=True, description='Riesgo del paciente')
})

cola_espera_model = rest_api.model('ColaEspera', {
    'cola': fields.List(fields.Nested(sala_espera_model), description='Lista de espera')
})

# Cola de espera global
cola_espera = []

def calcular_prioridad(paciente):
    if paciente.tipo == 'ninno':
        # Lógica para niños
        if 1 <= paciente.edad <= 5:
            return paciente.relacionPesoEstatura + 3
        elif 6 <= paciente.edad <= 12:
            return paciente.relacionPesoEstatura + 2
        elif 13 <= paciente.edad <= 15:
            return paciente.relacionPesoEstatura + 1
    elif paciente.tipo == 'joven':
        # Lógica para jóvenes
        return paciente.anosFumador / 4 + 2 if paciente.fumador else 2
    elif paciente.tipo == 'anciano':
        # Lógica para ancianos
        if paciente.tieneDieta and 60 <= paciente.edad <= 100:
            return paciente.edad / 20 + 4
        else:
            return paciente.edad / 30 + 3

def calcular_riesgo(paciente, prioridad):
    riesgo_base = (paciente.edad * prioridad) / 100
    return riesgo_base + 5.3 if paciente.tipo == 'anciano' else riesgo_base

@rest_api.route('/cola_espera')
class ColaEsperaResource(Resource):
    @rest_api.marshal_with(cola_espera_model)
    def get(self):
        return {"cola": cola_espera}

    @rest_api.expect(sala_espera_model)
    def post(self):
        data = request.get_json()
        """ Verificamos si ya existe el paciente en la cola """
        for paciente in cola_espera:
            if paciente['paciente_id'] == data['paciente_id']:
                return {"msg": "El paciente ya está en la cola"}, 400
        """ Agregamos más datos del paciente haciendo una consulta sobre él"""
        paciente = Paciente.query.get(data['paciente_id'])
        data['nombre'] = paciente.nombre
        data['edad'] = paciente.edad
        data['noHistoriaClinica'] = paciente.noHistoriaClinica
        data['tipo'] = paciente.tipo
        data['tieneDieta'] = paciente.tieneDieta if hasattr(paciente, 'tieneDieta') else None
        data['fumador'] = paciente.fumador if hasattr(paciente, 'fumador') else None
        data['relacionPesoEstatura'] = paciente.relacionPesoEstatura if hasattr(paciente, 'relacionPesoEstatura') else None

        prioridad = calcular_prioridad(paciente)
        riesgo = calcular_riesgo(paciente, prioridad)

        # Agrega la prioridad y el riesgo al diccionario data
        data['prioridad'] = prioridad
        data['riesgo'] = riesgo

        # Agrega el paciente a la cola con prioridad y riesgo
        cola_espera.append(data)
        return {"msg": "Paciente agregado a la cola"}, 201

@rest_api.route('/atender_paciente')
class AtenderPacienteResource(Resource):
    @rest_api.expect(sala_espera_model)
    def post(self):
        data = request.get_json()
        """ Verificamos si ya existe el paciente en la cola """
        for paciente in cola_espera:
            if paciente['paciente_id'] == data['paciente_id']:
                cola_espera.remove(paciente)
                """ asignamos la consulta al paciente  """
                consulta = BuscarConsultaLibre()
                if consulta is None:
                    return {"msg": "No hay consultas disponibles"}, 400
                consulta.estado = 'ACTIVO'
                consulta.paciente_id = data['paciente_id']
                db.session.commit()
                return {"msg": "Paciente atendido"}, 200
        return {"msg": "El paciente no está en la cola"}, 400
    
def BuscarConsultaLibre():
    consultas = Consulta.query.filter_by(estado='INACTIVO').all()
    if len(consultas) > 0:
        return consultas[0]
    return None

def VerConsultasActivas():
    consultas = Consulta.query.filter_by(estado='ACTIVO').all()
    if len(consultas) > 0:
        return consultas
    return None

def ListarPacientesMayorRiesgo():
    return sorted(cola_espera, key=lambda paciente: paciente['riesgo'], reverse=True)

def ListarPacientesFumadoresUrgentes():
    return list(filter(lambda paciente: paciente['fumador'] == True and paciente['prioridad'] >= 4, cola_espera))

def ConsultaMasPacientesAntedidos():
    consultas = Consulta.query.all()
    consultas.sort(key=lambda consulta: len(consulta.pacientes), reverse=True)
    return consultas[0]

def PacienteMasAnciano():
    pacientes = Paciente.query.all()
    pacientes.sort(key=lambda paciente: paciente.edad, reverse=True)
    return pacientes[0]

def OptimizarAtencion():
    # Ordenamos la cola de espera
    cola_espera.sort(key=lambda paciente: paciente['riesgo'], reverse=True)
    cola_espera.sort(key=lambda paciente: paciente['prioridad'], reverse=True)
    cola_espera.sort(key=lambda paciente: paciente['paciente_id'], reverse=False)

    # Liberamos todas las consultas
    consultas = Consulta.query.all()
    for consulta in consultas:
        consulta.estado = 'INACTIVO'
        consulta.paciente_id = None
    db.session.commit()

    # Asignamos las consultas a los pacientes
    for paciente in cola_espera:
        consulta = BuscarConsultaLibre()
        if consulta is None:
            return {"msg": "No hay consultas disponibles"}, 400
        consulta.estado = 'ACTIVO'
        consulta.paciente_id = paciente['paciente_id']
        db.session.commit()

    return {"msg": "Optimización realizada"}, 200