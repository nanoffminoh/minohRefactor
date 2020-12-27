import unittest
from model.guest import Guest, GuestList
from model.couple import Relationship, RelationshipList
from model.stats import Stats
from presets import preset_guest_stats, preset_guest_route_length, preset_couple_stats,\
    preset_maximum_relationship_length

KOTA_STATS = preset_guest_stats['Kota']
LUKE_STATS = preset_guest_stats['Luke']
MAX_ROUTES = preset_guest_route_length


class CouplesTest(unittest.TestCase):

    def test_relationship_member_requirement(self):
        relationship = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black'])
        self.assertTrue(relationship.can_start(['Luke', 'Black']))
        self.assertTrue(relationship.can_start('Luke,Black'))
        self.assertTrue(relationship.can_start(['Black', 'Luke']))
        self.assertTrue(relationship.can_start(['Black', 'Luke', 'Kota']))
        self.assertFalse(relationship.can_start(['Kota', 'Black']))
        self.assertFalse(relationship.can_start(['Black']))
        self.assertFalse(relationship.can_start('Black'))
        self.assertFalse(relationship.can_start('Black,Kota'))

    def test_start_and_complete_relationship(self):
        relationship = Relationship(['Luke', 'Black'], stats=preset_couple_stats['Luke,Black']['stats'])
        self.assertEqual(relationship.status, 'unset')
        relationship.advance()
        self.assertEqual(relationship.status, 'started')
        relationship.advance(max_progress=preset_maximum_relationship_length['Luke,Black'])
        self.assertEqual(relationship.status, 'complete')

    def test_stat_bonus_creating_properly(self):
        relationship = Relationship(['Luke', 'Black'], stats=preset_couple_stats['Luke,Black']['stats'])
        self.assertEqual(relationship.stat_bonus.get_value('Contract'),
                         Stats(preset_couple_stats['Luke,Black']).get_value('Contract'))

    def test_returns_bonus(self):
        length = preset_maximum_relationship_length['Luke,Black']
        relationship = Relationship(['Luke', 'Black'], stats=preset_couple_stats['Luke,Black']['stats'])
        self.assertEqual(relationship.status, 'unset')
        self.assertEqual(relationship.stat_bonus.get_value('Tech'), 1)
        self.assertEqual(relationship.get_bonus_stats().get_value('Tech'), 0)
        relationship.advance(amount=length, max_progress=length)
        self.assertEqual(relationship.status, 'complete')
        self.assertEqual(relationship.get_bonus_stats().get_value('Tech'), 1)


class CouplesListTest(unittest.TestCase):

    def test_create_relationship_list(self):
        luke_black = Relationship(['Luke', 'Black'], stats=preset_couple_stats['Luke,Black']['stats'])
        kota_onsen = Relationship(['Kota', 'Onsen'], stats=preset_couple_stats['Kota,Onsen']['stats'])
        self.assertEqual(luke_black.status, 'unset')
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        self.assertEqual(rel_list.get_relationship_status('Luke,Black'), 'unset')
        self.assertEqual(rel_list.get_relationship_status('Kota,Onsen'), 'missing')
        rel_list.add_relationship(kota_onsen)
        self.assertEqual(rel_list.get_relationship_status('Luke,Black'), 'unset')
        self.assertEqual(rel_list.get_relationship_status('Kota,Onsen'), 'unset')

    def test_start_relationship_modifies_guest_list(self):
        luke = Guest('Luke', preset_guest_stats['Luke'])
        black = Guest('Black', preset_guest_stats['Black'])
        luke_black = Relationship(['Luke', 'Black'], stats=preset_couple_stats['Luke,Black']['stats'])
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(black)
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        self.assertEqual(rel_list.get_relationship_progress('Luke'), 0)
        self.assertEqual(guest_list.guests['Luke'].romance_status, 'single')
        rel_list.advance_relationship(['Luke', 'Black'], guest_list=guest_list)
        self.assertEqual(rel_list.get_relationship_progress('Luke'), 1)
        self.assertEqual(guest_list.guests['Luke'].romance_status, 'dating')
        self.assertEqual(guest_list.guests['Luke'].romance_partner, 'Black')
        self.assertEqual(rel_list.get_relationship_status('Luke,Black'), 'started')

    def test_start_relationship_in_list(self):
        luke_black = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black']['stats'])
        kota_onsen = Relationship(['Kota', 'Onsen'], preset_couple_stats['Kota,Onsen']['stats'])
        rel_list = RelationshipList()
        self.assertEqual(len(rel_list.get_relationships_that_can_start('Luke,Black,Onsen,Kota')), 0)
        rel_list.add_relationship(luke_black)
        rel_list.add_relationship(kota_onsen)
        self.assertEqual(rel_list.get_relationship_status('Luke,Black'), 'unset')
        self.assertEqual(len(rel_list.get_relationships_that_can_start('Luke,Black,Onsen,Kota')), 2)
        self.assertEqual(rel_list.get_relationship_status('Onsen,Kota'), 'unset')
        rel_list.advance_relationship('Luke,Onsen')
        self.assertEqual(len(rel_list.get_relationships_that_can_start('Luke,Black,Onsen,Kota')), 2)
        rel_list.advance_relationship('Kota,Onsen')
        self.assertEqual(rel_list.get_relationship_status('Onsen,Kota'), 'started')
        self.assertEqual(len(rel_list.get_relationships_that_can_start('Luke,Black,Onsen,Kota')), 1)

    def test_get_team_relationship_bonus(self):
        dict_copy = preset_couple_stats['Luke,Black']
        route_max = preset_maximum_relationship_length['Luke,Black']
        luke_black = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black']['stats'])
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        self.assertEqual(rel_list.sum_bonus().get_value('Tech'), 0)
        self.assertEqual(rel_list.sum_bonus().get_value('Tech'), 0)
        self.assertEqual(rel_list.get_relationships_with_guests('Luke,Black,Kota,Onsen').sum_bonus().get_value('Tech'), 0)
        self.assertEqual(rel_list.get_relationship_status('Luke,Black'), 'unset')

        # test again after completing the relationship
        rel_list.advance_relationship('Luke,Black', amount=route_max, max_progress=route_max)
        self.assertEqual(rel_list.get_relationship_status('Luke,Black'), 'complete')
        self.assertEqual(rel_list.relationships[0].get_bonus_stats().get_value('Tech'), 1)
        self.assertEqual(rel_list.sum_bonus(), Stats(preset_couple_stats['Luke,Black']['stats']))
        self.assertEqual(rel_list.get_relationships_with_guests('Luke,Black,Kota,Onsen').sum_bonus().get_value('Tech'),
                         preset_couple_stats['Luke,Black']['stats']['Tech'])

        # make sure dict is not being modified
        self.assertEqual(dict_copy['stats']['Tech'],  preset_couple_stats['Luke,Black']['stats']['Tech'])

    def test_get_relationship_routes(self):
        luke_black = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black']['stats'])
        kota_onsen = Relationship(['Kota', 'Onsen'], preset_couple_stats['Kota,Onsen']['stats'])
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        rel_list.add_relationship(kota_onsen)
        current_maxes = {'Luke,Black': 2, 'Kota,Onsen': 2}
        available_guests = ['Luke', 'Black', 'Kota', 'Onsen']
        choices, couples = rel_list.get_available_couple_routes(available_guests, available_guests, current_maxes)
        self.assertEqual(choices, [("Luke and Black's scene #0", 'Luke_Black_0'), ("Kota and Onsen's scene #0", 'Kota_Onsen_0')])
        self.assertEqual(couples, [('Luke', 'Black'), ('Kota', 'Onsen')])

    def test_cant_meet_guest_requirements(self):
        luke_black = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black']['stats'])
        kota_onsen = Relationship(['Kota', 'Onsen'], preset_couple_stats['Kota,Onsen']['stats'])
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        rel_list.add_relationship(kota_onsen)
        current_maxes = {'Luke,Black': 2, 'Kota,Onsen': 2}
        available_guests = ['Luke', 'Black', 'Onsen']
        choices, couples = rel_list.get_available_couple_routes(available_guests, available_guests, current_maxes)
        self.assertEqual(choices, [("Luke and Black's scene #0", 'Luke_Black_0')])
        self.assertEqual(couples, [('Luke', 'Black')])

    def test_stopped_by_current_maxes(self):
        luke_black = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black']['stats'])
        kota_onsen = Relationship(['Kota', 'Onsen'], preset_couple_stats['Kota,Onsen']['stats'])
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        rel_list.add_relationship(kota_onsen)
        rel_list.advance_relationship('Luke,Black', max_progress=3)
        current_maxes = {'Luke,Black': 1, 'Kota,Onsen': 2}
        available_guests = ['Luke', 'Black', 'Kota', 'Onsen']
        choices, couples = rel_list.get_available_couple_routes(available_guests, available_guests, current_maxes)
        self.assertEqual(choices, [("Kota and Onsen's scene #0", 'Kota_Onsen_0')])
        self.assertEqual(couples, [('Kota', 'Onsen')])

    def test_advance_relationship(self):
        luke_black = Relationship(['Luke', 'Black'], preset_couple_stats['Luke,Black']['stats'])
        kota_onsen = Relationship(['Kota', 'Onsen'], preset_couple_stats['Kota,Onsen']['stats'])
        rel_list = RelationshipList()
        rel_list.add_relationship(luke_black)
        rel_list.add_relationship(kota_onsen)
        current_maxes = {'Luke,Black': 2, 'Kota,Onsen': 2}
        available_guests = ['Luke', 'Black', 'Onsen', 'Kota']
        rel_list.advance_relationship('Kota,Onsen')
        choices, couples = rel_list.get_available_couple_routes(available_guests, available_guests, current_maxes)
        self.assertEqual(choices, [("Luke and Black's scene #0", 'Luke_Black_0'), ("Kota and Onsen's scene #1", 'Kota_Onsen_1')])
        self.assertEqual(couples, [('Luke', 'Black'), ('Kota', 'Onsen')])
        rel_list.advance_relationship('Kota,Onsen', max_progress=2)
        choices, couples = rel_list.get_available_couple_routes(available_guests, available_guests, current_maxes)
        self.assertEqual(rel_list.get_relationship_status('Kota,Onsen'), 'complete')
        self.assertEqual(choices, [("Luke and Black's scene #0", 'Luke_Black_0')])
        self.assertEqual(couples, [('Luke', 'Black')])
