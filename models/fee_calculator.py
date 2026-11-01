# importaciones necesarias para la definición de la clase FeeCalculatorStrategy y sus implementaciones
from abc import ABC, abstractmethod
from models.enums import EmploymentType, DesiredService

# clase abstracta para la estrategia de cálculo de tarifas de afiliación
class FeeCalculatorStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, monthly_income: float, service: DesiredService) -> float:
        pass

# clase concreta para la estrategia de cálculo de tarifas estándar
class StandardFeeCalculator(FeeCalculatorStrategy):
    # implementación de la estrategia de cálculo de tarifas estándar
    def calculate_fee(self, monthly_income: float, employment_type: EmploymentType, service: DesiredService) -> float:
        base_fee = self._get_base_fee(monthly_income, employment_type)
        service_surcharge = self._get_service_surcharge(monthly_income, service)
        return base_fee + service_surcharge # devuelve la suma de la tarifa base y el recargo por servicio deseado

    # función privada para obtener la tarifa base según el ingreso mensual y el tipo de empleo
    def _get_base_fee(self, income: float, employment: EmploymentType) -> float:
        if employment == EmploymentType.EMPLOYEE: # para tipo de empleo dependiente
            if income <= 2000000:
                return 45000.0
            elif income <= 3000000:
                return 60000.0
            elif income <= 4000000:
                return 75000.0
            elif income <= 5000000:
                return 90000.0
            else:
                return 150000.0
        else:  # para tipo de empleo independiente
            if income <= 2000000:
                return 10000.0
            elif income <= 3000000:
                return 20000.0
            elif income <= 4000000:
                return 30000.0
            elif income <= 5000000:
                return 40000.0
            else:
                return 80000.0

    # función privada para obtener el recargo por servicio deseado según el ingreso mensual y el servicio
    def _get_service_surcharge(self, income: float, service: DesiredService) -> float:
        if service == DesiredService.PARK_ADMISSION:
            return 2500.0
        elif service == DesiredService.TRAINING_COURSE:
            return 7500.0
        elif service == DesiredService.TRAVEL_PACKAGE:
            return 10000.0
        elif service == DesiredService.PREVENTIVE_MEDICINE:
            return income * 0.10  # 10% del ingreso mensual
        return 0.0  # no hay recargo para el subsidio de desempleo