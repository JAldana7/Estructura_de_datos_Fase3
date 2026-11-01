# importación de la clase Enum del módulo enum para definir enumeraciones
from enum import Enum

# definiciones de tipos de enumeraciones para los diferentes atributos de los afiliados
class IDType(Enum):
    CC = "CC"
    CE = "CE"
    NUIP = "NUIP"
    PAS = "PAS"

# definiciones de tipos de empleo de los afiliados
class EmploymentType(Enum):
    EMPLOYEE = "Employee"
    INDEPENDENT = "Independent"

# definiciones de servicios deseados por los afiliados
class DesiredService(Enum):
    UNEMPLOYMENT_SUBSIDY = "Unemployment Subsidy"
    PARK_ADMISSION = "Park Admission"
    TRAINING_COURSE = "Training Course"
    TRAVEL_PACKAGE = "Travel Package"
    PREVENTIVE_MEDICINE = "Preventive Medicine"

# definiciones de tipos de estructuras de datos para almacenar los afiliados
class StructureType(Enum):
    STACK = "Stack"
    QUEUE = "Queue"
    LIST = "List"