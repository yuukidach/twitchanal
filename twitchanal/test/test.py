from click.testing import CliRunner
from src.cli import *

def test_save_secret():
    runner = CliRunner()
    res = runner.invoke(save_user, ['aaa', 'bbb'])
    assert res.output is True

if __name__ == "__main__":
    test_save_secret()