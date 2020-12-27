from model.guest import GuestList
from model.inventory import Inventory
from model.couple import RelationshipList
from renpy_functions import random_between, print_on_textbox


def calculate_rd_team_stats(inventory, guest_list, relationship_list):
    rd_team = guest_list.get_rd_team()
    rd_team_stats = rd_team.sum_stats()
    passive_bonus = inventory.get_passive_bonus()
    relationship_bonus = relationship_list.get_relationships_with_guests(rd_team.names()).sum_bonus()
    return rd_team_stats + passive_bonus + relationship_bonus


def calculate_exploration_team_stats(inventory, guest_list, relationship_list):
    ex_team = guest_list.get_exploration_team()
    ex_team_stats = ex_team.sum_stats()
    passive_bonus = inventory.get_passive_bonus()
    relationship_bonus = relationship_list.get_relationships_with_guests(ex_team.names()).sum_bonus()
    return ex_team_stats + passive_bonus + relationship_bonus


def determine_reward(reward_list, team_stats, team=None, materials=0):
    if team == "RD":
        team_stats = team_stats.filter_rd()
    if team == "Exploration":
        team_stats = team_stats.filter_exploration()
    if len(reward_list.possible_rewards(stats=team_stats, team=team, material=materials)) > 0:
        reward_list.sort_rewards(team_stats.list_stats())
        return reward_list.possible_rewards(stats=team_stats, team=team, material=materials)[0]
    else:
        return 0


def determine_rd_reward(reward_list, inventory, guest_list, relationship_list):
    team_stats = inventory.accumulated_stats['RD'] + calculate_rd_team_stats(inventory, guest_list, relationship_list)
    return determine_reward(reward_list, team_stats, team='RD', materials=inventory.rawMaterials)


def determine_exploration_reward(reward_list, inventory, guest_list, relationship_list):
    team_stats = inventory.accumulated_stats['Exploration'] + calculate_exploration_team_stats(inventory, guest_list, relationship_list)
    return determine_reward(reward_list, team_stats, team='Exploration', materials=inventory.rawMaterials)


def danger_attack(guest_list, background):
    # upon a failed danger event determines which teammates get attacked.
    someone_injured = False
    for guest in guest_list.guests:
        if guest.status == 'Exploration':
            chance = random_between(1, 7 if background == 'speedrunner' else 5)
            if chance < 4:
                someone_injured = True
                days = 'a day' if chance == 1 else str(chance) + " days"
                print_on_textbox(guest.name + " is injured. He will take " + days + " to recover.")
                guest_list.disableGuest(guest.name, chance)
    if not someone_injured:
        print_on_textbox("Thankfully, no one was injured. You make a mental note to be more careful next time.")
    return someone_injured


def get_relationship_routes(guest_list, relationship_list):
    return relationship_list.get_available_couple_routes(guest_list.get_guests_can_start_relationship(), guest_list.get_guests_can_date())


def survey(exploration_stats, background, inventory):
    # determines your survey reward.
    # if you meet a special reward the function returns a special label
    my_label = 'none'
    survey_stat = exploration_stats.get_value('Surveying')
    random_number = random_between(1, 100)
    if background == "speedrunner":
        random_number += 10
    if random_number <= 10:
        print_on_textbox("Your team didn't find any raw materials.")
    elif random_number < 60:
        print_on_textbox("Your team found " + str(survey_stat) + " raw materials!")
        inventory.rawMaterials += survey_stat
    else:
        survey_stat *= 2
        print_on_textbox("Your team got really lucky, and found " + str(survey_stat) + " raw materials, twice what you expected!")
        inventory.rawMaterials += survey_stat
    # if random_number == 100:
    #    my_label='Cool'
    # example of an extra surveying reward if you get super lucky
    return my_label
