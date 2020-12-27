import unittest
from access.ui import get_guest_team_filename, get_guest_inventory_filename, get_item_filename, get_guest_tooltip, \
    sort_file_list_by_key, get_fragment_filename
from presets import preset_guest_stats, preset_guest_descriptions
from model.guest import GuestList, Guest
from model.inventory import Inventory

LUKE_STATS = preset_guest_stats['Luke']
ASTERION_STATS = preset_guest_stats['Asterion']


class UITest(unittest.TestCase):

    def test_get_luke_team_filename(self):
        luke = Guest('Luke', LUKE_STATS)
        guest_list = GuestList()
        guest_list.add_guest(luke)
        self.assertEqual(guest_list.get_guest_status('Luke'), 'available')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke'), 'gui/inventory/icons/char_Luke_color')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke', size='big'),
                         'gui/inventory/icons/big/char_Luke_color')

    def test_orange_team_filename_if_unavailable(self):
        luke = Guest('Luke', LUKE_STATS)
        guest_list = GuestList()
        guest_list.add_guest(luke)
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke'), 'gui/inventory/icons/char_Luke_color')
        guest_list.send_guest_to_exploration('Luke')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke'), 'gui/inventory/icons/char_Luke_color')
        guest_list.disable_guest('Luke')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke'), 'gui/inventory/icons/char_Luke_orange')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke', size='big'),
                         'gui/inventory/icons/big/char_Luke_orange')

    def test_asterion_team_filename_matches_fur_color(self):
        asterion = Guest('Asterion', ASTERION_STATS)
        luke = Guest('Luke', LUKE_STATS)
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(asterion)
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Asterion'), 'gui/inventory/icons/char_Asterion_color')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Asterion', asterion_fur='white'), 'gui/inventory/icons/char_Asterion_color')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Asterion', asterion_fur='brown'), 'gui/inventory/icons/char_Asterion_color_brown')
        # check if adding asterion_fur affects luke's filename
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke'), 'gui/inventory/icons/char_Luke_color')
        self.assertEqual(get_guest_team_filename(guest_list, guest_name='Luke', asterion_fur='brown'), 'gui/inventory/icons/char_Luke_color')

    def test_inventory_filename(self):
        guest_list = GuestList()
        luke = Guest('Luke', LUKE_STATS)
        known_guests = []
        # luke is not known
        self.assertEqual(get_guest_inventory_filename(guest_list, guest_name='Luke', known_guests=known_guests),
                         'gui/inventory/icons/char_Luke_black')
        # luke is known from another playthrough but not currently checked in
        known_guests.append('Luke')
        self.assertEqual(get_guest_inventory_filename(guest_list, guest_name='Luke', known_guests=known_guests),
                         'gui/inventory/icons/char_Luke_orange')
        # luke is added to the current playthrough's guest list
        guest_list.add_guest(luke)
        self.assertEqual(get_guest_inventory_filename(guest_list, guest_name='Luke', known_guests=known_guests),
                         'gui/inventory/icons/char_Luke_color')

    def test_item_filename(self):
        self.assertEqual(get_item_filename('Wine'), 'gui/inventory/icons/item_Wine')
        self.assertEqual(get_item_filename('Wine', size='big'), 'gui/inventory/icons/big/item_Wine')

    def test_fragment_filename(self):
        inventory = Inventory()
        known_fragments = []
        self.assertEqual(get_fragment_filename(inventory, known_fragments, 'Poseidon'),
                         'gui/inventory/icons/frag_Poseidon_black')
        known_fragments.append('Poseidon')
        self.assertEqual(get_fragment_filename(inventory, known_fragments, 'Poseidon'),
                         'gui/inventory/icons/frag_Poseidon_orange')
        inventory.fragments.append('Poseidon')
        self.assertEqual(get_fragment_filename(inventory, known_fragments, 'Poseidon'),
                         'gui/inventory/icons/frag_Poseidon_color')

    def test_guest_tooltip(self):
        guest_list = GuestList()
        luke = Guest('Luke', LUKE_STATS)
        known_guests = []
        # luke is not known
        self.assertEqual(get_guest_tooltip(guest_list, known_guests=known_guests, guest_name='Luke', guest_desc=preset_guest_descriptions['Luke']),
                         {'title': '???', 'description': ''})
        # luke is known from another playthrough but not currently checked in
        known_guests.append('Luke')
        self.assertEqual(get_guest_tooltip(guest_list, known_guests=known_guests, guest_name='Luke', guest_desc=preset_guest_descriptions['Luke']),
                         {'title': 'Luke', 'description': ''})
        # luke is added to the current playthrough's guest list
        guest_list.add_guest(luke)
        self.assertEqual(get_guest_tooltip(guest_list, known_guests=known_guests, guest_name='Luke', guest_desc=preset_guest_descriptions['Luke']),
                         {'title': 'Luke', 'description': preset_guest_descriptions['Luke']})

    def test_sort_by_list(self):
        file1 = {'id': 'tuesday', 'value': 8989}
        file2 = {'id': 'lemon', 'value': 8989}
        file3 = {'id': 'sunday', 'value': 8989}
        file4 = {'id': 'monday', 'value': 8989}
        file5 = {'id': 'cheese', 'value': 8989}
        my_list = [file1, file2, file3, file4, file5]
        keys = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.assertEqual(sort_file_list_by_key(my_list, keys), [file4, file1, file3, file2, file5])
