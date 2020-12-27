import unittest
from presets import preset_guest_stats
from model.daily_event import DailyEvent, DailyEventList

LUKE_STATS = preset_guest_stats['Luke']
ASTERION_STATS = preset_guest_stats['Asterion']


class DailyEventTest(unittest.TestCase):

    def test_daily_event_default_creation(self):
        new_event = DailyEvent('test')
        self.assertEqual(new_event.name, 'test')
        self.assertEqual(new_event.complete, False)
        self.assertEqual(new_event.expires, False)
        self.assertEqual(new_event.label, None)
        self.assertEqual(new_event.guest_subject, None)
        self.assertEqual(new_event.remaining_days, 0)

    def test_advance_daily_event_with_no_pending_days(self):
        new_event = DailyEvent('test')
        new_event.advance()
        self.assertEqual(new_event.complete, False)
        self.assertEqual(new_event.remaining_days, 0)

    def test_advance_and_complete_daily_event(self):
        new_event = DailyEvent('test', expires=True, event_days=3)
        self.assertEqual(new_event.remaining_days, 3)
        self.assertEqual(new_event.complete, False)
        self.assertEqual(new_event.expires, True)
        new_event.advance()
        self.assertEqual(new_event.remaining_days, 2)
        self.assertEqual(new_event.complete, False)
        new_event.advance(2)
        self.assertEqual(new_event.remaining_days, 0)
        self.assertEqual(new_event.complete, True)

    def test_go_over_day_limit(self):
        new_event = DailyEvent('test', expires=True, event_days=3)
        new_event.advance(5)
        self.assertEqual(new_event.remaining_days, 0)
        self.assertEqual(new_event.complete, True)


class DailyEventListTest(unittest.TestCase):

    def test_create_event_list(self):
        event_list = DailyEventList()
        self.assertEqual(event_list.event_list, [])
        self.assertEqual(event_list.completed_events(), [])

    def test_add_events(self):
        event_list = DailyEventList()
        event1 = DailyEvent('test1')
        event2 = DailyEvent('test2', expires=True, event_days=1)
        event2.advance()
        self.assertEqual(event2.complete, True)
        event_list.add_event(event1)
        self.assertEqual(len(event_list), 1)
        self.assertEqual(len(event_list.completed_events()), 0)
        event_list.add_event(event2)
        self.assertEqual(len(event_list), 2)
        self.assertEqual(len(event_list.completed_events()), 1)

    def test_advance_days(self):
        event_list = DailyEventList()
        event1 = DailyEvent('test1')
        event2 = DailyEvent('test2', expires=True, event_days=4)
        event3 = DailyEvent('test3', expires=True, event_days=1)
        event_list.add_event(event1)
        event_list.add_event(event2)
        event_list.add_event(event3)
        self.assertEqual(len(event_list.completed_events()), 0)
        event_list.advance_days()
        self.assertEqual(len(event_list.completed_events()), 1)
        self.assertEqual(event_list.completed_events()[0].name, 'test3')
        event_list.advance_days(4)
        self.assertEqual(len(event_list.completed_events()), 2)

    def test_clear_completed_events(self):
        event_list = DailyEventList()
        event1 = DailyEvent('test1', expires=True, event_days=4)
        event2 = DailyEvent('test2', expires=True, event_days=1)
        event_list.add_event(event1)
        event_list.add_event(event2)
        self.assertEqual(len(event_list), 2)
        event_list.advance_days()
        event_list.clear_completed_events()
        self.assertEqual(len(event_list), 1)
        event_list.advance_days(6)
        event_list.clear_completed_events()
        self.assertEqual(len(event_list), 0)
