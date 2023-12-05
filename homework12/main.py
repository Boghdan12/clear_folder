from collections import UserDict
from datetime import datetime, date
import pickle
import os


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


class Field:
    
    def init(self, value):
        self.__value = None
        self.value = value
 
    @property
    def value(self):
        return self.__value
 
    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    
    def __init__(self, value):
        self.value = value


class Phone(Field):

    def __init__(self, value):
        self.__value = value
        self.value = value

    @Field.value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError

    @value.getter
    def value(self):
        return self.__value


class Birthday(Field):

    def __init__(self, value):
        self.__value = value
        self.value = value

    @Field.value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d').date()
        except:
            raise ValueError

    @value.getter
    def value(self):
        return self.__value


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)

    def add_birthday(self, value):
        self.birthday = Birthday(value) 

    def remove_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                self.phones.remove(phone)
                return True 
        return False
    
    def edit_phone(self, value_now, value_new):
        for phone in self.phones:
            if value_now == phone.value:
                phone.value = value_new
                return
        raise ValueError

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone

    def days_to_birthday(self):
        if self.birthday:
            current_date = date.today()
            year_now = current_date.year
            birthday = self.birthday.value.replace(year = year_now)
            # Calculate
            if birthday > current_date:
                return (birthday - current_date).days
            elif birthday == current_date:
                return "0"
            elif birthday < current_date:
                birthday = birthday.replace(year = year_now+1)
                return (birthday - current_date).days

    def __str__(self):
        if self.phones and self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        elif self.phones:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        elif self.birthday:
            return f"Contact name: {self.name.value}, birthday: {self.birthday.value}"


class AddressBook(UserDict):

    path_file = "save"

    def add_record(self, user_record):
        self.data.update({user_record.name.value: user_record})

    def find(self, value):
        if value in self.data:
            return self.data[value]

    def delete(self, value):
        if value in self.data:
            self.data.pop(value)
            return True
        else:
            return False
        
    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result[:-1]
                counter = 0
                result = ''
                break

    def find_users(self, str_user):
        found_users = []
        for user_name in self.data:
            record = self.data[user_name]
            if str_user in user_name:
                found_users.append(record)
            else:
                for phone in record.phones:
                    if str_user in phone.value:
                        found_users.append(record)
        # Print found users
        if found_users:
            print("List found users:")
            for found_user in found_users:
                print(f"Contact name: {found_user.name.value}, phones: {'; '.join(p.value for p in found_user.phones)}")
        else:
            print("Not found users")

    def load(self):
        if not os.path.exists(self.path_file):
            return
        with open(self.path_file, 'rb') as file:
            self.data = pickle.load(file)

    def save(self):
        with open(self.path_file, 'wb') as file:
            pickle.dump(self.data, file)


class Controller:

    def __init__(self):
        self.book = AddressBook()

    def terminal(self):
        # Load data
        self.book.load()
        while True:
            msg = input('>')
            args, func = self.handler_msg(msg)
            if func == None:
                print("Unknown command")
                continue

            answer = func(args)
            print(answer)
            if answer == "Good bye!":
                # Save data
                self.book.save()
                break

    def handler_msg(self, msg: str):

        commands_without_args = {
            "hello": self.start,
            "show all": self.show_all_contacts,
            "good bye": self.end,
            "close": self.end,
            "exit": self.end
        }
        commands_with_args = {
            "add-contact": self.add_contact,
            "show-contact": self.show_contact,
            "delete-contact": self.delete_contact,
            "add-phone": self.add_phone,
            "add-birthday": self.add_birthday,
            "days-to-birthday": self.get_to_birthday,
            "edit-phone": self.edit_phone,
            "find-phone": self.find_phone,
            "delete-phone": self.delete_phone
        }

        if msg.lower() in commands_without_args:
            return None, commands_without_args[msg]
        
        command, *args = msg.split(' ')
        if command in commands_with_args:
            return args, commands_with_args[command]

        return None, None

    def start(self, msg):
        return "Hello, how I can help you?"

    @error_handler
    def add_contact(self, args):
        user_name = args[0]
        user_record = Record(user_name)
        self.book.add_record(user_record)
        return f"Record {user_name} added"

    @error_handler
    def add_phone(self, args):
        user_name, user_phone = args
        record = self.book.data[user_name]
        record.add_phone(user_phone)
        return f"Record updated {str(record)}"
    
    @error_handler
    def edit_phone(self, args):
        user_name, old_phone, new_phone = args
        record = self.book.data[user_name]
        record.edit_phone(old_phone, new_phone)
        return f'Record updated {str(record)}'
    
    @error_handler
    def find_phone(self, args):
        user_name, phone = args
        record = self.book.data[user_name]
        found_phone = record.find_phone(phone)
        if found_phone:
            return f'Found phone {phone}'
        else:
            return f'Not found phone {phone}'
    
    @error_handler
    def delete_phone(self, args):
        user_name, phone = args
        record = self.book.data[user_name]
        answer = record.remove_phone(phone)
        if answer:
            return 'Phone deleted'
        else: 
            return 'Phone not exists'

    @error_handler
    def add_birthday(self, args):
        user_name, user_birthday = args
        record = self.book.data[user_name]
        record.add_birthday(user_birthday)
        return f"Record updated {str(record)}"
    
    @error_handler
    def get_to_birthday(self, args):
        user_name = args[0]
        record = self.book.data[user_name]
        days = record.days_to_birthday()
        return f'Days to birthday {days}'

    @error_handler
    def change(self, args):
        name, phone = args
        # DATA_CONTACTS.update({name: phone})
        return f"Contact {name} with phone: {phone} changed successfull"

    @error_handler
    def show_contact(self, args):
        user_name = args[0]
        record = self.book.data[user_name]
        return str(record)
    
    @error_handler
    def delete_contact(self, args):
        user_name = args[0]
        answer = self.book.delete(user_name)
        if answer:
            return 'Contact deleted'
        else:
            return 'Contact not exists'
    
    @error_handler
    def show_all_contacts(self, args):
        answer = "Address book:\n"
        for name, record in self.book.data.items():
            answer += str(record) + "\n"
        return answer[:-1]

    def end(self, msg):
        return "Good bye!"


if __name__ == "__main__":
    controller = Controller()
    controller.terminal()
    