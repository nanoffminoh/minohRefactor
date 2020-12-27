from model.stats import Stats, empty_stats
from presets import preset_stat_name_list, preset_reward_types, preset_reward_display_name
from renpy_functions import shuffle_list


class Reward:
    def __init__(self, name, reward_type, stats=None, materials=0, rewards=None, obtainable=True, essential=False):
        self.name = name
        self.reward_type = reward_type
        self.stat_requirement = Stats(stats) or Stats(empty_stats)
        self.material_requirement = materials
        self.reward_requirement = rewards or []
        self.obtainable = obtainable
        self.essential = essential

    def meets_requirements(self, stats, rewards=None, team=None, material=0):
        rewards = rewards or []
        return self.meets_stat_requirements(stats) and\
            self.meets_reward_requirements(rewards) and\
            self.meets_type_requirements(team) and\
            self.meets_material_requirements(material) and\
            self.obtainable

    def meets_type_requirements(self, team=None):
        if team is not None:
            if self.reward_type not in preset_reward_types[team]:
                return False
        return True

    def meets_material_requirements(self, material):
        return self.material_requirement <= material

    def meets_stat_requirements(self, stats):
        return stats.meets(self.stat_requirement)

    def meets_reward_requirements(self, rewards=None):
        required_rewards = rewards or []
        meets = True
        for reward in self.reward_requirement:
            if reward not in required_rewards:
                meets = False
                break
        return meets

    def total_requirements(self):
        return self.stat_requirement.sum_stat() + self.material_requirement


class RewardList:
    def __init__(self):
        self.pending_rewards = []
        self.obtained_rewards = []

    def possible_rewards(self, stats=None, team=None, material=0):
        stats = stats or Stats()
        rewards = self.list_obtained_reward_names()
        possible_rewards = []
        for reward in self.pending_rewards:
            if reward.meets_requirements(stats=stats, rewards=rewards, team=team, material=material):
                possible_rewards.append(reward)
        return possible_rewards

    def add_pending_reward(self, reward):
        self.pending_rewards.append(reward)

    def get_pending_reward(self, reward_name):
        for reward in self.pending_rewards:
            if reward.name == reward_name:
                return reward

    def obtain_reward(self, reward_name):
        reward = self.get_pending_reward(reward_name)
        self.pending_rewards.remove(reward)
        self.obtained_rewards.append(reward)

    def list_pending_reward_names(self):
        return self.list_reward_names(my_list=self.pending_rewards)

    def list_obtained_reward_names(self):
        return self.list_reward_names(my_list=self.obtained_rewards)

    def list_reward_names(self, my_list=None):
        if my_list is None:
            my_list = self.obtained_rewards + self.pending_rewards
        reward_list = []
        for reward in my_list:
            reward_list.append(reward.name)
        return reward_list

    def is_obtained(self, reward_name):
        obtained = False
        for reward in self.obtained_rewards:
            if reward.name == reward_name:
                obtained = True
                break
        return obtained

    def determine_reward(self, stat_list):
        self.sort_rewards()
        return self.pending_rewards[0]

    def sort_rewards(self, priorities_list=None):
        shuffle_list(self.pending_rewards)
        self.sort_rewards_by_requirements_sum()
        if priorities_list is not None:
            self.sort_rewards_by_type(priorities_list)
        self.sort_put_essentials_on_top()

    def sort_put_essentials_on_top(self):
        essential_rewards = [reward for reward in self.pending_rewards if reward.essential]
        non_essential_rewards = [reward for reward in self.pending_rewards if not reward.essential]
        self.pending_rewards = essential_rewards + non_essential_rewards

    def sort_rewards_by_requirements_sum(self):
        self.pending_rewards.sort(key=lambda x: x.total_requirements(), reverse=True)

    def sort_rewards_by_type(self, priorities_list):
        sorted_list = []
        for stat in priorities_list:
            sublist = [reward for reward in self.pending_rewards if reward.reward_type == stat['stat']]
            sorted_list = sorted_list + sublist
        # add missing rewards at the end
        sublist = [reward for reward in self.pending_rewards if reward not in sorted_list]
        sorted_list = sorted_list + sublist
        self.pending_rewards = sorted_list

    def get_reward_choices(self, team_stats, material):
        # returns reward choices for RD
        choice_list = []
        for reward in self.possible_rewards(team_stats, "RD", material):
            name = preset_reward_display_name[reward.name] if reward.name in preset_reward_display_name else reward.name
            choice_list.append((name, reward.name))
        choice_list.append(("Ignore and keep researching.", "none"))
        return choice_list
