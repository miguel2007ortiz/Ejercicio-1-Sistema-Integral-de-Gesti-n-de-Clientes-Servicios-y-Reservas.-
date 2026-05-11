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
Fecha: 2026
"""

import logging
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


# =====================================================================
# CLASE ABSTRACTA BASE
# =====================================================================

class Entidad(ABC):
    """Clase abstracta base para todas las entidades del sistema.

    Obliga a las clases hijas a implementar el método mostrar_info().
    Esta es la base del polimorfismo en el sistema.
    """

    @abstractmethod
    def mostrar_info(self) -> str:
        """Retorna información formateada de la entidad.

        Returns:
            str: Información completa de la entidad
        """
        pass

    def __repr__(self) -> str:
        """Representación técnica de la entidad para debugging."""
        return f"{self.__class__.__name__}()"


# =====================================================================
# CLASE CLIENTE
# Con validaciones exhaustivas y encapsulación completa
# =====================================================================

class Cliente(Entidad):
    """Representa un cliente en el sistema.

    Attributes:
        __nombre (str): Nombre completo (3+ caracteres)
        __cedula (str): Número de identificación (5+ dígitos)
        __correo (str): Email válido
        __telefono (str): Teléfono (7+ dígitos)
        __activo (bool): Estado del cliente
    """

    def __init__(self, nombre: str, cedula: str, correo: str, telefono: str):
        """Inicializa un cliente con validaciones exhaustivas.

        Args:
            nombre: Nombre completo del cliente
            cedula: Número de identificación
            correo: Correo electrónico
            telefono: Número de teléfono

        Raises:
            ValidacionError: Si algún dato es inválido
        """
        self.__nombre = self._validar_nombre(nombre)
        self.__cedula = self._validar_cedula(cedula)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)
        self.__activo = True

        logging.info(f'Cliente creado: {self.__nombre} (CC: {self.__cedula})')

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        """Valida y normaliza el nombre."""
        if not nombre or not nombre.strip():
            raise ValidacionError('El nombre no puede estar vacío')
        if len(nombre.strip()) < 3:
            raise ValidacionError('El nombre debe tener al menos 3 caracteres')
        return nombre.strip()

    @staticmethod
    def _validar_cedula(cedula: str) -> str:
        """Valida y normaliza la cédula."""
        if not cedula or not cedula.strip():
            raise ValidacionError('La cédula no puede estar vacía')
        if not cedula.strip().isdigit():
            raise ValidacionError('La cédula debe contener solo números')
        if len(cedula.strip()) < 5:
            raise ValidacionError('La cédula debe tener al menos 5 dígitos')
        return cedula.strip()

    @staticmethod
    def _validar_correo(correo: str) -> str:
        """Valida y normaliza el correo."""
        if not correo or '@' not in correo:
            raise ValidacionError('Correo inválido: debe contener @')
        partes = correo.split('@')
        if len(partes) != 2 or not partes[1]:
            raise ValidacionError('Correo inválido: formato incorrecto')
        if '.' not in partes[1]:
            raise ValidacionError('Correo inválido: dominio incompleto')
        return correo.strip()

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        """Valida y normaliza el teléfono."""
        if not telefono or not telefono.strip():
            raise ValidacionError('El teléfono no puede estar vacío')
        if not telefono.strip().isdigit():
            raise ValidacionError('El teléfono debe contener solo números')
        if len(telefono.strip()) < 7:
            raise ValidacionError('El teléfono debe tener al menos 7 dígitos')
        return telefono.strip()

    # Properties para acceso controlado
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Modifica el nombre con validación."""
        self.__nombre = self._validar_nombre(valor)

    @property
    def cedula(self) -> str:
        """Obtiene la cédula del cliente."""
        return self.__cedula

    @property
    def correo(self) -> str:
        """Obtiene el correo del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        """Modifica el correo con validación."""
        self.__correo = self._validar_correo(valor)

    @property
    def telefono(self) -> str:
        """Obtiene el teléfono del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Modifica el teléfono con validación."""
        self.__telefono = self._validar_telefono(valor)

    @property
    def activo(self) -> bool:
        """Verifica si el cliente está activo."""
        return self.__activo

    def desactivar(self):
        """Desactiva el cliente."""
        self.__activo = False
        logging.info(f'Cliente desactivado: {self.__nombre}')

    def mostrar_info(self) -> str:
        """Implementación del método abstracto."""
        estado = "Activo" if self.__activo else "Inactivo"
        return f'Cliente: {self.__nombre} | CC: {self.__cedula} | Correo: {self.__correo} | Teléfono: {self.__telefono} | {estado}'

    def __str__(self) -> str:
        return self.mostrar_info()

    def __eq__(self, otro) -> bool:
        """Compara clientes por cédula."""
        if not isinstance(otro, Cliente):
            return False
        return self.__cedula == otro.cedula


# =====================================================================
# CLASE ABSTRACTA SERVICIO
# Base para los servicios especializados con polimorfismo
# =====================================================================

class Servicio(ABC):
    """Clase abstracta que define la interfaz de servicios.

    Attributes:
        nombre (str): Nombre del servicio
        tarifa (float): Tarifa base por hora
    """

    def __init__(self, nombre: str, tarifa: float):
        """Inicializa un servicio con validaciones.

        Args:
            nombre: Nombre descriptivo del servicio
            tarifa: Valor por hora (debe ser > 0)

        Raises:
            ServicioError: Si los parámetros son inválidos
        """
        if not nombre or not nombre.strip():
            raise ServicioError('El nombre del servicio no puede estar vacío')
        if not isinstance(tarifa, (int, float)):
            raise ServicioError(f'Tarifa debe ser numérica, recibió {type(tarifa)}')
        if tarifa <= 0:
            raise ServicioError(f'Tarifa inválida: {tarifa}. Debe ser mayor a 0')

        self.nombre = nombre.strip()
        self.tarifa = float(tarifa)

    @abstractmethod
    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Calcula el costo del servicio.

        Args:
            horas: Cantidad de horas
            **kwargs: Parámetros adicionales (impuesto, descuento, etc.)

        Returns:
            float: Costo total
        """
        pass

    @abstractmethod
    def descripcion(self) -> str:
        """Retorna la descripción del servicio.

        Returns:
            str: Descripción completa
        """
        pass

    def __str__(self) -> str:
        return f'{self.nombre} - ${self.tarifa:,.2f}/hora'


# =====================================================================
# SERVICIOS ESPECIALIZADOS (Polimorfismo)
# =====================================================================

class ReservaSala(Servicio):
    """Servicio de reserva de sala empresarial.

    Tarifa base por hora sin cargos adicionales.
    """

    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Calcula costo: tarifa × horas + impuesto - descuento."""
        impuesto = kwargs.get('impuesto', 0)
        descuento = kwargs.get('descuento', 0)

        total = self.tarifa * horas
        total += total * impuesto
        total -= descuento

        return max(total, 0)

    def descripcion(self) -> str:
        """Descripción del servicio."""
        return 'Reserva de sala empresarial con equipamiento básico'


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos.

    Incluye costo fijo de $20,000 por mantenimiento.
    """

    COSTO_FIJO = 20000

    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Calcula costo: (tarifa × horas) + costo_fijo + impuesto - descuento."""
        impuesto = kwargs.get('impuesto', 0)
        descuento = kwargs.get('descuento', 0)

        total = (self.tarifa * horas) + self.COSTO_FIJO
        total += total * impuesto
        total -= descuento

        return max(total, 0)

    def descripcion(self) -> str:
        """Descripción del servicio."""
        return f'Alquiler de equipos tecnológicos con soporte (costo fijo: ${self.COSTO_FIJO:,})'


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada.

    Aplica recargo del 15% por especialización.
    """

    RECARGO_ESPECIALIZACION = 1.15

    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Calcula costo: (tarifa × horas × 1.15) + impuesto - descuento."""
        impuesto = kwargs.get('impuesto', 0)
        descuento = kwargs.get('descuento', 0)

        total = (self.tarifa * horas) * self.RECARGO_ESPECIALIZACION
        total += total * impuesto
        total -= descuento

        return max(total, 0)

    def descripcion(self) -> str:
        """Descripción del servicio."""
        return 'Asesoría especializada con expertos certificados (recargo 15%)'


# =====================================================================
# CLASE RESERVA
# Integra cliente, servicio, duración y estado con validaciones
# =====================================================================

class Reserva:
    """Representa una reserva en el sistema.

    Attributes:
        cliente (Cliente): Cliente que realiza la reserva
        servicio (Servicio): Servicio reservado
        horas (int): Duración en horas
        estado (EstadoReserva): Estado actual
        costo_total (Optional[float]): Costo calculado al procesar
    """

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: float):
        """Inicializa una reserva.

        Args:
            cliente: Objeto Cliente válido
            servicio: Objeto Servicio válido
            horas: Duración en horas (> 0)

        Raises:
            ReservaError: Si los parámetros son inválidos
        """
        if not isinstance(cliente, Cliente):
            raise ReservaError('El cliente debe ser una instancia de Cliente')
        if not isinstance(servicio, Servicio):
            raise ReservaError('El servicio debe ser una instancia de Servicio')
        if not isinstance(horas, (int, float)):
            raise ReservaError(f'Horas debe ser numérica, recibió {type(horas)}')
        if horas <= 0:
            raise ReservaError(f'Horas inválidas: {horas}. Debe ser mayor a cero')

        self.cliente = cliente
        self.servicio = servicio
        self.horas = int(horas)
        self.estado = EstadoReserva.PENDIENTE
        self.costo_total: Optional[float] = None

        logging.info(f'Reserva creada: {cliente.nombre} → {servicio.nombre} ({horas}h)')

    def confirmar(self):
        """Confirma la reserva.

        Raises:
            ReservaError: Si la reserva está cancelada o ya confirmada
        """
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservaError('No se puede confirmar una reserva cancelada')
        if self.estado == EstadoReserva.CONFIRMADA:
            raise ReservaError('La reserva ya está confirmada')

        self.estado = EstadoReserva.CONFIRMADA
        logging.info(f'Reserva confirmada: {self.cliente.nombre}')

    def cancelar(self):
        """Cancela la reserva.

        Raises:
            ReservaError: Si la reserva ya está cancelada
        """
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservaError('La reserva ya está cancelada')

        self.estado = EstadoReserva.CANCELADA
        logging.warning(f'Reserva cancelada: {self.cliente.nombre}')

    def procesar(self, impuesto: float = 0.19, descuento: float = 0) -> float:
        """Procesa la reserva: calcula costo y confirma.

        Args:
            impuesto: Porcentaje de impuesto (default 19%)
            descuento: Valor fijo de descuento (default 0)

        Returns:
            float: Costo total procesado

        Raises:
            ReservaError: Si no puede procesarse
        """
        try:
            if self.estado == EstadoReserva.CANCELADA:
                raise ReservaError('No se puede procesar una reserva cancelada')
            if self.estado == EstadoReserva.CONFIRMADA:
                raise ReservaError('La reserva ya fue procesada')

            # Cálculo de costo usando polimorfismo
            self.costo_total = self.servicio.calcular_costo(
                self.horas,
                impuesto=impuesto,
                descuento=descuento
            )

            self.confirmar()
            self.estado = EstadoReserva.PROCESADA

            logging.info(
                f'Reserva procesada: {self.cliente.nombre} | '
                f'{self.servicio.nombre} | {self.horas}h | '
                f'Total: ${self.costo_total:,.2f}'
            )

            return self.costo_total

        except ReservaError as e:
            logging.error(f'Error de reserva: {e}')
            raise
        except Exception as e:
            logging.error(f'Error inesperado: {e}')
            raise ReservaError('Error inesperado al procesar la reserva') from e

    def __str__(self) -> str:
        costo_str = f' | Costo: ${self.costo_total:,.2f}' if self.costo_total else ''
        return f'{self.cliente.nombre} | {self.servicio.nombre} | {self.horas}h | {self.estado.value}{costo_str}'

    def __repr__(self) -> str:
        return f'Reserva({self.cliente.nombre}, {self.servicio.nombre}, {self.horas}h, {self.estado.value})'


# =====================================================================
# CALCULADORA DE COSTOS CON SOBRECARGA
# Demuestra @singledispatchmethod para polimorfismo de métodos
# =====================================================================

class CalculadoraCostos:
    """Calculadora que demuestra sobrecarga de métodos.

    Usa @singledispatchmethod para diferentes implementaciones
    según el tipo del argumento (Patrón Visitor de Python).
    """

    @singledispatchmethod
    def calcular(self, arg):
        """Método base para cálculo de costos.

        Args:
            arg: Argumento de tipo no especificado

        Raises:
            NotImplementedError: Si el tipo no está soportado
        """
        raise NotImplementedError(f'Tipo no soportado: {type(arg).__name__}')

    @calcular.register
    def _(self, arg: int) -> str:
        """Sobrecarga para enteros: horas sin modificaciones."""
        return f'Cálculo con entero: {arg} horas'

    @calcular.register
    def _(self, arg: float) -> str:
        """Sobrecarga para flotantes: redondea a 2 decimales."""
        return f'Cálculo con flotante: {round(arg, 2)} horas'

    @calcular.register
    def _(self, arg: list) -> str:
        """Sobrecarga para listas: suma de múltiples servicios."""
        if not arg:
            return 'Lista vacía'
        total = sum(tarifa * horas for tarifa, horas in arg)
        return f'Cálculo múltiple: {len(arg)} servicios, total ${total:,.2f}'

    @calcular.register
    def _(self, arg: str) -> str:
        """Sobrecarga para strings: códigos promocionales."""
        descuentos = {'PROMO10': 0.10, 'PROMO20': 0.20, 'VIP': 0.30}
        descuento = descuentos.get(arg.upper(), 0)
        return f'Código "{arg}": descuento {descuento*100:.0f}%'


# =====================================================================
# BLOQUE DE FUNCIONES DEL SISTEMA
# =====================================================================

# Listas globales para almacenamiento en memoria
clientes: List[Cliente] = []
servicios: List[Servicio] = []
reservas: List[Reserva] = []

# Servicios predefinidos
servicios.append(ReservaSala('Sala Premium', 50000))
servicios.append(AlquilerEquipo('Portátil Gamer', 40000))
servicios.append(AsesoriaEspecializada('Consultoría TI', 90000))


def registrar_cliente():
    """Registra un nuevo cliente con validación interactiva."""
    print("\n" + "="*50)
    print("REGISTRO DE CLIENTE")
    print("="*50)

    try:
        nombre = input('Nombre completo: ').strip()
        cedula = input('Cédula (números): ').strip()
        correo = input('Correo electrónico: ').strip()
        telefono = input('Teléfono (números): ').strip()

        cliente = Cliente(nombre, cedula, correo, telefono)

        clientes.append(cliente)
        print(f'\nCliente registrado exitosamente: {cliente.nombre}')

    except ValidacionError as e:
        logging.error(f'Validación fallida: {e}')
        print(f'\nError de validación: {e}')
    except Exception as e:
        logging.error(f'Error inesperado: {e}')
        print(f'\nError: {e}')


def listar_clientes():
    """Muestra todos los clientes registrados."""
    print("\n" + "="*50)
    print("LISTA DE CLIENTES")
    print("="*50)

    if not clientes:
        print("No hay clientes registrados")
        return

    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente}")


def listar_servicios():
    """Muestra todos los servicios disponibles."""
    print("\n--- SERVICIOS DISPONIBLES ---")
    for i, servicio in enumerate(servicios, 1):
        print(f"{i}. {servicio.nombre}")
        print(f"   → {servicio.descripcion()}")
        print(f"   → Tarifa: ${servicio.tarifa:,.2f}/hora\n")


def crear_reserva():
    """Permite crear una nueva reserva interactivamente."""
    print("\n" + "="*50)
    print("CREAR NUEVA RESERVA")
    print("="*50)

    try:
        if not clientes:
            raise ReservaError('No hay clientes registrados. Registre uno primero.')

        listar_clientes()
        indice_cliente = int(input('\nSeleccione número de cliente: ')) - 1

        if indice_cliente < 0 or indice_cliente >= len(clientes):
            raise ReservaError('Selección inválida de cliente')

        listar_servicios()
        indice_servicio = int(input('Seleccione número de servicio: ')) - 1

        if indice_servicio < 0 or indice_servicio >= len(servicios):
            raise ReservaError('Selección inválida de servicio')

        horas = float(input('Cantidad de horas: '))

        reserva = Reserva(clientes[indice_cliente], servicios[indice_servicio], horas)

        print(f"\n{'-'*50}")
        print("RESUMEN DE RESERVA:")
        print(f"{'-'*50}")
        print(reserva)

        confirmacion = input("\n¿Confirmar reserva? (s/n): ").lower()

        if confirmacion in ['s', 'si', 'sí']:
            costo = reserva.procesar()
            reservas.append(reserva)
            print(f'\n✓ Reserva procesada exitosamente')
            print(f'  Total a pagar: ${costo:,.2f}')
        else:
            print('\n✗ Reserva cancelada por el usuario')

    except ValueError:
        logging.error('Entrada numérica inválida')
        print('\n✗ Error: Ingrese números válidos')
    except ReservaError as e:
        logging.error(f'Error de reserva: {e}')
        print(f'\n✗ Error: {e}')
    except Exception as e:
        logging.error(f'Error inesperado: {e}')
        print(f'\n✗ Error inesperado: {e}')


def ver_reservas():
    """Muestra todas las reservas registradas."""
    print("\n" + "="*50)
    print("LISTA DE RESERVAS")
    print("="*50)

    if not reservas:
        print("No hay reservas registradas")
        return

    for i, reserva in enumerate(reservas, 1):
        print(f"{i}. {reserva}")


def cancelar_reserva():
    """Permite cancelar una reserva existente."""
    print("\n" + "="*50)
    print("CANCELAR RESERVA")
    print("="*50)

    if not reservas:
        print("No hay reservas para cancelar")
        return

    ver_reservas()

    try:
        indice = int(input('\nSeleccione número de reserva a cancelar: ')) - 1

        if indice < 0 or indice >= len(reservas):
            raise ValueError('Selección inválida')

        reserva = reservas[indice]

        confirmacion = input(f"\n¿Cancelar reserva de {reserva.cliente.nombre}? (s/n): ").lower()

        if confirmacion in ['s', 'si', 'sí']:
            reserva.cancelar()
            print('Reserva cancelada exitosamente')
        else:
            print('Cancelación abortada')

    except ValueError as e:
        logging.error(f'Error de entrada: {e}')
        print(f'✗ Error: Ingrese un número válido')
    except ReservaError as e:
        logging.error(f'Error de reserva: {e}')
        print(f'✗ Error: {e}')


def pruebas_automaticas():
    """Ejecuta pruebas automáticas del sistema."""
    print("\n" + "="*50)
    print("EJECUTANDO PRUEBAS AUTOMÁTICAS")
    print("="*50)

    # Casos de prueba
    casos_prueba = [
        ('Ana García', '1234567890', 'ana@empresa.com', '3001234567'),
        ('Luis López', '0987654321', 'luis@empresa.com', '3009876543'),
        ('María Pérez', '1122334455', 'maria@empresa.com', '3112233445'),
    ]

    print("\n[1] Registrando clientes de prueba...")
    for nombre, cedula, correo, telefono in casos_prueba:
        try:
            cliente = Cliente(nombre, cedula, correo, telefono)
            clientes.append(cliente)
            print(f"{nombre}")
        except ValidacionError as e:
            logging.error(f'Validación fallida: {e}')
            print(f"{nombre}: {e}")

    print("\n[2] Creando reservas de prueba...")
    try:
        reserva1 = Reserva(clientes[0], servicios[0], 2)
        reserva1.procesar()
        reservas.append(reserva1)
        print(f"Reserva 1: {reserva1.cliente.nombre} → {reserva1.servicio.nombre}")

        reserva2 = Reserva(clientes[1], servicios[1], 3)
        reserva2.procesar()
        reservas.append(reserva2)
        print(f"Reserva 2: {reserva2.cliente.nombre} → {reserva2.servicio.nombre}")
    except ReservaError as e:
        logging.error(f'Error en reserva: {e}')
        print(f"Error: {e}")

    print("\n[3] Probando validaciones...")
    casos_invalidos = [
        ('', '123', 'correo@test.com', '3001234567', 'Nombre vacío'),
        ('Juan', '123', 'correo_invalido', '3001234567', 'Correo inválido'),
        ('Pedro', '123', 'correo@test.com', '123', 'Teléfono muy corto'),
    ]

    for nombre, cedula, correo, telefono, razon in casos_invalidos:
        try:
            Cliente(nombre, cedula, correo, telefono)
            print(f"{razon}: No se detectó error")
        except ValidacionError:
            print(f"{razon}: Error capturado correctamente")

    print("\n[4] Probando calculadora con sobrecarga...")
    calc = CalculadoraCostos()
    print(f"  {calc.calcular(5)}")
    print(f"  {calc.calcular(3.75)}")
    print(f"  {calc.calcular([(50000, 2), (40000, 1)])}")
    print(f"  {calc.calcular('PROMO20')}")

    print("\n✓ Pruebas completadas - Revise el archivo 'sistema_reservas.log'")


def menu():
    """Menú principal interactivo del sistema."""
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE RESERVAS - SOFTWARE FJ")
        print("="*50)
        print("1. Registrar cliente")
        print("2. Ver clientes")
        print("3. Ver servicios")
        print("4. Crear reserva")
        print("5. Ver reservas")
        print("6. Cancelar reserva")
        print("7. Ejecutar pruebas automáticas")
        print("8. Salir")
        print("="*50)

        try:
            opcion = input("\nSeleccione opción: ").strip()

            if opcion == '1':
                registrar_cliente()
            elif opcion == '2':
                listar_clientes()
            elif opcion == '3':
                listar_servicios()
            elif opcion == '4':
                crear_reserva()
            elif opcion == '5':
                ver_reservas()
            elif opcion == '6':
                cancelar_reserva()
            elif opcion == '7':
                pruebas_automaticas()
            elif opcion == '8':
                print("\nGracias por usar el sistema! Hasta luego.")
                logging.info('Sistema cerrado por usuario')
                break
            else:
                print("\nOpción inválida. Intente de nuevo.")

        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario")
            logging.warning('Sistema interrumpido por usuario')
        except Exception as e:
            logging.error(f'Error en menú: {e}')
            print(f'\nError: {e}')


# =====================================================================
# PUNTO DE ENTRADA
# =====================================================================

if __name__ == '__main__':
    logging.info('='*60)
    logging.info('INICIO DEL SISTEMA DE GESTIÓN DE RESERVAS')
    logging.info('='*60)
    
    menu()
