from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):

    def __repr__(self):
        return f'{self.value}'

    def __eq__(self, o):
        return self.value == o.value


class Record:

    def __init__(self, name_in, phone: str = None):
        self.name = Name(name_in)
        self.phones = [Phone(phone) if phone else []]

    def __repr__(self):
        return f'{self.phones}'

    def adding_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.adding_phone(new_phone)

    def edit_name(self, new_name):
        self.name = Name(new_name)


class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def edit_record(self, name, old_phone, new_phone):
        local_record = self.data[name]
        local_record.edit_phone(old_phone, new_phone)

    def remove_record(self, record):
        self.data.pop(record.name.value)

    def find_record(self, name):
        error_text = f'Contact {name} is not found at AdressBook'
        return self.data[name] if name in self.data else error_text

    def show_all_book(self):
        return self.data


#CONTACTS: dict = {}
address_book = AdressBook()

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact is not found. Please try again'
        except ValueError:
            return 'Please enter your data correctly and try again'
        except IndexError:
            return 'Please check arguments'
        except TypeError:
            return 'Please enter correct data with space'
    return wrapper


@input_error
def greetings_fun():
    return 'Greeting, How can I help you?'


@input_error
def adding_fun(name, phone):
    # CONTACTS[name] = phone              #Було так
    record = Record(name, phone)        #Має стати так
    address_book.add_record(record)
    return f'Contact {name} and phone(s) {phone} was successfully added'


@input_error
def change_fun(name, old_phone, new_phone):
    #CONTACTS[name] = new_phone
    address_book.edit_record(name, old_phone, new_phone)
    return f'Contact {name} has changed phone number on {new_phone}'


@input_error
def find_fun(name):
    return f'Under the {name} contact is recorded phone {address_book.find_record(name)}'


@input_error
def show_all_fun():
    contacts = address_book.show_all_book()
    database = ''
    if contacts:
        for name, phone in contacts.items():
            database += f'|{name}   :   {phone}|\n'
        return database
    else:
        return 'Contacts database is empty'


@input_error
def goodbay_fun():
    return 'Thank you for applying our Bot-assist. Have a nice day'


def reaction(user_command, *data):
    if user_command in COMMANDS:
        return COMMANDS[user_command](*data)
    else:
        return 'Wrong command'


def data_analytic(data):
    if data == 'show all':
        user_command = 'show all'
        arguments = tuple()
        return reaction(user_command, *arguments)

    if data == 'good bye':
        user_command = 'good bye'
        arguments = tuple()
        return reaction(user_command, *arguments)

    (user_command, *arguments) = data.casefold().split()
    return reaction(user_command, *arguments)


COMMANDS = {
    'hello': greetings_fun,
    'add': adding_fun,
    'change': change_fun,
    'phone': find_fun,
    'show all': show_all_fun,
    'good bye': goodbay_fun,
    'close': goodbay_fun,
    'exit': goodbay_fun
}


def main():
    while True:
        request = input('Please type command: ')
        result = data_analytic(request)
        print(result)
        if result == 'Thank you for applying our Bot-assist. Have a nice day':
            break


if __name__ == '__main__':
    main()



