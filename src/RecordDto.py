from dataclasses import dataclass


@dataclass
class RecordDto:
    date: str
    time: str
    duration: int
    act: str
    category_1: str = None
    category_2: str = None
