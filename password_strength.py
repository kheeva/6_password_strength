#!/usr/bin/env python
import sys
import getpass


def load_bad_passwords(file_path):
    with open(file_path, 'r', encoding='utf8') as text_file:
        text_data = text_file.read()
    return text_data


def get_user_info(user_input):
    return user_input.replace(' ', '').isalnum() and user_input or (
        get_user_info(input('Wrong format. Use letters and digits.')))


def compare_passwords(password):
    return password == getpass.getpass('Confirm password: ')


def get_user_password(password):
    return compare_passwords(password) and password or get_user_password(
        getpass.getpass('The passwords mismatch. Try again: '))


def make_user_data_dict(username, company_name, password):
    return {
        'username': username,
        'company_name': company_name,
        'password': password
    }


def has_upper_and_lower_cases(password):
    return not password.islower() and not password.isupper() and (
        not password.isdigit())


def has_alpha_and_digit(password):
    return sum([symbol.isdigit() for symbol in password]) != 0 and sum(
        [symbol.isalpha() for symbol in password]) != 0


def has_specials(password):
    return not password.isalnum()


def rate_password_length(password):
    password_length = len(password)
    password_rate = 0
    if password_length > 20:
        password_rate += 4
    elif password_length > 12:
        password_rate += 3
    elif password_length > 8:
        password_rate += 2
    elif password_length > 6:
        password_rate += 1
    return password_rate


def has_not_personal_info(user_data):
    password = user_data['password'].lower()
    return user_data['username'].lower() not in password and (
        user_data['company_name'].lower() not in password)


def is_not_date_or_phone(password):
    password = password.replace('-', '').replace('.', '')
    return not (password.isdigit() and len(password) in [7, 8, 10])


def get_password_strength(user_data, password_blacklist):
    password_strength = 1
    password_length_rate = rate_password_length(user_data['password'])

    if user_data['password'] not in password_blacklist and (
        is_not_date_or_phone(user_data['password'])) and (
            has_not_personal_info(user_data)) and (
            password_length_rate != 0):
        password_strength += 1
    else:
        return 1

    password_strength += sum([
        has_upper_and_lower_cases(user_data['password']),
        has_alpha_and_digit(user_data['password']),
        has_specials(user_data['password'])])

    # If a password pass all of the tests, we increase his rate by 1
    if password_strength == 5:
        password_strength += 1

    password_strength += password_length_rate

    return password_strength


def main():
    passwords_blacklist = []

    if len(sys.argv) == 2:
        try:
            passwords_blacklist = load_bad_passwords(sys.argv[1]).splitlines()
        except FileNotFoundError as error:
            print(error, '\nWorking without a blacklist file..')

    user_data = make_user_data_dict(
                    get_user_info(input('Input username: ')),
                    get_user_info(input('Input the name of your company: ')),
                    get_user_password(getpass.getpass('Input your password: ')))

    print('\nYour password scored {} points out of 10.'.format(
        get_password_strength(user_data, passwords_blacklist)))


if __name__ == '__main__':
    main()
