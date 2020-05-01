# Reverse Shell Helper

A script to help you automate reverse shell tasks. It can run a script as soon
as the connection happens or add a key to the `authorized_keys` file.

It uses [pwntools](https://github.com/Gallopsled/pwntools) to handle the reverse
shell.

## Example usage
I usually use it to run
[linpeas](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite)
for enumeration and add a public key so that I can later on use SSH:
```
$ ./rsh.py -s linpeas.sh -k id_rsa.pub
```

## Help
```
usage: rsh.py [-h] [-i HOST] [-p PORT] [-s SCRIPT] [-k KEY]

Reverse shell helper

optional arguments:
  -h, --help  show this help message and exit
  -i HOST     The IP to listen on
  -p PORT     The port to listen on
  -s SCRIPT   A script to execute
  -k KEY      Public key to add to authorized file
```
