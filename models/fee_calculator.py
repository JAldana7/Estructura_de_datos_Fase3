from abc import ABC, abstractmethod
from models.enums import EmploymentType, DesiredService

class FeeCalculatorStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, monthly_income: float, service: DesiredService) -> float:
        pass

class StandardFeeCalculator(FeeCalculatorStrategy):
    """Calculates affiliation fee based on employment type, income ranges, and desired service."""
    
    def calculate_fee(self, monthly_income: float, employment_type: EmploymentType, service: DesiredService) -> float:
        base_fee = self._get_base_fee(monthly_income, employment_type)
        service_surcharge = self._get_service_surcharge(monthly_income, service)
        return base_fee + service_surcharge

    def _get_base_fee(self, income: float, employment: EmploymentType) -> float:
        if employment == EmploymentType.EMPLOYEE:
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
        else:  # EmploymentType.INDEPENDENT
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

    def _get_service_surcharge(self, income: float, service: DesiredService) -> float:
        if service == DesiredService.PARK_ADMISSION:
            return 2500.0
        elif service == DesiredService.TRAINING_COURSE:
            return 7500.0
        elif service == DesiredService.TRAVEL_PACKAGE:
            return 10000.0
        elif service == DesiredService.PREVENTIVE_MEDICINE:
            return income * 0.10  # 10% of current income
        return 0.0  # UNEMPLOYMENT_SUBSIDY or default