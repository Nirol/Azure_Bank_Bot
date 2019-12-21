from abc import ABC, abstractmethod


class IndentDetailsABS(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def update_entity(self, entity_name : str, entity_value : str)-> None:
        self.__dict__[entity_name] = entity_value