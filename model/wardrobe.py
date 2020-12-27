from presets import preset_clothing_types, preset_default_clothes, preset_extra_clothes


class Wardrobe:
    def __init__(self):
        self.clothing = {}
        for clothing_type in preset_clothing_types:
            self.clothing[clothing_type] = {}
        self.add_articles_in_list(preset_default_clothes)

    def has_clothing(self, clothing_type, value):
        return value in self.clothing[clothing_type].keys()

    def add(self, clothing_type, value):
        if not self.has_clothing(clothing_type, value):
            filename_id = value
            if clothing_type in ['nose_ring', 'wedding_ring']:
                if value == "True":
                    filename_id = clothing_type
                else:
                    filename_id = "none"
            idle_filename = "gui/wardrobe/" + filename_id + "_idle"
            hover_filename = "gui/wardrobe/" + filename_id + "_hover"
            self.clothing[clothing_type][value] = {'idle': idle_filename, 'hover': hover_filename}

    def add_articles_in_list(self, list_of_clothes):
        for article in list_of_clothes:
            self.add(article[0], article[1])

    def fill_up(self):
        # adds every non default clothing option.
        self.add_articles_in_list(preset_extra_clothes)
