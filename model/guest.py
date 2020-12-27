from model.stats import Stats
from renpy_functions import print_on_textbox


class Guest:
    def __init__(self, name, stats=None):
        self.name = name
        self.stats = Stats(stats) or Stats()
        self.status = "available"
        self.route_progress = 0
        self.route_complete = False
        self.romance_status = "single"
        self.romance_partner = "none"
        self.days_off = 0

    def advance_route(self, amount=1, max_progress=None):
        self.route_progress += amount
        if max_progress and self.route_progress >= max_progress:
            self.route_progress = max_progress
            self.route_complete = True

    def advance_day(self, days=1):
        if self.status == 'unavailable' and self.days_off > 0:
            self.days_off -= days
            if self.days_off <= 0:
                self.days_off = 0
                print_on_textbox(self.name + ' has recovered and is active again.')
                self.set_status('available')

    def set_status(self, status):
        self.status = status

    def disable_guest(self, days=-1):
        # -1 makes a guest is unavailable indefinitely
        self.set_status('unavailable')
        self.days_off += days

    def can_date(self):
        return self.route_complete and self.status == 'available' and self.romance_status != "couple"

    def can_start_relationship(self):
        return self.route_complete and self.status == 'available' and self.romance_status == "single"

    def can_advance_route(self, current_max):
        return (not self.route_complete) and (self.status == 'available') and (self.route_progress < current_max)

    def next_scene(self):
        return self.name + "_" + str(self.route_progress)


class GuestList:
    def __init__(self):
        self.guests = {}

    def __len__(self):
        return len(self.guests)

    def add_guest(self, guest):
        self.guests[guest.name] = guest

    def names(self):
        names_list = []
        for guest in self.guests.keys():
            names_list.append(guest)
        return names_list

    def has_guest(self, name):
        return name in self.guests.keys()

    def get_guest_status(self, name):
        return self.guests[name].status

    def get_guest_stats(self, name):
        return self.guests[name].stats

    # query guests
    def get_guests_with_status(self, status_list=None):
        status_list = status_list or []
        guest_list = GuestList()
        for guest in self.guests.keys():
            if self.guests[guest].status in status_list:
                guest_list.add_guest(self.guests[guest])
        return guest_list

    def get_rd_team(self):
        return self.get_guests_with_status(['RD'])

    def get_exploration_team(self):
        return self.get_guests_with_status(['Exploration'])

    def get_free_guests(self):
        return self.get_guests_with_status(['available'])

    def get_active_guests(self):
        return self.get_guests_with_status(['RD', 'Exploration', 'available'])

    def get_guests_can_date(self):
        guest_list = GuestList()
        for guest in self.guests.keys():
            if self.guests[guest].can_date():
                guest_list.add_guest(self.guests[guest])
        return guest_list

    def get_guests_can_start_relationship(self):
        guest_list = GuestList()
        for guest in self.guests.keys():
            if self.guests[guest].can_start_relationship():
                guest_list.add_guest(self.guests[guest])
        return guest_list

    # move guests around
    def set_guest_status(self, name, status):
        self.guests[name].set_status(status)

    def send_guest_to_rd(self, name):
        self.set_guest_status(name, 'RD')

    def send_guest_to_exploration(self, name):
        self.set_guest_status(name, 'Exploration')

    def free_guest(self, name):
        self.set_guest_status(name, 'available')

    def disable_guest(self, name, days=-1):
        self.guests[name].disable_guest(days)

    def sum_stats(self):
        stats = Stats()
        for guest in self.guests.keys():
            stats += self.guests[guest].stats
        return stats

    def advance_day(self, days=1):
        for guest in self.guests:
            guest.advance_day(days)

    def advance_guest_route(self, guest_name, max_progress=None, amount=1):
        self.guests[guest_name].advance_route(amount, max_progress[guest_name])

    def get_available_guest_routes(self, current_build_route_max):
        choice_list = []
        guest_list = []
        for guest_name in self.guests.keys():
            guest = self.guests[guest_name]
            if guest.can_advance_route(current_build_route_max[guest_name]):
                choice = guest_name + "_" + str(guest.route_progress)
                # convert the route code into tuple for the renpy menu
                choice = (guest_name + "'s scene #" + str(guest.route_progress), choice)
                choice_list.append(choice)
                guest_list.append(guest_name)
        return choice_list, guest_list

    def get_next_guest_scene(self, guest_name):
        return self.guests[guest_name].next_scene()

    def start_relationship(self, guest_names):
        guest1 = guest_names[0]
        guest2 = guest_names[1]
        self.guests[guest1].romance_status = 'dating'
        self.guests[guest1].romance_partner = guest2
        self.guests[guest2].romance_status = 'dating'
        self.guests[guest2].romance_partner = guest1

    def complete_relationship(self, guest_names):
        for name in guest_names:
            self.guests[name].romance_status = 'complete'
