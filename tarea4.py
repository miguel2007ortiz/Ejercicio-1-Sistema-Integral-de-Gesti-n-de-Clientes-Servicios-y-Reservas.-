"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
============================================================

Un sistema robusto de gestión de reservas que demuestra:
- Programación orientada a objetos (POO) avanzada
- Abstracción e Herencia
- Polimorfismo
- Encapsulación con properties
- Manejo exhaustivo de excepciones
- Logging detallado
- Validaciones robustas
- Patrones de diseño (singledispatchmethod)
- Persistencia de datos en archivos JSON
"""

import logging
import json
import os
from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import List, Optional, Tuple
from enum import Enum

# =====================================================================
# CONFIGURACIÓN DE LOGGING
# =====================================================================

logging.basicConfig(
    filename='sistema_reservas.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s'
)

# =====================================================================
# ENUMERACIONES PARA ESTADOS
# =====================================================================

class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = 'Pendiente'
    CONFIRMADA = 'Confirmada'
    CANCELADA = 'Cancelada'
    PROCESADA = 'Procesada'


# =====================================================================
# BLOQUE DE EXCEPCIONES PERSONALIZADAS
# Jerarquía clara de excepciones del sistema
# =====================================================================

class SistemaError(Exception):
    """Excepción base para todos los errores del sistema."""
    pass


class ValidacionError(SistemaError):
    """Error cuando los datos no pasan las validaciones."""
    pass


class ReservaError(SistemaError):
    """Error relacionado con operaciones de reserva."""
    pass


class ClienteError(SistemaError):
    """Error relacionado con operaciones de cliente."""
    pass


class ServicioError(SistemaError):
    """Error relacionado con operaciones de servicio."""
    pass

# clase abtracta ABC "Abstrac Base Class"
class Entidad(ABC):
    @abstractmethod  # obliga a clases hijas a usar este método
    def mostrar_info(self):
        pass
# clase Cliente con validaciones robustas y encapsulación de 
# datos personales

class Cliente(Entidad):
    def __init__(self, nombre, cedula, correo, telefono):

        if not nombre.strip():  # limpia espacios al inicio y final
            # si queda vacío lanza error
            raise ValidacionError('Nombre vacío')

        if '@' not in correo:
            raise ValidacionError('Correo inválido')

        self.__nombre = nombre  # encapsulación (privado)
        self.__cedula = cedula
        self.__correo = correo
        self.__telefono = telefono

    @property
    def nombre(self):  # permite usar como variable a nombre
        return self.__nombre

    def mostrar_info(self):
        return f'Cliente: {self.__nombre} - CC {self.__cedula} - correo {self.__correo} - telefono {self.__telefono}'


class Servicio(ABC):
    def __init__(self, nombre, tarifa):

        if tarifa <= 0:
            raise ValidacionError('Tarifa inválida')

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod  # obliga a implementar cálculo de costo
    def calcular_costo(self, horas, impuesto=0, descuento=0):# el valor de impuesto y descuetno determinado por programa
        pass

    @abstractmethod  # obligación de descripción
    def descripcion(self):
        pass

#Una clase abstracta Servicio y al menos tres servicios 
#especializados que hereden de ella, implementando polimorfismo y 
#métodos sobrescritos para calcular costos, describir servicios y 
#validar parámetro

# primer clase abstracta de servicio 
class ReservaSala(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        total = self.tarifa * horas
        total += total * impuesto
        total -= descuento
        return max(total, 0)  # evita negativos

    def descripcion(self):
        return 'Reserva de sala empresarial'

# segunda clase abstracta de servicio
class AlquilerEquipo(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        total = (self.tarifa * horas) + 20_000## Costo fijo adicional  independiente de las horas
        total += total * impuesto
        total -= descuento
        return max(total, 0) # evita negativos y de ser asi retorna cero

    def descripcion(self):
        return 'Alquiler de equipos tecnológicos'

# tercera clase abtracta de servico
class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        total = (self.tarifa * horas) * 1.15# aumento 15% el valro de este servicio por ser especializado
        total += total * impuesto
        total -= descuento
        return max(total, 0)

    def descripcion(self):
        return 'Asesoría especializada'

#Una clase Reserva que integre cliente, servicio, duración y estado, 
#e implemente confirmación, cancelación y procesamiento con 
# manejo de excepciones.
class Reserva:
    ESTADO_PENDIENTE = 'Pendiente'
    ESTADO_CONFIRMADA = 'Confirmada'
    ESTADO_CANCELADA = 'Cancelada'

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaError('Horas inválidas dede ser mayor a cero')
# Atributos principales de la reserva
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = self.ESTADO_PENDIENTE

    def confirmar(self):
        if self.estado == self.ESTADO_CANCELADA:
            raise ReservaError('No se puede confirmar una reserva cancelada')

        if self.estado == self.ESTADO_CONFIRMADA:
            raise ReservaError('La reserva ya está confirmada')

        self.estado = self.ESTADO_CONFIRMADA
 # Evita cancelar dos veces
    def cancelar(self):
        if self.estado == self.ESTADO_CANCELADA:
            raise ReservaError('La reserva ya está cancelada')

        self.estado = self.ESTADO_CANCELADA

    def procesar(self):
        try:
            if self.estado == self.ESTADO_CANCELADA:
                raise ReservaError('No se puede procesar una reserva cancelada')

            if self.estado == self.ESTADO_CONFIRMADA:
                raise ReservaError('La reserva ya fue procesada')
# Cálculo del costo usando polimorfismo del servicio
            costo = self.servicio.calcular_costo(self.horas,impuesto=0.19)

            self.confirmar()
 # Registro del evento en logs
            logging.info(
                f'Reserva confirmada para {self.cliente.nombre}'  )

            return costo

        except Exception as e:
            logging.error(f'Error procesando reserva: {e}')
            raise ReservaError('No fue posible procesar la reserva') from e
 # Representación en texto de la reserva
    def __str__(self):
        return f'{self.cliente.nombre} | {self.servicio.nombre} | {self.horas}h | {self.estado}'







#================================================================================================================================
# BLOQUE DE FUNCIONES =================
# se crean las listas vacias  y se agregan funciones

clientes = []
servicios = []
reservas = []
# agrega a lista servicios
servicios.append(ReservaSala('Sala Premium', 50000))# Crea una instancia de ReservaSala y la agrega a la lista de servicios y se le da valor 
servicios.append(AlquilerEquipo('Portátil Gamer', 40000))# crea instancia de class alquielerequipo y se de da valor 
servicios.append(AsesoriaEspecializada('Consultoría TI', 90000))# se crea instancia class asesoriaespacializada y se da valor 
# =====================================================================
# SISTEMA DE PERSISTENCIA
# =====================================================================

def guardar_datos():
    # Guarda la lista de clientes en un archivo json para no perder datos al cerrar
    try:
        lista_final = []
        for c in clientes:
            lista_final.append({
                "nombre": c.nombre,
                "cedula": c._Cliente__cedula,
                "correo": c._Cliente__correo,
                "telefono": c._Cliente__telefono
            })
        
        with open('data_clientes.json', 'w', encoding='utf-8') as archivo:
            json.dump(lista_final, archivo, indent=4, ensure_ascii=False)
            
        logging.info("Archivo data_clientes.json actualizado correctamente.")
    except Exception as error:
        logging.error(f"Error al guardar: {error}")
def generar_reporte_txt(reserva):
    # Genera un historial de reservas en un archivo de texto plano (Logs de usuario)
    try:
        with open('historial_reservas.txt', 'a', encoding='utf-8') as f:
            f.write(f"RESERVA REALIZADA: {reserva.cliente.nombre} | "
                    f"Servicio: {reserva.servicio.nombre} | "
                    f"Horas: {reserva.horas} | "
                    f"Costo calculado con éxito\n")
            f.write("-" * 60 + "\n")
        print("-> Reporte generado en historial_reservas.txt")
    except Exception as e:
        logging.error(f"Error al escribir reporte TXT: {e}")

def cargar_datos():
    # Carga la info desde el json apenas arranca el sistema
    if os.path.exists('data_clientes.json'):
        try:
            with open('data_clientes.json', 'r', encoding='utf-8') as archivo:
                datos_leidos = json.load(archivo)
                for d in datos_leidos:
                    clientes.append(Cliente(d['nombre'], d['cedula'], d['correo'], d['telefono']))
            print("-> Info: Se recuperaron los clientes del archivo local.")
        except Exception as error:
            logging.error(f"Error al cargar: {error}")

# =====================================================================

def registrar_cliente():# Registra un nuevo cliente solicitando datos por consola,
# valida la información mediante la clase Cliente y lo agrega a la lista.
# Si ocurre un error, lo registra en el log y lo muestra en pantalla.
    try:# estructura de control de errores try
        n = input('Nombre: ')
        c = input('Cédula: ')
        co = input('Correo: ')
        t = input('Teléfono: ')

        cli = Cliente(n, c, co, t) # Crea un objeto Cliente con los datos ingresados
        clientes.append(cli)  # Agrega el cliente a la lista de clientes
        guardar_datos() 

        print('Cliente registrado')

    except Exception as e: #cualquier error, lo registra en logs y lo muestra en pantalla
        logging.error(str(e))
        print('Error:', e)

# Muestra la lista de clientes registrados; si no hay, informa que está vacía
def listar_clientes():
    if not clientes:
        print(" No hay clientes registrados")
        return
# Recorre la lista de clientes asignando un número (desde 1) y muestra su informació
    for i, c in enumerate(clientes, 1):
        print(i, c.mostrar_info())

# Recorre y muestra los servicios con su número, nombre y descripción
def listar_servicios():
    for i, s in enumerate(servicios, 1):
        print(i, s.nombre, '-', s.descripcion())


def crear_reserva():
    try:
        if not clientes:# verifica si no hay clientes 
            raise ReservaError('No hay clientes registrados')

        listar_clientes()
        ic = int(input('Seleccione cliente: ')) - 1 #Muestra los clientes, pide al usuario que elija uno, 
                                                    #resta 1 porque las listas empiezan en 0

        listar_servicios()
        isv = int(input('Seleccione servicio: ')) - 1 #Muestra los servicios, el usuario selecciona uno
                                                    ## Se resta 1 porque las listas en Python empiezan en índice 0
        horas = int(input('Horas: '))#Pide cuántas horas va a durar la reserva
        r = Reserva(clientes[ic], servicios[isv], horas)# Crea una reserva con el cliente y servicio seleccionados, y la duración en horas


        print("\nResumen de reserva:")
        print(r)

        confirmar = input("¿Desea confirmar la reserva? (s/n), ingrese si o no: ").lower()
#Pregunta si quiere confirmar la reserva Convierte la respuesta a minúsculas
        if confirmar == 'si':#Si el usuario digita “si”, continúa con la confirmación
            total = r.procesar()#calcula costo valida estadoconfirma la reserva
            reservas.append(r) #Guarda la reserva en la lista reservas
            generar_reporte_txt(r) #Genera el TXT físico
            print('Reserva creada. Total:', total)# Muestra el valor total de la reserva
        else:
            print("Reserva no confirmada")#Si el usuario no confirma, no se guarda la reserva

    except Exception as e:#Si ocurre cualquier error, entra aquí
        logging.error(str(e))#Guarda el error en el archivo de logs
        print('Error:', e)#Muestra el error en pantalla
        
        
        
def ver_reservas():#Define la función que sirve para mostrar todas las reservas registradas
    if not reservas: #Verifica si la lista reservas está vacía.
        print(" No hay reservas registradas")
        return
    for i, r in enumerate(reservas, 1):#Recorre la lista reservas.
                                        #i = número de la reserva (empieza en 1)
                                        #r = cada objeto reserva
        print(i, r)


def cancelar_reserva():#Define la función que sirve para cancelar una reserva existente.
    if not reservas:#Verifica si la lista reservas está vacía.
        print(" No hay reservas para cancelar")
        return

    ver_reservas()#Llama a la función que muestra todas las reservas disponibles.
    i = int(input("Seleccione reserva a cancelar: ")) - 1#Pide al usuario que elija una reserva.
                                                       #Convierte la entrada a número (int)
                                                        #Resta 1 porque las listas empiezan en 0
    reservas[i].cancelar()#Accede a la reserva seleccionada y ejecuta su método cancelar().
                            #Cambia el estado a “Cancelada”
    print("Reserva cancelada")
    
    
    # simulacion para uso
def pruebas_automaticas():# función que ejecuta pruebas del sistema automáticamente (casos de prueba).
    casos = [ # lista llamada casos con diferentes datos de clientes.
        ('Ana', '1', 'ana@mail.com', '300'),# SI SE  QUIERE AUMENTAR LA LISTA SE HARIA AQUI DIRECTAMENTE 
        ('', '2', 'mal', '300'),
        ('Luis', '3', 'luis@mail.com', '301'),
    ]

    for x in casos:#Recorre cada caso uno por uno.
        try:#ejecutar la creación del cliente sin que el programa se caiga si hay error.
            clientes.append(Cliente(*x))#Cliente(*x) → crea un cliente usando los datos del caso
                                        #append → lo agrega a la lista clientes. El *x significa: “desempaqueta la tupla”
        except Exception as e:#Si hay error:lo guarda en el log no detiene el programa
            logging.error(e)

    try:
        reservas.append(Reserva(clientes[0], servicios[0], 2))#Crea una reserva válida:primer cliente,primer servicio,2 horas
                                                                #y la guarda en la lista reservas, datos predertimanados por programa
        reservas[-1].procesar() # Toma la última reserva creada y la procesa
    except Exception as e:#Si algo falla en la reserva, lo registra en el log.
        logging.error(e)

    try:
        Reserva(clientes[0], servicios[1], -1)#Intenta crear una reserva inválida, debe fallar al se -1 
    except Exception as e:
        logging.error(e)#Captura el error y lo guarda en el log.
    guardar_datos()

    print('Pruebas ejecutadas')
    


def menu():# función principal del programa, que muestra el menú de opciones.
    cargar_datos() # Carga automática al abrir
    while True:#Crea un ciclo infinito.
                #El menú se repite una y otra vez hasta que el usuario elija salir.
        try:#Intenta ejecutar todo el menú sin que el programa se caiga si hay errores.
            # imprime todo el menu que va ver el usario en pantalla
            print('\n--- SOFTWARE FJ ---')
            print('1. Registrar cliente')
            print('2. Ver clientes')
            print('3. Ver servicios')
            print('4. Crear reserva')
            print('5. Ver reservas')
            print('6. Cancelar reserva')
            print('7. Ejecutar pruebas automáticas')
            print('8. Salir')
            

            op = input('Opción: ')#Pide al usuario que seleccione una opción del menú.
# compara el dato ingresado por el usuario y segun corresponda ejecuta la funcion corresponde
            if op == '1':
                registrar_cliente()
            elif op == '2':
                listar_clientes()
            elif op == '3':
                listar_servicios()
            elif op == '4':
                crear_reserva()
            elif op == '5':
                ver_reservas()
            elif op == '6':
                 cancelar_reserva()
            elif op == '7':
                pruebas_automaticas()
            elif op == '8':

                break#Sale del ciclo y termina el programa con la opcion 8
            else:
                print('Opción inválida')#Si el usuario escribe algo diferente de 1 a 8, muestra error.

        except Exception as e:#Si ocurre cualquier error:lo guarda en el log, lo muestra en pantalla, evita que el programa se cierre
            logging.error(str(e))
            print('Error general:', e)

        finally:#e ejecuta siempre (haya error o no),En este caso no hace nada (pass),Solo está como estructura de control
            pass

#===============================================================================================================
#Solo arranca el programa aquí si este archivo es el principal, no si lo estoy usando como módulo en otro archivo
if __name__ == '__main__':
    menu()
