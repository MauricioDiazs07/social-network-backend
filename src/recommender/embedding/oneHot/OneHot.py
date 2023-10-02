from ._simple import simpleOneHot
from typing import List


class OneHotClass:
    """Docstring."""

    def simple(self, categories:List, elements:List) -> List:
        """Docstring."""
        return simpleOneHot(categories, elements)