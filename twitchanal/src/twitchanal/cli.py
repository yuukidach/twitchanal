import click
from twitchanal.save_secret.save_secret import save_id_secret
from twitchanal.datacollection.collect import collect_data


@click.group()
@click.version_option()
def cli():
    pass


@click.command()
def save_user():
    """ Save user id and secret key in `secret.yaml`.
    """
    id = click.prompt('Please enter the client ID', type=str)
    secret = click.prompt('Please enter the secret key', type=str)
    save_id_secret(id, secret)


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