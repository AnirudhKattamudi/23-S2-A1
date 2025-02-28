from __future__ import annotations
import abc

from stats import Stats

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        self.simple_mode = simple_mode
        self.level = level
        self.original_level = level
        #initial intialisation for all parameters

        #choose whether you want to use simple or complex stats
        if simple_mode:
            self.stats = self.get_simple_stats() #if they choose simple stats, call that method 
            #otherwise use the other method
        else: 
            self.stats = self.get_complex_stats()
            
        
        self.current_hp = self.get_max_hp() #initialise the current hp as the max hp at the start

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        hp_to_be_maintained = self.get_max_hp() - self.get_hp() #this gives us the value of what needs to be remained constant
        self.level += 1
        self.set_hp(self.get_max_hp() - hp_to_be_maintained)

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.current_hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.current_hp = val
        #changes the current hp to whatever 'val' is

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.stats.get_attack()

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.stats.get_defense()

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.stats.get_speed()

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.stats.get_max_hp()
    
    #for the last four methods, the values are found through by calling the function
    #and looking for the current value

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        if self.current_hp > 0:
            return True
        else:
            return False

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP
        raise NotImplementedError
      

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        if self.get_evolution() is not None and self.level > self.original_level:
                return True
        else: 
            return False 
    
    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        evolution_check = self.get_evolution()
        hp_to_be_maintained = self.get_max_hp() - self.current_hp

        if evolution_check is None:
            return ValueError("This monster cannot be evolved")
        
        else:
            evolved_monster = evolution_check(simple_mode = self.simple_mode, level = self.level)
            evolved_monster.set_hp(evolved_monster.get_max_hp() - hp_to_be_maintained)
            return evolved_monster
    
    def __str__(self):
        return f"LV.{self.get_level()} {self.get_name()}, {self.current_hp}/{self.get_max_hp()} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
