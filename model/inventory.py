from model.stats import Stats


class Inventory:
    def __init__(self):
        self.accumulated_stats = {'RD': Stats(), 'Exploration': Stats()}
        self.passive_bonus = Stats()
        self.items = []
        self.rawMaterials = 0
        self.files = FileList()
        self.fragments = []

    def add_item(self, item_name):
        if item_name not in self.items:
            self.items.append(item_name)

    def remove_item(self, item_name):
        if item_name in self.items:
            self.items.remove(item_name)

    def increase_passive_bonus(self, stat, amount=1):
        self.passive_bonus.increase_stat(stat, amount)

    def get_passive_bonus(self):
        return self.passive_bonus

    def spend_stats(self, stats, team):
        if self.accumulated_stats[team].meets(stats):
            self.accumulated_stats[team] -= stats

    def accumulate_stats(self, stats, team):
        self.accumulated_stats[team] += stats

    def add_file(self, file_type, file):
        self.files.add_file(file_type, file)


class FileList:
    def __init__(self):
        self.files = {'Memento': [],
                      'Artifact': [],
                      'Profile': [],
                      'Tech': [],
                      'Contract': []}

    def add_file(self, file_type, file):
        # just in case file_type has an s in the end or is missing caps
        file_type = file_type.lower().rstrip('s').capitalize()
        if file not in self.files[file_type] and 'id' in file.keys() and 'name' in file.keys():
            self.files[file_type].append(file)

    def get_files(self, file_type):
        file_type = file_type.lower().rstrip('s').capitalize()
        return self.files[file_type]

    def list_file_types(self):
        file_type_list = []
        for file_type in self.files.keys():
            if len(self.files[file_type]) > 0:
                file_type_list.append(file_type)
        return file_type_list
