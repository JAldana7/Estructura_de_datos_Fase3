from dataclasses import dataclass
from datetime import datetime
from models.enums import IDType, EmploymentType, DesiredService
from models.fee_calculator import StandardFeeCalculator

@dataclass
class Affiliate:
    id_type: IDType
    id_number: str
    full_name: str
    current_income: float
    desired_service: DesiredService
    employment_type: EmploymentType
    affiliation_date: datetime
    affiliation_fee: float = 0.0

    def __post_init__(self):
        """Calculates affiliation fee automatically upon creation if not provided."""
        if self.affiliation_fee == 0.0:
            calculator = StandardFeeCalculator()
            self.affiliation_fee = calculator.calculate_fee(
                self.current_income, 
                self.employment_type, 
                self.desired_service
            )

    def to_tuple(self) -> tuple:
        """Utility method to easily populate Tkinter Treeview rows."""
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
