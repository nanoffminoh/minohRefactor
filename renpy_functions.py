import random
from random import randint


def shuffle_list(my_list):
    # return sorted(my_list, key=lambda x: renpy.random.random())
    random.shuffle(my_list)

def print_on_textbox(text):
    # renpy.say(narrator, text)
    print(text)

def random_between(int1, int2):
    # renpy.random.randint(int1, int2)
    return randint(int1, int2)

#def show_team(name_list):
#    if len(name_list)>0:
#        renpy.show(name_list[0], [xalcenter] if len(name_list) != 2 else [xalright])
#    if len(name_list)>1:
#        renpy.show(name_list[1], [xalleft] if len(name_list) == 2 else [xallefter])
#    if len(name_list)>2:
#        renpy.show(name_list[2], [xalrighter])

#def hide_team(name_list):
#    for guest in name_list:
#        renpy.hide(guest)

#def team_pose(name_list, emote='neutral'):
#    for guest in name_list:
#        globals()[guest].change('posing', emote)


#transform xalcenter:
#    xalign 0.5
#    yalign 1.0

#transform xalleft:
#    xalign 0.1
#    yalign 1.0

#transform xalright:
#    xalign 0.9
#    yalign 1.0

#transform xallefter:
#    xalign -0.1
#    yalign 1.0

#transform xalrighter:
#    xalign 1.1
#    yalign 1.0
