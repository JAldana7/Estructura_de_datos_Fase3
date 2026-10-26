from enum import Enum

class IDType(Enum):
    CC = "CC"
    CE = "CE"
    NUIP = "NUIP"
    PAS = "PAS"

class EmploymentType(Enum):
    EMPLOYEE = "Employee"
    INDEPENDENT = "Independent"

class DesiredService(Enum):
    UNEMPLOYMENT_SUBSIDY = "Unemployment Subsidy"
    PARK_ADMISSION = "Park Admission"
    TRAINING_COURSE = "Training Course"
    TRAVEL_PACKAGE = "Travel Package"
    PREVENTIVE_MEDICINE = "Preventive Medicine"

class StructureType(Enum):
    STACK = "Stack"
    QUEUE = "Queue"
    LIST = "List"