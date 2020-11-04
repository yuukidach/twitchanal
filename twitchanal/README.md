# twitchanal

A command line tool to gether certain data from twitch.

## 1. Installation

``` shell
pip3 install [-e] .
```

If you want to further develop this tool, add `-e` option is a good choice.

## 2. Usage

``` shell
Usage: twitchanal [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  collect    Collect data for analysis
  save-user  Save user id and secret key in `secret.yaml`.
```

`twitchanal` now contains `save-user` and `collect` sub commands.

### 2.1. `save-user` command

In order to call twitch API, we have to pass client id and secret key to it. This tool is used to save your twitch client id and secret key in `secret.yaml` so that you have no need to input mannually next time.

**WARNING:** DO NOT upload your `secret.yaml` file to GitHub or any other public website!!!

``` shell
Usage: twitchanal save-user [OPTIONS]

  Save user id and secret key in `secret.yaml`.

Options:
  --help  Show this message and exit.
```

### 2.2 `collect` command

`collect` command is one of the most important command in this tool. It used to collect top games data and related streams data into csv / yaml files. Later, we can use these files to do data analysis.

``` shell
Usage: twitchanal collect [OPTIONS]

  Collect data for analysis

Options:
  -d, --dir TEXT                Directory to store the collected data.
  --timestamp / --no-timestamp  Whether to use timestamp as suffix for data
                                file.

  -n, --num INTEGER             Number of games to collect.
  --help                        Show this message and exit.
```
