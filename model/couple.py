from model.stats import Stats


class Relationship:
    def __init__(self, members, stats=None, enabled=True):
        self.members = members
        if stats is None:
            self.stat_bonus = Stats()
        else:
            self.stat_bonus = Stats(stats)
        self.enabled = enabled
        self.status = "unset"
        self.progress = 0

    def can_start(self, guest_list):
        return self.meets_member_requirement(guest_list) and self.status == 'unset'

    def can_advance(self, guest_list, current_max=None):
        max_check = True if current_max is None else self.progress < current_max
        return self.meets_member_requirement(guest_list) and self.status in ['started', 'unset'] and max_check

    def meets_member_requirement(self, guest_list):
        meets = True
        for member in self.members:
            if member not in guest_list:
                meets = False
                break
        return meets

    def advance(self, amount=1, max_progress=None, guest_list=None):
        if self.status == "unset":
            if guest_list is not None:
                guest_list.start_relationship(self.members)
            self.status = "started"
        self.progress += amount
        if max_progress and self.progress >= max_progress:
            self.progress = max_progress
            self.status = "complete"
            if guest_list is not None:
                guest_list.complete_relationship(self.members)

    def get_bonus_stats(self):
        if self.status == "complete":
            return self.stat_bonus
        else:
            return Stats()


class RelationshipList:
    def __init__(self):
        self.relationships = []

    def __len__(self):
        return len(self.relationships)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    def get_relationships_with_guests(self, guest_list):
        new_list = RelationshipList()
        for relationship in self.relationships:
            if relationship.meets_member_requirement(guest_list):
                new_list.add_relationship(relationship)
        return new_list

    def get_relationships_that_can_start(self, guest_list):
        new_list = RelationshipList()
        for relationship in self.relationships:
            if relationship.can_start(guest_list):
                new_list.add_relationship(relationship)
        return new_list

    def get_relationships_that_can_advance(self, guest_list):
        new_list = RelationshipList()
        for relationship in self.relationships:
            if relationship.can_advance(guest_list):
                new_list.add_relationship(relationship)
        return new_list

    def get_relationship_status(self, members):
        for relationship in self.relationships:
            if relationship.meets_member_requirement(members):
                return relationship.status
        return "missing"

    def get_relationship_progress(self, guest_name):
        for relationship in self.relationships:
            if guest_name in relationship.members and relationship.status != 'unset':
                return relationship.progress
        return 0

    def get_bonus_stats_for_relationship(self, members):
        for relationship in self.relationships:
            if relationship.meets_member_requirement(members):
                return relationship.stat_bonus
        return "missing"

    def advance_relationship(self, guest_names, amount=1, max_progress=None, guest_list=None):
        for relationship in self.relationships:
            if relationship.can_advance(guest_names) or relationship.can_start(guest_names):
                relationship.advance(amount, max_progress, guest_list)
                break

    def sum_bonus(self):
        bonus = Stats()
        for relationship in self.relationships:
            bonus += relationship.get_bonus_stats()
        return bonus

    def get_available_couple_routes(self, single_guests, available_guests, current_maxes):
        couple_list = []
        choices_list = []
        for relationship in self.relationships:
            guest1 = relationship.members[0]
            guest2 = relationship.members[1]
            if relationship.can_advance(available_guests, current_maxes[guest1 + ',' + guest2]) or relationship.can_start(single_guests):
                scene_number = relationship.progress
                choice = guest1 + "_" + guest2 + "_" + str(scene_number)
                # convert the route code into tuple for the renpy menu
                choice = (guest1 + " and " + guest2 + "'s scene #" + str(scene_number), choice)
                choices_list.append(choice)
                couple_list.append((guest1, guest2))
        return choices_list, couple_list
