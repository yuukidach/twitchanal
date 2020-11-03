import click
from twitchanal.save_secret.save_secret import save_id_secret

@click.group()
@click.version_option()
def cli():
    pass


@click.command()
def save_user():
    id = click.prompt('Please enter the client ID', type=str)
    secret = click.prompt('Please enter the secret key', type=str)
    save_id_secret(id, secret)


cli.add_command(save_user)


if __name__ == '__main__':
    cli()