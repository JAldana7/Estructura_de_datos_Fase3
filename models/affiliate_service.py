from typing import List, Optional
from models.enums import StructureType
from models.affiliate import Affiliate
from models.data_structures import AffiliateStack, AffiliateQueue, AffiliateList, BaseStructure

class AffiliateService:
    """
    Facade service to manage the lifecycle and operations of linear data structures 
    (Stack, Queue, and List) in main memory.
    """

    def __init__(self):
        # Initialize the three linear data structures in memory
        self._structures = {
            StructureType.STACK: AffiliateStack(),
            StructureType.QUEUE: AffiliateQueue(),
            StructureType.LIST: AffiliateList()
        }

    def get_structure(self, structure_type: StructureType) -> BaseStructure:
        """Returns the specific data structure instance."""
        return self._structures[structure_type]

    def add_affiliate(self, structure_type: StructureType, affiliate: Affiliate) -> None:
        """Adds an affiliate to the specified structure following its native behavior."""
        self._structures[structure_type].add(affiliate)

    def remove_affiliate(self, structure_type: StructureType, id_number: Optional[str] = None) -> Optional[Affiliate]:
        """Removes an affiliate from the specified structure based on its native removal logic."""
        return self._structures[structure_type].remove(id_number)

    def get_all_from_structure(self, structure_type: StructureType) -> List[Affiliate]:
        """Retrieves all records from the selected structure to populate views."""
        return self._structures[structure_type].get_all()

    def get_structure_report(self, structure_type: StructureType) -> str:
        """Generates the required report string for the selected structure."""
        return self._structures[structure_type].get_report()

    def is_structure_empty(self, structure_type: StructureType) -> bool:
        """Checks if the selected structure has no elements."""
        return self._structures[structure_type].is_empty()

    def find_in_list(self, id_number: str) -> Optional[Affiliate]:
        """Helper method to check if a record exists in the List structure prior to removal."""
        list_structure: AffiliateList = self._structures[StructureType.LIST]
        return list_structure.find_by_id(id_number)