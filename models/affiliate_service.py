# importacion necesaria para la definición de tipos
from typing import List, Optional
from models.enums import StructureType
from models.affiliate import Affiliate
from models.data_structures import AffiliateStack, AffiliateQueue, AffiliateList, BaseStructure

# clase para el servicio de afiliados
class AffiliateService:
    # Constructor de la clase AffiliateService
    def __init__(self):
        # Inicialización de las estructuras de datos para cada tipo
        self._structures = {
            StructureType.STACK: AffiliateStack(),
            StructureType.QUEUE: AffiliateQueue(),
            StructureType.LIST: AffiliateList()
        }

    # Función para obtener la estructura de datos específica
    def get_structure(self, structure_type: StructureType) -> BaseStructure:
        return self._structures[structure_type] # Devuelve la estructura de datos correspondiente al tipo especificado

    # Función para agregar un afiliado a la estructura de datos especificada
    def add_affiliate(self, structure_type: StructureType, affiliate: Affiliate) -> None:
        self._structures[structure_type].add(affiliate) # agrega el afiliado a la estructura de datos correspondiente al tipo especificado

    # Función para eliminar un afiliado de la estructura de datos especificada
    def remove_affiliate(self, structure_type: StructureType, id_number: Optional[str] = None) -> Optional[Affiliate]:
        return self._structures[structure_type].remove(id_number) # elimina el afiliado de la estructura corespondiente

    # Función para obtener todos los registros de la estructura de datos especificada
    def get_all_from_structure(self, structure_type: StructureType) -> List[Affiliate]:
        return self._structures[structure_type].get_all() # devuelve todos los registros de la estructura de datos correspondiente al tipo especificado

    # Función para obtener un reporte de la estructura de datos especificada
    def get_structure_report(self, structure_type: StructureType) -> str:
        return self._structures[structure_type].get_report() # devuelve un reporte de la estructura de datos correspondiente al tipo especificado

    # Función para verificar si la estructura de datos especificada está vacía
    def is_structure_empty(self, structure_type: StructureType) -> bool:
        return self._structures[structure_type].is_empty()

    # Función para buscar un afiliado por su número de identificación en la lista
    def find_in_list(self, id_number: str) -> Optional[Affiliate]:
        list_structure: AffiliateList = self._structures[StructureType.LIST]
        return list_structure.find_by_id(id_number) # devuelve el afiliado encontrado en la lista por su número de identificación, o None si no se encuentra