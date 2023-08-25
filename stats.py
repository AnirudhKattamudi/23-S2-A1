import abc

from data_structures.referential_array import ArrayR

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp
        

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        # TODO: Implement
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    #need to create a function such that it can analyse the reverse polish notation
    def get_attack(self, level: int):
    #     def evaluate_expression(self, level:int, expressions: List[str]) -> int:
    #         open_stack = []
    #         operators = {"+", "-", "*", "/", "power", "sqrt", "middle"}

    #         for operator in expressions:
    #             if operator not in operators:
    #                 if operator == "level":
    #                     stack.append(level)
        raise NotImplementedError

                        


            
        

    def get_defense(self, level: int):
        raise NotImplementedError

    def get_speed(self, level: int):
        raise NotImplementedError

    def get_max_hp(self, level: int):
        raise NotImplementedError
