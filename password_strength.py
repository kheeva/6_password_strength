import getpass


def get_user_info(user_input):
    return user_input.isalnum() and user_input or get_user_info(
        input('Wrong format. Use letters and digits.'))


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
    return not password.islower()


def has_alpha_and_digit(password):
    return sum([word.isdigit() for word in password]) != 0 and sum(
        [word.isalpha() for word in password]) !=0


def has_specials(password):
    return not password.isalnum()


def get_password_strength(password):
    pass


def main():
    user_data = make_user_data_dict(
                    get_user_info(input('Input username: ')),
                    get_user_info(input('Input the name of your company: ')),
                    get_user_password(getpass.getpass('Input your password: ')))
    print(user_data)


if __name__ == '__main__':
    main()
