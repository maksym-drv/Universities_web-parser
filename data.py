from dataclasses import dataclass

@dataclass
class Program:
    name: str
    study_format: str
    applications: int
    budget: int 
    contract: int
    price: int

@dataclass
class University:
    name: str
    specialities: list
    programs: list

@dataclass
class State:
    name: str
    universities: list