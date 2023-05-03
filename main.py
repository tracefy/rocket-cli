#!/usr/bin/env python3
import os
import json
import click
import subprocess

CONFIG_DIR = os.path.expanduser("~/.rocket")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def print_ascii_art():
    art = r"""
  _____            _        _   
 |  __ \          | |      | |  
 | |__) |___   ___| | _____| |_ 
 |  _  // _ \ / __| |/ / _ \ __|
 | | \ \ (_) | (__|   <  __/ |_ 
 |_|  \_\___/ \___|_|\_\___|\__|
                                
        By Joeri Abbo
    """
    print(art)


@click.group()
def rocket():
    pass


@click.command()
@click.option('--username', default=None, help='Username for the connection')
@click.option('--host', default=None, help='Host for the connection')
@click.option('--nickname', default=None, help='Optional nickname for the connection')
@click.option('--through-proxy', is_flag=True, help='If set, the connection will go through the proxy')
def add(username, host, nickname, through_proxy):
    print_ascii_art()
    config = read_config()

    if not username:
        if 'default_username' in config:
            use_default = click.confirm(f"Do you want to use the default username {config['default_username']}?")
            if use_default:
                username = config['default_username']
            else:
                username = click.prompt('Please enter a username')
        else:
            username = click.prompt('Please enter a username')

    if not host:
        host = click.prompt('Please enter a host')

    connection = {'username': username, 'host': host, 'nickname': nickname or host}

    if through_proxy:
        if 'proxy' in config:
            connection['through_proxy'] = True
        else:
            click.echo('No proxy found in the config. Please add a proxy using the add_proxy command.')

    config['connections'] = config.get('connections', [])
    config['connections'].append(connection)

    write_config(config)
    click.echo(f'Added connection: {connection}')


@click.command()
@click.option('--username', default=None, help='Username for the proxy')
@click.option('--host', default=None, help='Host for the proxy')
@click.option('--nickname', default=None, help='Optional nickname for the proxy')
def add_proxy(username, host, nickname):
    print_ascii_art()
    config = read_config()

    if not username:
        username = click.prompt('Please enter a username for the proxy')

    if not host:
        host = click.prompt('Please enter a host for the proxy')

    proxy = {'username': username, 'host': host, 'nickname': nickname or host}
    config['proxy'] = proxy
    write_config(config)
    click.echo(f'Added proxy: {proxy}')


@click.command()
def delete():
    print_ascii_art()
    config = read_config()
    config['connections'] = []
    write_config(config)
    click.echo('All connections deleted')


@click.command()
@click.argument('nickname', required=False)
def launch(nickname):
    print_ascii_art()
    config = read_config()

    if not config.get('connections'):
        click.echo('No connections found, please add a connection first')
        return

    if nickname:
        connection = next((c for c in config['connections'] if c.get('nickname') == nickname), None)
    else:
        connection_nicknames = [c.get('nickname') or c['host'] for c in config['connections']]
        connection_nickname = click.prompt(
            f"Please choose a connection by its nickname ({', '.join(connection_nicknames)})", type=str)
        connection = next((c for c in config['connections'] if
                           c.get('nickname') == connection_nickname or c['host'] == connection_nickname), None)

    if connection:
        if 'proxy' in connection:
            proxy = config['proxy']
            command = f"ssh -J {proxy['username']}@{proxy['host']} {connection['username']}@{connection['host']}"
        else:
            command = f"ssh {connection['username']}@{connection['host']}"

        click.echo(f'Launching: {command}')
        subprocess.Popen([command], shell=True, executable='/bin/bash')
    else:
        click.echo(f"No connection found for nickname {nickname}")


@click.command()
def install():
    print_ascii_art()
    config = read_config()
    default_username = click.prompt('Please enter the default username')
    config['default_username'] = default_username
    write_config(config)
    click.echo(f'Default username set to: {default_username}')


def read_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def write_config(config):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


rocket.add_command(add)
rocket.add_command(add_proxy)
rocket.add_command(delete)
rocket.add_command(launch)
rocket.add_command(install)

if __name__ == '__main__':
    rocket()
