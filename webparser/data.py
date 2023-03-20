from dataclasses import dataclass

@dataclass
class Offer:
    program: str
    speciality: str
    form: str
    applications: int
    budget: int
    contract: int
    price: int

@dataclass
class University:
    name: str
    offers: list[Offer]    

@dataclass
class Region:
    name: str
    institutes: list[University]
