from logic import *

# Characters
mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")

characters = [mustard, plum, scarlet]

# Rooms
ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")

rooms = [ballroom, kitchen, library]

# Weapons
knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")

weapons = [knife, revolver, wrench]



symbols= characters + rooms +weapons
def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge,symbol):
            print(f"{symbol}: Yes")
        elif not model_check(knowledge,Not(symbol)):
            print(f"{symbol} : Maybe")

# # Knowledge base
knowledge = And(

    # At least one character committed the crime
    Or(mustard, plum, scarlet),

    # At least one room is the crime scene
    Or(ballroom, kitchen, library),

    # At least one weapon was used
    Or(knife, revolver, wrench)
    )
knowledge.add(Not(mustard))
knowledge.add(Not(revolver))
knowledge.add(Not(kitchen))
knowledge.add(Or(Not(scarlet), Not(library),Not(wrench)
                 ))

knowledge.add(Not(plum))
knowledge.add(Not(ballroom))
# print(knowledge.formula())
check_knowledge(knowledge)