def error_handler(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return 'No user with this name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'
    return inner

def start(msg):
    return "Hello, how I can help you?"

@error_handler
def add(args):
    name, phone = args
    if name.isnumeric():
        return "Wrong format name"
    elif not phone.isnumeric():
        return "Wrong format phone"
    DATA_CONTACTS.update({name: phone})
    return f"Contact {name} with phone: {phone} added successfull"

@error_handler
def change(args):
    name, phone = args
    DATA_CONTACTS.update({name: phone})
    return f"Contact {name} with phone: {phone} changed successfull"

@error_handler
def show_name_contact(args):
    name = args[0]
    phone = DATA_CONTACTS[name]
    return f"Contact {name} with phone: {phone}"

@error_handler
def show_all_contacts(args):
    answer = "Contact list:\n"
    for name, phone in DATA_CONTACTS.items():
        answer += f"Contact {name} with phone: {phone}\n"
    return answer[:-1]

def end(msg):
    return "Good bye!"

def handler_msg(msg: str):
    msg = msg.lower()

    if msg in COMMANDS_WITHOUT_ARGS:
        return msg, COMMANDS_WITHOUT_ARGS[msg]
    
    command, *args = msg.split(' ')
    if command in COMMANDS_WITH_ARGS:
        return args, COMMANDS_WITH_ARGS[command]

    return None, None


DATA_CONTACTS = {}

COMMANDS_WITHOUT_ARGS = {
    "hello": start,
    "show all": show_all_contacts,
    "good bye": end,
    "close": end,
    "exit": end
}

COMMANDS_WITH_ARGS = {
    "add": add,
    "change": change,
    "phone": show_name_contact
}


def main():
    while True:

        msg = input('>')
        msg, func = handler_msg(msg)

        if msg == None:
            print("Unknown command")
            continue

        answer = func(msg)
        print(answer)
        if answer == "Good bye!":
            break


if __name__ == "__main__":
    main()
