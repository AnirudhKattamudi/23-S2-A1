from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR

#import the required ADTs
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.stack_adt import ArrayStack

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.team_mode = team_mode
        
        #initialise all the ADTs to their corresponding team mode
        if team_mode == self.TeamMode.FRONT:
            self.original_team = ArrayStack(MonsterTeam.TEAM_LIMIT)
        
        elif team_mode == self.TeamMode.BACK:
            self.original_team = CircularQueue(MonsterTeam.TEAM_LIMIT)
        
        elif team_mode == self.TeamMode.OPTIMISE:
            self.original_team = ArraySortedList(MonsterTeam.TEAM_LIMIT)

        #gets rid of sort key error
        if 'sort_key' in kwargs:
            del(kwargs['sort_key'])
            
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
        
    def __len__(self):
        len(self.original_team)
    
    def add_to_team(self, monster: MonsterBase):
        #depending on what type of team mode it is, it will use their
        #element adding function to add monsters to team if its empty
        if self.team_mode == self.TeamMode.FRONT:
            self.original_team.push(monster)
        if self.team_mode == self.TeamMode.BACK:
            self.original_team.append(monster)
        if self.team_mode == self.TeamMode.OPTIMISE:
            self.original_team.add(monster)
    
    def retrieve_from_team(self) -> MonsterBase:
        #same as add_to_team, however we are now removing monsters when 
        #required, and only when there are 1 or more monsters
        if len(self) == 0:
            raise ValueError("Team is empty, there are no monsters!")

        if self.team_mode == self.TeamMode.FRONT:
            return self.original_team.pop()
        elif self.team_mode == self.TeamMode.BACK:
            return self.original_team.serve()
        #delete_at_index needs a parameter and from the diagram provided
        #it can be seen that the first monster is always removed
        elif self.team_mode == self.TeamMode.OPTIMISE:
            return self.original_team.delete_at_index(0)
    
        
    def special(self) -> None:
        #when the team selection is FRONT, we need to make sure that the size is atleast 3
        #initialise the reversed monsters items to a queue as it follows a FIFO implementation
        if self.team_mode == self.TeamMode.FRONT and len(self.original_team) >= 3:
            reversed_monsters_queue = CircularQueue(min(3, len(self.original_team)))
            #if it is within the length of the team, pop the first three and then push them
            for _ in range(len(self.original_team)):
                reversed_monsters_queue.push(self.original_team.pop())
            #using the elements that were originally popped, push them back into the team after
            #being reversed
            for _ in range(len(reversed_monsters_queue)):
                self.original_team.push(reversed_monsters_queue.serve())

        
        if self.team_mode == self.TeamMode.BACK:
            #check how many monsters we want to move around
            create_count = len(self.original_team)//2
            #make the first half a queue as we can use the FIFO implementation to move them around
            created_queue_first_half = CircularQueue[MonsterBase](create_count)
            #make last half a stack so we can pop and push as required as it uses a LIFO implementation
            bottom_half_stack = ArrayStack[MonsterBase](len(self.original_team))
            
            #moves the first half of the team to the created queue
            for _ in range(create_count):
                created_queue_first_half.append(self.original_team.serve())
            #moves the bottom half to the created stack
            for _ in range(self.original_team):
                bottom_half_stack.push(self.original_team.serve())
            #moves the monsters from created stack back into the team
            for _ in range(len(bottom_half_stack)):
                self.original_team.append(bottom_half_stack.pop())
            #moves the monsters from the created queue into the team
            for _ in range(len(created_queue_first_half)):
                self.original_team.append(created_queue_first_half.serve())

        if self.team_mode == self.TeamMode.OPTIMISE:
            pass

    def regenerate_team(self) -> None:
        #while
        for i in range(len(self)):
            if self.team_mode == self.TeamMode.FRONT:
                monsters = self.original_team.clear()
                monsters.set_hp(monsters.get_max_hp())
                monsters.level() == monsters.get_level(1)
                self.original_team == self.add_to_team(monsters)
                
            elif self.team_mode == self.TeamMode.BACK:
                self.original_team.clear()
                monsters = self.original_team.clear()
                monsters.set_hp(monsters.get_max_hp())
                monsters.level() == monsters.get_level(1)
                self.original_team == self.add_to_team(monsters)

            elif self.team_mode == self.TeamMode.OPTIMISE:
                self.original_team.reset()
                monsters = self.original_team.clear()
                monsters.set_hp(monsters.get_max_hp())
                monsters.level() == monsters.get_level(1)
                self.original_team == self.add_to_team(monsters)

        
    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        raise NotImplementedError

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        
        for monsters in provided_monsters:
            if monsters.can_be_spawned():
                self.add_to_team(monsters)

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
