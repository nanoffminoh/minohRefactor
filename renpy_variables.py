from model.guest import GuestList
from model.inventory import Inventory, FileList
from model.couple import RelationshipList
from model.reward import RewardList
from model.daily_event import DailyEventList
from model.wardrobe import Wardrobe

player_background = ""
current_chapter = ""
guests = GuestList()
inventory = Inventory()
relationships = RelationshipList()
rewards = RewardList()
daily_events = DailyEventList()
wardrobe = Wardrobe()

UI_permissions = {'ledger': False,
                  'items': False,
                  'guests': False,
                  'rd': False,
                  'exploration': False,
                  'fragments': False,
                  'files': False,
                  'file_profile': False,
                  'file_mementos': False,
                  'file_tech': False,
                  'file_contracts': False,
                  'file_artifacts': False}

# permanent variables

permanent_known_guests = []
permanent_known_fragments = []
permanent_files = FileList()
permanent_show_files = False
permanent_first_save = True
