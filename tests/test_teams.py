import unittest
from access.team import calculate_rd_team_stats, calculate_exploration_team_stats, determine_reward, determine_rd_reward
from presets import preset_guest_stats, preset_couple_stats
from tests import REWARD_WIFI, REWARD_WINE, REWARD_TABLET2, REWARD_TABLET1
from model.guest import Guest, GuestList
from model.inventory import Inventory
from model.couple import RelationshipList, Relationship
from model.stats import Stats
from model.reward import RewardList


class TeamsTest(unittest.TestCase):

    def test_initialized_stats(self):
        luke = Guest('Luke', preset_guest_stats['Luke'])
        guest_list = GuestList()
        guest_list.add_guest(luke)
        inventory = Inventory()
        relationship_list = RelationshipList()
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats())

    def test_send_guest_to_rd_and_ex(self):
        luke_stats = preset_guest_stats['Luke']
        luke = Guest('Luke', luke_stats)
        guest_list = GuestList()
        guest_list.add_guest(luke)
        inventory = Inventory()
        relationship_list = RelationshipList()
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats())
        self.assertEqual(calculate_exploration_team_stats(inventory, guest_list, relationship_list), Stats())
        guest_list.send_guest_to_rd('Luke')
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats(luke_stats))
        self.assertEqual(calculate_exploration_team_stats(inventory, guest_list, relationship_list), Stats())
        guest_list.send_guest_to_exploration('Luke')
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats())
        self.assertEqual(calculate_exploration_team_stats(inventory, guest_list, relationship_list), Stats(luke_stats))

    def test_add_passive_bonus_to_rd(self):
        guest_list = GuestList()
        inventory = Inventory()
        relationship_list = RelationshipList()
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats())
        self.assertEqual(calculate_exploration_team_stats(inventory, guest_list, relationship_list), Stats())
        inventory.increase_passive_bonus('Tech', 4)
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats({'Tech': 4}))

    def test_relationship_bonus(self):
        guest_list = GuestList()
        inventory = Inventory()
        relationship_list = RelationshipList()
        luke_stats = preset_guest_stats['Luke']
        luke = Guest('Luke', luke_stats)
        black_stats = preset_guest_stats['Black']
        black = Guest('Black', black_stats)
        guest_list.add_guest(luke)
        guest_list.add_guest(black)
        luke_black_stats = preset_couple_stats['Luke,Black']
        luke_black = Relationship(['Luke', 'Black'], luke_black_stats)
        relationship_list.add_relationship(luke_black)
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats())
        # move Luke to RD
        guest_list.send_guest_to_rd('Luke')
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats(luke_stats))
        # move Black to RD
        guest_list.send_guest_to_rd('Black')
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list),
                         Stats(luke_stats) + Stats(black_stats))
        # complete Luke and Black's relationship
        relationship_list.advance_relationship('Luke,Black', 1, 1)
        self.assertEqual(relationship_list.get_relationship_status('Luke,Black'), 'complete')
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list),
                         Stats(luke_stats) + Stats(black_stats) + Stats(luke_black_stats))

    def test_determine_reward(self):
        reward_list = RewardList()
        reward_list.add_pending_reward(REWARD_WIFI)
        reward_list.add_pending_reward(REWARD_TABLET1)
        reward_list.add_pending_reward(REWARD_WINE)
        reward_list.add_pending_reward(REWARD_TABLET2)
        guest_list = GuestList()
        luke_stats = preset_guest_stats['Luke']
        luke = Guest('Luke', luke_stats)
        kota_stats = preset_guest_stats['Kota']
        kota = Guest('Kota', kota_stats)
        black_stats = preset_guest_stats['Black']
        black = Guest('Black', black_stats)
        guest_list.add_guest(luke)
        guest_list.add_guest(kota)
        guest_list.add_guest(black)

        reward = determine_reward(reward_list, guest_list.get_rd_team().sum_stats(), team='RD', materials=0)
        self.assertEqual(reward, 0)
        guest_list.send_guest_to_exploration('Kota')
        reward = determine_reward(reward_list, guest_list.get_rd_team().sum_stats(), team='RD', materials=0)
        self.assertEqual(reward, 0)
        self.assertEqual(guest_list.get_exploration_team().sum_stats().get_value('Memento'), 2)
        reward = determine_reward(reward_list, guest_list.get_exploration_team().sum_stats(), team='Exploration', materials=0)
        self.assertTrue(reward.name in ['Tablet1', 'Tablet2'])

    def test_use_passive_to_reach_requirement(self):
        reward_list = RewardList()
        reward_list.add_pending_reward(REWARD_WIFI)
        luke = Guest('Luke', preset_guest_stats['Luke'])
        kota = Guest('Kota', preset_guest_stats['Kota'])
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(kota)
        inventory = Inventory()
        relationship_list = RelationshipList()
        reward = determine_reward(reward_list, calculate_rd_team_stats(inventory, guest_list, relationship_list), team='RD', materials=inventory.rawMaterials)
        self.assertEqual(reward, 0)
        guest_list.send_guest_to_rd('Kota')
        guest_list.send_guest_to_rd('Luke')
        reward = determine_reward(reward_list, calculate_rd_team_stats(inventory, guest_list, relationship_list), team='RD', materials=inventory.rawMaterials)
        self.assertEqual(reward, 0)
        self.assertEqual(determine_rd_reward(reward_list, inventory, guest_list, relationship_list), 0)
        self.assertEqual(calculate_rd_team_stats(inventory, guest_list, relationship_list), Stats(preset_guest_stats['Luke']) + Stats(preset_guest_stats['Kota']))

        # Kota and Luke have 3 contract, 3 tech between them, they're short two points
        inventory.increase_passive_bonus('Tech', 2)
        inventory.increase_passive_bonus('Contract', 2)
        reward = determine_reward(reward_list, calculate_rd_team_stats(inventory, guest_list, relationship_list), team='RD', materials=inventory.rawMaterials)
        self.assertEqual(reward.name, 'WiFi')
        self.assertEqual(determine_rd_reward(reward_list, inventory, guest_list, relationship_list).name, 'WiFi')

        # If I remove either from the team then the reward becomes unobtainable
        guest_list.free_guest('Kota')
        reward = determine_reward(reward_list, calculate_rd_team_stats(inventory, guest_list, relationship_list), team='RD', materials=inventory.rawMaterials)
        self.assertEqual(reward, 0)
        self.assertEqual(determine_rd_reward(reward_list, inventory, guest_list, relationship_list), 0)

