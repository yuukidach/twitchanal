import click
from twitchanal.secret.secret import save_id_secret
from twitchanal.collect.save import collect_data


@click.group()
@click.version_option()
def cli():
    pass


@click.command()
@click.option('--dir', '-d', default='./',
              help='Directory to store the secret.')
def save_user(dir):
    """ Save user id and secret key in `secret.yaml`.
    """
    id = click.prompt('Please enter the client ID', type=str)
    secret = click.prompt('Please enter the secret key', type=str)
    save_id_secret(id, secret, dir)


@click.command()
@click.option('--dir', '-d', default='./dataset',
              help='Directory to store the collected data.')
@click.option('--timestamp/--no-timestamp', default=True,
              help='Whether to use timestamp as suffix for data file.')
@click.option('--num', '-n', default=251,
              help='Number of games to collect.')
def collect(dir: str, timestamp: bool, num: int):
    """ Collect data for analysis
    """
    collect_data(dir, timestamp, num)


cli.add_command(save_user)
cli.add_command(collect)

if __name__ == '__main__':
    cli()