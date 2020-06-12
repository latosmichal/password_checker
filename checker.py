import requests
import hashlib
import sys


def get_passwords_from_file(path):
    try:
        with open(path) as passwd_file:
            passwords = passwd_file.readlines()
            passes = []
            for passwd in passwords:
                passes.append(passwd.rstrip())       
            print(passes)
            return passes
    except:
        print('Error with fetching a file! Try correcting your path.')


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again.')
    return response


def pwned_api_check(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1pass[:5],sha1pass[5:]
    res = request_api_data(first5)
    return how_many_pass_leaks(res, tail)


def how_many_pass_leaks(hashes, pass_hash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, leaks in hashes:
        if pass_hash == h:
            return leaks
    return 0


def main(password_file):
    passwords = get_passwords_from_file(password_file)
    for password in passwords:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... Consider changing your password ;) For REAL!')
        else:
            print(f'{password} was not found ;)')
        

if __name__ == "__main__":
    #main(sys.argv[1])
    main('passwd.txt')
