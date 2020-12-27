preset_stat_ids = {
    "Contract": 0,
    "Tech": 1,
    "Fragment": 2,
    "Memento": 3,
    "Artifact": 4,
    "Surveying": 5,
    "Danger": 6
}

preset_stat_name_list = ['Contract', 'Tech', 'Artifact', 'Memento', 'Danger', 'Fragment', 'Surveying']

preset_stat_descriptions = {
    "Contract": "Creates contracts that change the rules of the hotel.",
    "Tech": "Develops technological projects.",
    "Fragment": "Contributes to obtaining and using godly fragments.",
    "Memento": "Used to find mementos from Asterion's past.",
    "Artifact": "Used to find artifacts that improve your team's stats.",
    "Surveying": "Used to find raw materials while exploring.",
    "Danger": "If Danger is your team's highest stat, look out!"
}

preset_guest_ids = {
    "Asterion": 0,
    "Luke":     1,
    "Kota":     2,
    "Black":    3,
    "Onsen":    4,
    "Robert":   5,
    "P":        6,
    "Nito":     7
}

preset_guest_descriptions = {
    "Asterion": "The Hotel's Keeper and prisoner of the labyrinth.",
    "Luke": "A jingoistic, fun-loving gryphon.",
    "Kota": "A calm river spirit from Japan.",
    "Onsen": "A fiery, red dragon and Kota's brother.",
    "Nito": "A lonely spacefaring gecko mechanic.",
    "Black": "A three-headed lab experiment.",
    "Robert": "A demon lawyer on vacation.",
    "P": "A peacock detective on a quest."
}

preset_guest_stats = {
    "Asterion": {'Contract': 2,
                 'Tech': 0,
                 'Fragment': 3,
                 'Memento': 3,
                 'Artifact': 1,
                 'Surveying': 1,
                 'Danger': 4},
    "Luke": {'Contract': 1,
             'Tech': 2,
             'Fragment': 3,
             'Memento': 0,
             'Artifact': 1,
             'Surveying': 3,
             'Danger': 2},
    "Kota": {'Contract': 2,
             'Tech': 1,
             'Fragment': 2,
             'Memento': 2,
             'Artifact': 1,
             'Surveying': 0,
             'Danger': 0},
    "Onsen": {'Contract': 3,
              'Tech': 0,
              'Fragment': 2,
              'Memento': 1,
              'Artifact': 2,
              'Surveying': 1,
              'Danger': 2},
    "Black": {'Contract': 0,
              'Tech': 3,
              'Fragment': 2,
              'Memento': 0,
              'Artifact': 3,
              'Surveying': 0,
              'Danger': 2},
    "Robert": {'Contract': 4,
               'Tech': 0,
               'Fragment': 1,
               'Memento': 2,
               'Artifact': 2,
               'Surveying': 0,
               'Danger': 0},
    "Nito": {'Contract': 0,
             'Tech': 5,
             'Fragment': 0,
             'Memento': 0,
             'Artifact': 2,
             'Surveying': 2,
             'Danger': 0},
    "P": {'Contract': 0,
          'Tech': 4,
          'Fragment': 0,
          'Memento': 0,
          'Artifact': 0,
          'Surveying': 3,
          'Danger': -1}
}

preset_current_route_length = {
    "Asterion": 3,
    "Luke": 2,
    "Kota": 2,
    "Onsen": 4,
    "Nito": 1,
    "Black": 1,
    "Robert": 1,
    "P": 1
}

preset_guest_route_length = {
    "Asterion": 3,
    "Luke": 4,
    "Kota": 2,
    "Onsen": 4,
    "Nito": 1,
    "Black": 1,
    "Robert": 1,
    "P": 1
}

preset_item_descriptions = {
    "Old Deed": "An old deed given to you by an old man. Despite its age, the wax seal is recent.",
    "Wine Bottle": "A healing wine prized by Asterion.",
    "Ledger": "A book that keeps track of contracts and guests.",
    "Passports": "A set of four old passports dating back to the 1940's, all from different countries.",
    "Bundle": "A coal-like stone bundled with dried olive leaves to be used as a sacrifice."
}

preset_fragment_ids = {
    "Dionysus": 0,
    "Poseidon": 1
}

preset_fragDescDict = {
    "Dionysus": "Magical wine that heals those who drink it.",
    "Poseidon": "A pocket universe meant for Asterion."
}

preset_couple_stats = {
    'Kota,Onsen': {'stats': {'Contract': 2,
                             'Fragment': 3},
                   'enabled': True},
    'Luke,Black': {'stats': {'Tech': 1,
                             'Surveying': 1,
                             'Danger': -3},
                   'enabled': True},
    'P,Storm': {'stats': {'Memento': 2,
                          'Artifact': 2,
                          'Surveying': 2,
                          'Danger': 1},
                'enabled': False}
    }

preset_current_relationship_length = {
    'Kota,Onsen': 3,
    'Luke,Black': 2,
    'P,Storm': 2
}

preset_maximum_relationship_length = {
    'Kota,Onsen': 3,
    'Luke,Black': 2,
    'P,Storm': 2
}

preset_reward_types = {'RD': ['Tech', 'Contract'],
                       'Exploration': ['Memento', 'Artifact'],
                       'Surveying': ['Surveying']}

preset_rewards = {
    #template:
    #'reward_name': {
    #    "stats": {"Contract": 1, "Tech": 1, "Surveying": 1, "Danger": 1, "Fragment": 1, "Artifact": 1, "Memento": 1},
    #    "type": "Tech/Contract/Memento/Artifact/Surveying",
    #    "essential": True/False,
    #    "rewards": ['WiFi', 'Wine'],
    #    "material": 4,
    #    "obtainable": True/False},
    "WiFi": {
        "stats": {"Contract": 5, "Tech": 5},
        "type": "Tech",
        "essential": True},
    "Wine": {
        "stats": {"Artifact": 3, "Surveying": 3},
        "type": "Artifact",
        "essential": True},
    "Tablet1": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet2": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet3": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet4": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet5": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet6": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet7": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet8": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet9": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet10": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet11": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet12": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet13": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet14": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet15": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet16": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet17": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Tablet18": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "TypewriterScrap": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "PoemNotebook": {
        "stats": {"Memento": 3},
        "type": "Memento"},
    "RockCarving": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Agape": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "FieldWork": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "FoldedNote": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Selene": {
        "stats": {"Memento": 1},
        "type": "Memento"},
    "Build3": {
        "type": "Contract",
        "obtainable": False},
    "Diary1": {
        "stats": {"Contract": 6},
        "type": "Contract"
        }
}

preset_reward_display_name = {
    "WiFi": "Connect the hotel to the internet.",
    "Diary1": "Translate Argos' first diary.",
    "Contract1": "TEST: optional contract."
}

preset_memento_id_key = ['Tablet1', 'Tablet2', 'Tablet3', 'Tablet4', 'Tablet5', 'Tablet6', 'Tablet7', 'Tablet8',
                         'Tablet9', 'Tablet10', 'Tablet11', 'Tablet12', 'Tablet13', 'Tablet14', 'Tablet15',
                         'Tablet16', 'Tablet17', 'Tablet18']

preset_clothing_types = ["fur", "clothes", "underwear", "armwear", "headwear", "neckwear", "skin", "horns",
                         "horn_accessory", "nipple_rings", "nose_ring", "wedding_ring", "penis"]

preset_default_clothes = [["horns", "normal"], ["nose_ring", "False"], ["clothes", "nude"], ["clothes", "40s"],
                          ["clothes", "vneck"], ["horn_accessory", "none"], ["nipple_rings", "none"],
                          ["skin", "none"], ["underwear", "none"], ["underwear", "loincloth"], ["armwear", "none"],
                          ["headwear", "none"], ["neckwear", "none"], ["wedding_ring", "False"], ["penis", "normal"]]

preset_extra_clothes = [["nose_ring", "True"], ["fur", "brown"], ["fur", "black"], ["fur", "white"], ["fur", "spotted"],
                        ["fur", "red"], ["fur", "blue"], ["fur", "gold"], ["clothes", "suspenders"],
                        ["clothes", "workout"], ["clothes", "harness"], ["clothes", "toga"], ["horns", "tall"],
                        ["horns", "shaved"], ["horn_accessory", "engravings"], ["horn_accessory", "caps"],
                        ["nipple_rings", "sapphire"], ["nipple_rings", "bone"], ["nipple_rings", "studs"],
                        ["nipple_rings", "bignips"], ["skin", "labyrinth"], ["skin", "labrys"], ["skin", "birthmark"],
                        ["skin", "taurus"], ["underwear", "briefs"], ["underwear", "gymshorts_blue"],
                        ["underwear", "gymshorts_red"], ["underwear", "jockstrap_black"], ["underwear", "jockstrap_white"],
                        ["underwear", "loincloth"], ["underwear", "jeans"], ["armwear", "laurel"], ["armwear", "wristband"],
                        ["armwear", "leatherband"], ["armwear", "leathergloves"], ["armwear", "shackles"],
                        ["headwear", "bangs"], ["headwear", "glasses"], ["headwear", "sunglasses"], ["headwear", "eartag"],
                        ["headwear", "earrings"], ["neckwear", "collar"], ["neckwear", "medallion"], ["neckwear", "neckerchief"],
                        ["neckwear", "cowbell"], ["neckwear", "padlock"], ["neckwear", "necklace"]]
