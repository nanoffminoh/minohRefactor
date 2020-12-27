from model.guest import GuestList


def get_guest_team_filename(guest_list, guest_name, size='normal', asterion_fur='white'):
    # gets the filename for the guest icons for the team screen. Will show as orange if unavailable.
    status = guest_list.get_guest_status(guest_name)
    color = 'orange' if status == 'unavailable' else 'color'
    size = '/big' if size == 'big' else ''
    if guest_name == 'Asterion' and status != 'unavailable':
        asterion_fur = '_' + asterion_fur if asterion_fur in ['black', 'brown'] else ''
    else:
        asterion_fur = ''
    return "gui/inventory/icons" + size + "/char_" + guest_name + "_" + color + asterion_fur


def get_guest_inventory_filename(guest_list, guest_name, known_guests, size='normal', asterion_fur='white'):
    # gets the filename for the guest icons in the guest and ledger screens.
    # full color if the guest is checked in, orange if the guest was in previous playthroughs, black if not known.
    if guest_list.has_guest(guest_name):
        color = 'color'
    elif guest_name in known_guests:
        color = 'orange'
    else:
        color = 'black'
    size = '/big' if size == 'big' else ''
    if guest_name == 'Asterion' and color == 'color':
        asterion_fur = '_' + asterion_fur if asterion_fur in ['black', 'brown'] else ''
    else:
        asterion_fur = ''
    return "gui/inventory/icons" + size + "/char_" + guest_name + "_" + color + asterion_fur


def get_item_filename(item_name, size='normal'):
    size = '/big' if size == 'big' else ''
    return "gui/inventory/icons" + size + "/item_" + item_name


def get_fragment_filename(inventory, known_fragments, fragment_name, size='normal'):
    if fragment_name in inventory.fragments:
        color = 'color'
    elif fragment_name in known_fragments:
        color = 'orange'
    else:
        color = 'black'
    size = '/big' if size == 'big' else ''
    return "gui/inventory/icons" + size + "/frag_" + fragment_name + "_" + color


def get_guest_tooltip(guest_list, known_guests, guest_name, guest_desc):
    title = guest_name if guest_list.has_guest(guest_name) or guest_name in known_guests else '???'
    description = guest_desc if guest_list.has_guest(guest_name) else ''
    return {'title': title, 'description': description}


def sort_file_list_by_key(my_list, list_of_keys):
    copy_list = my_list.copy()
    sorted_list = []
    for key in list_of_keys:
        for element in my_list:
            if element['id'] == key:
                sorted_list.append(element)
                copy_list.remove(element)
    sorted_list = sorted_list + copy_list
    if len(sorted_list) == len(my_list):
        return sorted_list
    else:
        return my_list
