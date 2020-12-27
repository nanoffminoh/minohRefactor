from presets import preset_rewards
from access.loader import load_reward

MAXED_STATS = {'Contract': 99,
               'Tech': 99,
               'Fragment': 99,
               'Memento': 99,
               'Artifact': 99,
               'Surveying': 99,
               'Danger': 99}

MOCK_REWARD_WIFI = {'name': 'WiFi',
                    'type': 'Tech',
                    'stats':  {'Contract': 5,
                               'Tech': 5},
                    'materials': 0,
                    'rewards': []
                    }

MOCK_REWARD_SATELLITE = {'name': 'Satellite',
                         'type': 'Tech',
                         'stats':  {'Tech': 5},
                         'materials': 0,
                         'rewards': ['WiFi']
                         }

REWARD_WINE = load_reward('Wine', preset_rewards['Wine'])
REWARD_TABLET1 = load_reward('Tablet1', preset_rewards['Tablet1'])
REWARD_TABLET2 = load_reward('Tablet2', preset_rewards['Tablet2'])
REWARD_WIFI = load_reward('WiFi', preset_rewards['WiFi'])
