from model.reward import RewardList, Reward
from model.stats import Stats, empty_stats
from model.guest import Guest
from model.couple import Relationship, RelationshipList


def load_reward_list(reward_dict, reward_list):
    for reward_name in reward_dict.keys():
        if reward_name not in reward_list.list_reward_names():
            new_reward = load_reward(reward_name, reward_dict[reward_name])
            reward_list.add_pending_reward(new_reward)


def load_reward(reward_name, reward_dict):
    reward = reward_dict.copy()
    reward_type = reward['type']
    reward.setdefault('materials', 0)
    reward.setdefault('stats', empty_stats)
    reward.setdefault('rewards', [])
    reward.setdefault('obtainable', True)
    reward.setdefault('essential', False)
    stats = reward['stats']
    materials = reward['materials']
    rewards = reward['rewards']
    obtainable = reward['obtainable']
    essential = reward['essential']

    new_reward = Reward(reward_name, reward_type, stats, materials, rewards, obtainable, essential)
    return new_reward


def load_guest(guest_name, guest_stat_dict):
    stats = guest_stat_dict[guest_name]
    return Guest(guest_name, stats)


def load_relationships(relationship_dict, relationship_list):
    for relationship_name in relationship_dict.keys():
        if relationship_list.get_relationship_status(relationship_name) == 'missing':
            relationship = relationship_dict[relationship_name]
            members = relationship_name.split(',')

            new_relationship = Relationship(members, stats=relationship['stats'], enabled=relationship['enabled'])
            relationship_list.add_relationship(new_relationship)
