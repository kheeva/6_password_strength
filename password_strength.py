#!/usr/bin/env python
import sys
import getpass


def load_bad_passwords(file_path):
    with open(file_path, 'rb') as text_file:
        text_data = text_file.read().decode('utf-8')
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
    return sum([word.isdigit() for word in password]) != 0 and sum(
        [word.isalpha() for word in password]) != 0


def has_specials(password):
    return not password.isalnum()


def has_more_than_8_symbols(password):
    return len(password) > 8


def has_more_than_12_symbols(password):
    return len(password) > 10


def has_more_than_20_symbols(password):
    return len(password) > 20


def is_not_blacklisted_password(password):
    try:
        loaded_bad_passwords = load_bad_passwords(sys.argv[1])
    except FileNotFoundError as error:
        exit(error)
    else:
        loaded_bad_passwords = loaded_bad_passwords.splitlines()
        if password in loaded_bad_passwords:
            return False
        return True


def has_not_personal_info(user_data):
    password = user_data['password'].lower()
    return user_data['username'].lower() not in password and (
        user_data['company_name'].lower() not in password)


def is_not_date_or_phone(password):
    password = password.replace('-', '').replace('.', '')
    return not (password.isdigit() and len(password) in [7, 8, 10])


def get_password_strength(user_data):
    password_strength = 1
    if len(sys.argv) == 2:
        if is_not_blacklisted_password(user_data['password']):
            password_strength += 1
        else:
            return 1

    if is_not_date_or_phone(user_data['password']):
        password_strength += 1
    else:
        return 1

    if has_not_personal_info(user_data):
        password_strength += 1
    else:
        return 1

    password_strength += sum([
        has_upper_and_lower_cases(user_data['password']),
        has_alpha_and_digit(user_data['password']),
        has_specials(user_data['password']),
        has_more_than_8_symbols(user_data['password']),
        has_more_than_12_symbols(user_data['password']),
        has_more_than_20_symbols(user_data['password'])])

    return password_strength


def main():
    user_data = make_user_data_dict(
                    get_user_info(input('Input username: ')),
                    get_user_info(input('Input the name of your company: ')),
                    get_user_password(getpass.getpass('Input your password: ')))

    print('\nYour password scored {} points out of 10.'.format(
        get_password_strength(user_data)))


if __name__ == '__main__':
    main()
