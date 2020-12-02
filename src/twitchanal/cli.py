import click
import logging
import os
from twitchanal.secret.secret import save_id_secret
from twitchanal.collect.save import collect_data
from twitchanal.process.show import show


@click.group()
@click.version_option()
def cli():
    pass


@click.command()
@click.option('--dir',
              '-d',
              default='./',
              help='Directory to store the secret.')
def save_user(dir):
    """ Save user id and secret key in `secret.yaml`.
    """
    id = click.prompt('Please enter the client ID', type=str)
    secret = click.prompt('Please enter the secret key', type=str)
    save_id_secret(id, secret, dir)


@click.command()
@click.option('--dir',
              '-d',
              default='./dataset',
              help='Directory to store the collected data.')
@click.option('--timestamp/--no-timestamp',
              default=True,
              help='Whether to use timestamp as suffix for data file.')
@click.option('--num', '-n', default=251, help='Number of games to collect.')
@click.option('--stream',
              '-s',
              default=100,
              help='Number of game streams to collect.')
@click.option(
    '--extra/--no-extra',
    default=True,
    help=
    'Whether to collect extra info like `peek viewers`, `peek channels` and so on for top games.'
)
@click.option('--debug/--no-debug',
              default=False,
              help='Run in debug mode or not.')
def collect(dir: str, timestamp: bool, num: int, stream: int, extra: bool,
            debug: bool):
    """ Collect data for analysis
    """
    try:
        os.remove('twitchanal.log')
    except OSError:
        pass

    if debug:
        lv = logging.DEBUG
    else:
        lv = logging.INFO
    logging.basicConfig(filename='twitchanal.log', level=lv)
    collect_data(dir, timestamp, num, stream, extra)


@click.command()
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Run in debug mode.')
@click.option('--dir', '-d', default='dataset', help='Data directory.')
@click.option(
    '--timestamp',
    '-t',
    default=None,
    help=
    'Data timestamp. Specify which csv file to use or the program will use the latest one by default.'
)
def process(debug: bool, dir: str, timestamp: str):
    """ Process data and do visualization.
    """
    show(debug, dir, timestamp)


cli.add_command(save_user)
cli.add_command(collect)
cli.add_command(process)

if __name__ == '__main__':
    cli()