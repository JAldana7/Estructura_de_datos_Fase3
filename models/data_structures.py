# importaciones necesarias para la definición de las estructuras de datos
from abc import ABC, abstractmethod
from collections import deque
from typing import List, Optional
from models.affiliate import Affiliate

# clase abstracta base para las estructuras de datos
class BaseStructure(ABC):
    @abstractmethod
    def add(self, affiliate: Affiliate) -> None: # agrega un afiliado a la estructura de datos
        pass

    @abstractmethod
    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]: # elimina un afiliado de la estructura de datos
        pass

    @abstractmethod
    def get_all(self) -> List[Affiliate]: # devuelve todos los afiliados en la estructura de datos
        pass

    @abstractmethod
    def get_report(self) -> str: # devuelve un reporte de la estructura de datos
        pass

    @abstractmethod
    def is_empty(self) -> bool: # verifica si la estructura de datos está vacía
        pass

# clase para la implementación de una pila (stack) de afiliados
class AffiliateStack(BaseStructure):
    # implementación de una pila (stack) de afiliados
    def __init__(self):
        self._items: List[Affiliate] = []

    def add(self, affiliate: Affiliate) -> None: # agrega un afiliado a la pila (stack) de afiliados
        self._items.append(affiliate)  
 
    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]: # elimina un afiliado de la pila (stack) de afiliados
        if not self.is_empty():
            return self._items.pop() 
        return None

    def get_all(self) -> List[Affiliate]: # devuelve todos los afiliados en la pila (stack) de afiliados
        return list(reversed(self._items))  

    def is_empty(self) -> bool: # verifica si la pila (stack) de afiliados está vacía
        return len(self._items) == 0

    def get_report(self) -> str:
        total_fee = sum(item.affiliation_fee for item in self._items)
        return f"Total Affiliation Fees Sum: ${total_fee:,.2f}"

# clase para la implementación de una cola (queue) de afiliados
class AffiliateQueue(BaseStructure):
    # implementación de una cola (queue) de afiliados
    def __init__(self):
        self._items: deque[Affiliate] = deque()

    def add(self, affiliate: Affiliate) -> None: # agrega un afiliado a la cola (queue) de afiliados
        self._items.append(affiliate) 

    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]: # elimina un afiliado de la cola (queue) de afiliados
        if not self.is_empty():
            return self._items.popleft() # elimina el primer elemento de la cola (queue) de afiliados
        return None

    def get_all(self) -> List[Affiliate]: # devuelve todos los afiliados en la cola (queue) de afiliados
        return list(self._items)

    def is_empty(self) -> bool: # verifica si la cola (queue) de afiliados está vacía
        return len(self._items) == 0

    def get_report(self) -> str:
        return f"Total Enqueued Records: {len(self._items)}"

# clase para la implementación de una lista (list) de afiliados
class AffiliateList(BaseStructure):
    # implementación de una lista (list) de afiliados
    def __init__(self):
        self._items: List[Affiliate] = []

    def add(self, affiliate: Affiliate) -> None: # agrega un afiliado a la lista (list) de afiliados
        self._items.append(affiliate)

    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]: # elimina un afiliado de la lista (list) de afiliados
        if not id_number:
            return None
            
        for index, item in enumerate(self._items):
            if item.id_number == id_number:
                return self._items.pop(index) # elimina el afiliado de la lista (list) de afiliados por su número de identificación
        return None

    def find_by_id(self, id_number: str) -> Optional[Affiliate]: # busca un afiliado en la lista (list) de afiliados por su número de identificación
        for item in self._items:
            if item.id_number == id_number: 
                return item
        return None

    def get_all(self) -> List[Affiliate]:
        return list(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def get_report(self) -> str: # devuelve un reporte de la lista (list) de afiliados
        if self.is_empty():
            return "Average Income: $0.00"
        avg_income = sum(item.current_income for item in self._items) / len(self._items)
        return f"Average Current Income: ${avg_income:,.2f}"