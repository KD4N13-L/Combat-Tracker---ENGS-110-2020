import json
from random import randint
from random import seed
import os.path

seed(randint(1, 100))


class Participant:

    def __init__(self, name, modifier, initiative, player):
        self.name = name
        self.modifier = modifier
        self.initiative = initiative
        self.player = player

    def display_participant(self):
        if self.modifier >= 0:
            new_mod = "+" + str(self.modifier)
            print(self.initiative, ":", self.name, "(", new_mod, ")")
        else:
            print(self.initiative, ":", self.name, "(", self.modifier, ")")


class Initiative:

    def __init__(self):
        self.creatures = []
        self.amount = 0

    def update(self, creature_list):
        sorting_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                           "s", "t", "u", "v", "w", "x", "y", "z", "misc", "npcs"]
        while True:
            alph_number = input("Input the creature's alphabetical sorting letter. ---- ")
            if alph_number in sorting_letters:
                with open('' + alph_number + '.json') as data_file:
                    dictionary = json.load(data_file)
                while 'name' not in dictionary.keys():
                    hier = input("Input the creature's name. ---- ")
                    while hier not in dictionary:
                        hier = input("Such a creature doesn't exit. Try again. ---- ")
                    dictionary = dictionary['' + hier + '']
                name = dictionary["name"]
                modifier = int(dictionary["dexterity"])
                initiative = randint(1, 20) + modifier
                player = False
                creature = Participant(name, modifier, initiative, player)
                creature_list.append(creature)
                print(creature.name, "has been added to the initiative!")
                return
            else:
                print("Such an alphabetical sorting letter doesn't exit.")

    def import_npcs(self, creature_amount):
        self.creatures.clear()
        creature_amount = int(creature_amount)
        while True:
            if creature_amount == 0:
                blank_list = []
                return blank_list
            else:
                for check in range(0, 15):
                    if creature_amount == check:
                        for i in range(0, creature_amount):
                            self.update(self.creatures)
                        return
                print("Please insert a NON-negative INTEGER from 0 to 15")

    def display_current_list(self):
        for creature in self.creatures:
            creature.display_participant()

    def import_char(self, participant):
        self.creatures.append(participant)
        print(participant.name, "has been added to the initiative!")
        self.amount += 1

    def sort_creatures(self):
        def initiative_sorter(participant):
            return participant.initiative

        self.creatures.sort(key=initiative_sorter, reverse=True)
        list_length = len(self.creatures)
        for index1 in range(list_length - 1):
            index2 = index1 + 1
            if self.creatures[index1].initiative == self.creatures[index2].initiative:
                if self.creatures[index1].modifier < self.creatures[index2].modifier:
                    temp = self.creatures[index1]
                    self.creatures[index1] = self.creatures[index2]
                    self.creatures[index2] = temp
                elif self.creatures[index1].modifier == self.creatures[index2].modifier:
                    if self.creatures[index1].player:
                        print(self.creatures[index1].name, "is tied on initiative with another participant. Ask them "
                                                           "to roll initiative again.")
                        initiative1 = int(input("Input the reult. ---- "))
                    else:
                        initiative1 = randint(1, 20) + self.creatures[index1].modifier
                    if self.creatures[index2].player:
                        print(self.creatures[index2].name, "is tied on initiative with another participant. Ask them "
                                                           "to roll initiative again.")
                        initiative2 = int(input("Input the reult. ---- "))
                    else:
                        initiative2 = randint(1, 20) + self.creatures[index2].modifier
                    if initiative1 < initiative2:
                        temp = self.creatures[index1]
                        self.creatures[index1] = self.creatures[index2]
                        self.creatures[index2] = temp
        return self.creatures


class Player_list:

    def __init__(self):
        self.amount = 0
        self.participants = []

    def create_players(self):
        amount = int(input("How many PCs are participating? ---- "))
        i_pc = 1
        dictionary_file_name = input("What would you like to name the new players file? ---- ")
        dictionary_destination = {"amount": amount}
        while i_pc <= amount:
            value_pc = 'player%d' % i_pc
            player = {}
            player[value_pc] = {"name": "blank", "initiative": 0, "dexterity": 0}
            print("Input information of PC", i_pc)
            player[value_pc].update({"name": input("Name: ")})
            player[value_pc].update({"initiative": 10})
            player[value_pc].update({"dexterity": int(input("Dexterity Modifier: "))})
            dictionary_destination.update({value_pc: player[value_pc]})
            i_pc += 1
        with open('' + dictionary_file_name + '.json', "w") as file:
            json.dump(dictionary_destination, file, indent=2)

    def import_players(self, initiative_list):
        while True:
            dictionary_name = input("What is the name of the Players File? ---- ")
            dictionary_file = '' + dictionary_name + '.json'
            manager = os.path.isfile(dictionary_file)
            if manager:
                with open(dictionary_file) as data_file:
                    dictionary = json.load(data_file)
                i_pc = 1
                updated_list = []
                while i_pc <= int(dictionary["amount"]):
                    value_pc = 'player%d' % i_pc
                    name = dictionary['' + value_pc + '']["name"]
                    modifier = dictionary['' + value_pc + '']["dexterity"]
                    print(name)
                    initiative = int(input("Initiative Score: "))
                    player = True
                    player = Participant(name, modifier, initiative, player)
                    updated_list.append(player)
                    self.participants += updated_list
                    i_pc += 1
                    updated_list = []
                initiative_list.creatures += self.participants
                return
            else:
                print("Such a Players File doesn't exit.")


# ---------------------------------------------------------------------------------------------------------------------

def main():
    init = Initiative()
    plays = Player_list()
    npc_number = int(input("How many NPCs are participating (0 to 15)? ---- "))
    init.import_npcs(npc_number)
    #plays.create_players()
    plays.import_players(init)
    init.sort_creatures()
    init.display_current_list()


main()