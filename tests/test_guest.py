import unittest
from model.guest import Guest, GuestList
from presets import preset_guest_stats, preset_guest_route_length

KOTA_STATS = preset_guest_stats['Kota']
LUKE_STATS = preset_guest_stats['Luke']
MAX_ROUTES = preset_guest_route_length


class GuestTest(unittest.TestCase):

    def test_create_guest(self):
        new_guest = Guest('Luke')
        self.assertEqual(new_guest.name, 'Luke')

    def test_guest_stats_initialize_not_empty(self):
        new_guest = Guest('Kota', KOTA_STATS)
        self.assertEqual(new_guest.stats.get_value('Contract'), KOTA_STATS['Contract'])

    def test_max_stats(self):
        luke = Guest('Luke', LUKE_STATS)
        self.assertTrue('Contract' not in luke.stats.top_stats())
        self.assertTrue('Fragment' in luke.stats.top_stats())
        self.assertTrue('Surveying' in luke.stats.top_stats())

        # if the guest has no stat set, all stats are on the top stats
        kota = Guest('Kota')
        self.assertEqual(len(kota.stats.top_stats()), 7)

    def test_guest_route(self):
        luke = Guest('Luke', LUKE_STATS)
        self.assertEqual(luke.route_progress, 0)
        self.assertFalse(luke.route_complete)
        luke.advance_route(1, MAX_ROUTES['Luke'])
        self.assertEqual(luke.route_progress, 1)
        self.assertFalse(luke.route_complete)
        luke.advance_route(3, MAX_ROUTES['Luke'])
        self.assertEqual(luke.route_progress, 4)
        self.assertTrue(luke.route_complete)

    def test_guest_status(self):
        luke = Guest('Luke', LUKE_STATS)
        self.assertEqual(luke.status, 'available')
        luke.set_status('RD')
        self.assertEqual(luke.status, 'RD')
        luke.disable_guest()
        self.assertEqual(luke.status, 'unavailable')

    def test_guest_advance_days_to_recover(self):
        luke = Guest('Luke', LUKE_STATS)
        luke.disable_guest(3)
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, 3)
        luke.advance_day(2)
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, 1)
        luke.advance_day()
        self.assertEqual(luke.status, 'available')
        self.assertEqual(luke.days_off, 0)

    def test_advance_day_doesnt_affect_avialiable_guest(self):
        luke = Guest('Luke', LUKE_STATS)
        self.assertEqual(luke.status, 'available')
        self.assertEqual(luke.days_off, 0)
        luke.advance_day()
        self.assertEqual(luke.status, 'available')
        self.assertEqual(luke.days_off, 0)
        luke.set_status('RD')
        luke.advance_day()
        self.assertEqual(luke.days_off, 0)

    def test_advance_day_does_not_affect_permanently_disabled_guest(self):
        luke = Guest('Luke', LUKE_STATS)
        self.assertEqual(luke.status, 'available')
        self.assertEqual(luke.days_off, 0)
        luke.disable_guest()
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, -1)
        luke.advance_day()
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, -1)

    def test_add_extra_sick_days(self):
        luke = Guest('Luke', LUKE_STATS)
        luke.disable_guest(3)
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, 3)
        luke.advance_day()
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, 2)
        luke.disable_guest(5)
        self.assertEqual(luke.status, 'unavailable')
        self.assertEqual(luke.days_off, 7)

    def test_can_date(self):
        luke = Guest('Luke', LUKE_STATS)
        self.assertFalse(luke.can_date())
        self.assertEqual(luke.route_progress, 0)
        self.assertFalse(luke.route_complete)
        luke.advance_route(MAX_ROUTES['Luke']-1, MAX_ROUTES['Luke'])
        self.assertFalse(luke.route_complete)
        luke.advance_route(1, MAX_ROUTES['Luke'])
        self.assertTrue(luke.route_complete)
        self.assertTrue(luke.can_date())
        self.assertTrue(luke.can_start_relationship())
        luke.set_status('RD')
        self.assertFalse(luke.can_date())
        self.assertFalse(luke.can_start_relationship())

    def test_guest_can_advance_route(self):
        luke = Guest('Luke', LUKE_STATS)
        current_route_max = 2
        route_max = 3
        self.assertTrue(luke.can_advance_route(current_route_max))
        luke.advance_route(1, route_max)
        self.assertTrue(luke.can_advance_route(current_route_max))
        # send to RD, won't be able to advance
        luke.set_status('RD')
        self.assertFalse(luke.can_advance_route(current_route_max))
        luke.set_status('available')
        self.assertTrue(luke.can_advance_route(current_route_max))
        # advance route to the max available in the build, won't be able to advance
        luke.advance_route(1, route_max)
        self.assertFalse(luke.can_advance_route(current_route_max))
        # raise the build's current maximum route, will be able to advance
        current_route_max = 3
        self.assertTrue(luke.can_advance_route(current_route_max))
        # luke advances and completes his route, cannot advance anymore
        luke.advance_route(1, route_max)
        self.assertFalse(luke.can_advance_route(current_route_max))


class GuestListTest(unittest.TestCase):

    def test_create_guest_list(self):
        luke = Guest('Luke', LUKE_STATS)
        guest_list = GuestList()
        self.assertFalse(guest_list.has_guest('Luke'))
        guest_list.add_guest(luke)
        self.assertTrue(guest_list.has_guest('Luke'))
        self.assertEqual(guest_list.get_guest_status('Luke'), 'available')
        self.assertEqual(guest_list.get_free_guests().names()[0], 'Luke')

    def test_move_guests_around(self):
        luke = Guest('Luke', LUKE_STATS)
        kota = Guest('Kota', KOTA_STATS)
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(kota)
        self.assertEqual(guest_list.get_guest_status('Luke'), 'available')
        self.assertEqual(guest_list.get_guest_status('Kota'), 'available')
        self.assertTrue('Luke' in guest_list.get_free_guests().names())
        guest_list.send_guest_to_rd('Luke')
        self.assertFalse('Luke' in guest_list.get_free_guests().names())
        self.assertTrue('Luke' in guest_list.get_rd_team().names())
        guest_list.send_guest_to_exploration('Kota')
        self.assertFalse('Kota' in guest_list.get_free_guests().names())
        self.assertTrue('Kota' in guest_list.get_exploration_team().names())
        guest_list.free_guest('Luke')
        self.assertTrue('Luke' in guest_list.get_free_guests().names())
        self.assertFalse('Luke' in guest_list.get_rd_team().names())

    def test_team_stat_total(self):
        luke = Guest('Luke', LUKE_STATS)
        kota = Guest('Kota', KOTA_STATS)
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(kota)
        self.assertEqual(len(guest_list.get_rd_team()), 0)
        self.assertEqual(guest_list.get_rd_team().sum_stats().get_value('Contract'), 0)
        guest_list.send_guest_to_rd('Luke')
        self.assertEqual(len(guest_list.get_rd_team()), 1)
        self.assertEqual(guest_list.get_rd_team().sum_stats().get_value('Contract'), LUKE_STATS['Contract'])
        guest_list.send_guest_to_rd('Kota')
        self.assertEqual(len(guest_list.get_rd_team()), 2)
        self.assertEqual(guest_list.get_rd_team().sum_stats().get_value('Contract'),
                         LUKE_STATS['Contract'] + KOTA_STATS['Contract'])

    def test_available_routes(self):
        luke = Guest('Luke', LUKE_STATS)
        kota = Guest('Kota', KOTA_STATS)
        current_build_max = {'Luke': 3, 'Kota': 1}
        guest_route_max = {'Luke': 3, 'Kota': 2}
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(kota)
        choices, guests = guest_list.get_available_guest_routes(current_build_max)
        self.assertEqual(choices, [("Luke's scene #0", 'Luke_0'), ("Kota's scene #0", 'Kota_0')])
        self.assertEqual(guests, ['Luke', 'Kota'])
        guest_list.send_guest_to_rd('Kota')
        choices, guests = guest_list.get_available_guest_routes(current_build_max)
        self.assertEqual(choices, [("Luke's scene #0", 'Luke_0')])
        self.assertEqual(guests, ['Luke'])
        guest_list.free_guest('Kota')
        guest_list.advance_guest_route('Luke', guest_route_max)
        choices, guests = guest_list.get_available_guest_routes(current_build_max)
        self.assertEqual(choices, [("Luke's scene #1", 'Luke_1'), ("Kota's scene #0", 'Kota_0')])
        self.assertEqual(guests, ['Luke', 'Kota'])
        self.assertEqual(guest_list.guests['Kota'].route_progress, 0)
        guest_list.advance_guest_route('Kota', guest_route_max)
        self.assertEqual(guest_list.guests['Kota'].route_progress, 1)
        choices, guests = guest_list.get_available_guest_routes(current_build_max)
        self.assertEqual(choices, [("Luke's scene #1", 'Luke_1')])
        self.assertEqual(guests, ['Luke'])
        guest_list.advance_guest_route('Luke', guest_route_max, 2)
        self.assertTrue(guest_list.guests['Luke'].route_complete)
        choices, guests = guest_list.get_available_guest_routes(current_build_max)
        self.assertEqual(choices, [])
        self.assertEqual(guests, [])

    def test_get_next_guest_scene(self):
        luke = Guest('Luke', LUKE_STATS)
        kota = Guest('Kota', KOTA_STATS)
        current_build_max = {'Luke': 3, 'Kota': 1}
        guest_route_max = {'Luke': 3, 'Kota': 2}
        guest_list = GuestList()
        guest_list.add_guest(luke)
        guest_list.add_guest(kota)
        self.assertEqual(guest_list.get_next_guest_scene('Luke'), 'Luke_0')
        self.assertEqual(guest_list.get_next_guest_scene('Kota'), 'Kota_0')
        guest_list.advance_guest_route('Luke', guest_route_max)
        self.assertEqual(guest_list.get_next_guest_scene('Luke'), 'Luke_1')
