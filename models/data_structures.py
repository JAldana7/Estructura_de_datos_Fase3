from abc import ABC, abstractmethod
from collections import deque
from typing import List, Optional
from models.affiliate import Affiliate

class BaseStructure(ABC):
    """Abstract Base Class (Liskov Substitution & Interface Segregation Principles)"""
    
    @abstractmethod
    def add(self, affiliate: Affiliate) -> None:
        pass

    @abstractmethod
    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]:
        pass

    @abstractmethod
    def get_all(self) -> List[Affiliate]:
        pass

    @abstractmethod
    def get_report(self) -> str:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass


class AffiliateStack(BaseStructure):
    """Stack implementation using Python list (LIFO)"""
    
    def __init__(self):
        self._items: List[Affiliate] = []

    def add(self, affiliate: Affiliate) -> None:
        self._items.append(affiliate)  # Push

    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]:
        if not self.is_empty():
            return self._items.pop()  # Pop LIFO
        return None

    def get_all(self) -> List[Affiliate]:
        return list(reversed(self._items))  # Return top-first for visual display

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def get_report(self) -> str:
        """Report for Stack: Total sum of affiliation fees in stack."""
        total_fee = sum(item.affiliation_fee for item in self._items)
        return f"Total Affiliation Fees Sum: ${total_fee:,.2f}"


class AffiliateQueue(BaseStructure):
    """Queue implementation using collections.deque (FIFO)"""
    
    def __init__(self):
        self._items: deque[Affiliate] = deque()

    def add(self, affiliate: Affiliate) -> None:
        self._items.append(affiliate)  # Enqueue

    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]:
        if not self.is_empty():
            return self._items.popleft()  # Dequeue FIFO
        return None

    def get_all(self) -> List[Affiliate]:
        return list(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def get_report(self) -> str:
        """Report for Queue: Count of current records in queue."""
        return f"Total Enqueued Records: {len(self._items)}"


class AffiliateList(BaseStructure):
    """List implementation using Python list with search-and-delete capability"""
    
    def __init__(self):
        self._items: List[Affiliate] = []

    def add(self, affiliate: Affiliate) -> None:
        self._items.append(affiliate)

    def remove(self, id_number: Optional[str] = None) -> Optional[Affiliate]:
        if not id_number:
            return None
            
        for index, item in enumerate(self._items):
            if item.id_number == id_number:
                return self._items.pop(index)
        return None

    def find_by_id(self, id_number: str) -> Optional[Affiliate]:
        for item in self._items:
            if item.id_number == id_number:
                return item
        return None

    def get_all(self) -> List[Affiliate]:
        return list(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def get_report(self) -> str:
        """Report for List: Average current income of members in list."""
        if self.is_empty():
            return "Average Income: $0.00"
        avg_income = sum(item.current_income for item in self._items) / len(self._items)
        return f"Average Current Income: ${avg_income:,.2f}"