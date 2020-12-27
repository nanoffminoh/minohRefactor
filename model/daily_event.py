class DailyEvent:
    def __init__(self, event_name, expires=False, event_days=0, event_label=None, guest=None):
        self.name = event_name
        self.label = event_label
        self.expires = expires
        self.remaining_days = event_days
        self.guest_subject = guest
        self.complete = False

    def advance(self, days=1):
        if self.remaining_days > 0:
            self.remaining_days -= days
        if self.remaining_days <= 0:
            self.remaining_days = 0
            if self.expires:
                self.complete = True


class DailyEventList:
    def __init__(self):
        self.event_list = []

    def __len__(self):
        return len(self.event_list)

    def completed_events(self):
        new_list = []
        for event in self.event_list:
            if event.complete:
                new_list.append(event)
        return new_list

    def add_event(self, event):
        self.event_list.append(event)

    def advance_days(self, days=1):
        for event in self.event_list:
            event.advance(days)

    def clear_completed_events(self):
        self.event_list = [event for event in self.event_list if not event.complete]

    def get_daily_event_label(self):
        label = 'none'
        for event in self.event_list:
            if not event.complete:
                # Check every incomplete event. If it meets the completion criteria, break the loop, complete and remove
                # it, and return its label, signalling the game to jump to the scene that happens if the event is done.
                if event.name == 'LukeCompleteRoute':
                    if False:  # replace with a check to see if luke's route is clear
                        event.complete = True
                        label = event.label
                        break
        self.clear_completed_events()
        return label
