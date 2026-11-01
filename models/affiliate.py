# importaciones necesarias para la definición de la clase Affiliate
from dataclasses import dataclass
from datetime import datetime
from models.enums import IDType, EmploymentType, DesiredService
from models.fee_calculator import StandardFeeCalculator

@dataclass # decorador que permite crear una clase de datos con atributos y métodos automáticamente generados
class Affiliate:
    # atributos de la clase Affiliate
    id_type: IDType
    id_number: str
    full_name: str
    current_income: float
    desired_service: DesiredService
    employment_type: EmploymentType
    affiliation_date: datetime
    affiliation_fee: float = 0.0

    # método especial que se ejecuta después de la inicialización de la clase
    def __post_init__(self):
        if self.affiliation_fee == 0.0: # si la tarifa de afiliación es cero, se calcula automáticamente
            calculator = StandardFeeCalculator() # para calcular la tarifa de afiliación, se utiliza la clase StandardFeeCalculator
            self.affiliation_fee = calculator.calculate_fee(
                self.current_income, 
                self.employment_type, 
                self.desired_service
            )

    # método que devuelve la representación en forma de tupla de los atributos del afiliado
    def to_tuple(self) -> tuple:
        # metodo que devuelve la tupla de atributos del afiliado
        return (
            self.id_type.value,
            self.id_number,
            self.full_name,
            f"${self.current_income:,.2f}",
            self.employment_type.value,
            self.desired_service.value,
            f"${self.affiliation_fee:,.2f}",
            self.affiliation_date.strftime("%d/%m/%Y")
        )