from presets import preset_stat_name_list

empty_stats = dict.fromkeys(preset_stat_name_list, 0)


class Stats:
    def __init__(self, stat_dict=None):
        if stat_dict is None:
            stat_dict = empty_stats
        self.stat_dict = stat_dict.copy()
        self.fill_stat_dict()
        self.stat_dict = {stat: self.stat_dict[stat] for stat in preset_stat_name_list}

    def __add__(self, other):
        new_stats = self.stat_dict.copy()
        for key in new_stats.keys():
            new_stats[key] = new_stats[key] + other.stat_dict[key]
        return Stats(new_stats)

    def __sub__(self, other):
        new_stats = self.stat_dict.copy()
        for key in new_stats.keys():
            new_stats[key] = new_stats[key] - other.stat_dict[key]
        return Stats(new_stats)

    def __eq__(self, other):
        match = True
        for key in preset_stat_name_list:
            if self.stat_dict[key] != other.stat_dict[key]:
                match = False
                break
        return match

    def increase_stat(self, stat, amount):
        if stat in self.stat_dict.keys():
            self.stat_dict[stat] += amount

    def set_stat(self, stat, amount):
        if stat in self.stat_dict.keys():
            self.stat_dict[stat] = amount

    def get_value(self, stat):
        if stat in self.stat_dict.keys():
            return self.stat_dict[stat]

    def fill_stat_dict(self):
        for stat in preset_stat_name_list:
            if stat not in self.stat_dict:
                self.stat_dict[str(stat)] = 0

    def meets(self, other):
        meets = True
        for key in preset_stat_name_list:
            if self.stat_dict[key] < other.stat_dict[key]:
                meets = False
                break
        return meets

    def top_stats(self):
        max_keys = []
        max_value = 0
        for key in self.stat_dict:
            if max_value == self.stat_dict[key]:
                max_keys.append(key)
            elif max_value < self.stat_dict[key]:
                max_value = self.stat_dict[key]
                max_keys = [key]
        return max_keys

    def top_stat(self):
        return self.top_stats()[0]

    def sum_stat(self):
        return sum(self.stat_dict.values())

    def list_stats(self, stat_filter=preset_stat_name_list):
        my_list = []
        for key in self.stat_dict:
            if self.stat_dict[key] != 0 and str(key) in stat_filter:
                my_list.append({'stat': key, 'value': self.stat_dict[key]})
        my_list.sort(key=lambda x: x['value'], reverse=True)
        return my_list

    def filter_rd(self):
        return Stats({'Contract': self.get_value('Contract'), 'Tech': self.get_value('Tech'),
                      'Fragment': self.get_value('Fragment')})

    def filter_exploration(self):
        return Stats({'Surveying': self.get_value('Surveying'), 'Memento': self.get_value('Memento'),
                      'Danger': self.get_value('Danger'), 'Artifact': self.get_value('Artifact'),
                      'Fragment': self.get_value('Fragment')})