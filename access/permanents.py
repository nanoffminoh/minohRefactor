# functions that affect persistent variables

def add_file(inventory, permanent_files, file_type, file_id, file_name):
    new_file = {'id': file_id, 'name': file_name}
    inventory.add_file(file_type, new_file)
    permanent_files.add_file(file_type, new_file)


def add_guest(guest_list, permanent_guests, guest):
    guest_list.add_guest(guest)
    if guest.name in permanent_guests:
        permanent_guests.append(guest.name)
