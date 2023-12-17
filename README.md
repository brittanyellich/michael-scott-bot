# Timber Bot

The purpose of this bot is to be a space for automating some tasks in a few family discord servers, and to experiment with some different bot functionality.

For the bot's command reference, go to the [Docs](./docs/).

## Setup

### Install necessary Python tools

1. Install **Python 3.12**
2. **Recommended:** Get [pipx](https://pypa.github.io/pipx/) to manage global Python packages.
3. Install **pipenv**
   1. `pipx install pipenv`

### Environment setup

Once you've cloned the repo, run
```shell
pipenv install
```

Once that completes, initialize the DB by running this at the root of the repo:
```shell
pipenv run python cli.py db create_all
```

Finally, create a `.env` file at the root of the repo with the following contents:
```
BOT_TOKEN="<YOUR_BOT_TOKEN>"
```
Replace `<YOUR_BOT_TOKEN>` with your own test bot token. If you don't know how
to make one, follow Step 1 on [this page](https://discord.com/developers/docs/getting-started#step-1-creating-an-app).

### Running the bot

You can run the bot from your terminal using
```shell
pipenv run python main.py
```

If everything's working, you should see this appear after a few seconds:
```
Logged in as
Your Bot Name
12345678900982345
------
```

Except it should show the name of your bot and its ID.

---

## Important packages to know about

### nextcord ([Docs](https://docs.nextcord.dev/en/stable/index.html))

Nextcord is the Python SDK for Discord that the bot uses. It's big and supports
all (as far as I know anyway) of Discord's features.

Its [commands framework](https://docs.nextcord.dev/en/stable/ext/commands/index.html) is
important to be familiar with, as well as this primer on [Slash Commands](https://docs.nextcord.dev/en/stable/interactions.html).

### sqla-wrapper ([Docs](https://sqla-wrapper.scaletti.dev/))

I use sqla-wrapper for most of my personal Python projects that need data persistence,
since working with SQLAlchemy and Alembic directly is kind of a pain, lol.

---

## Quick primer on how the code is organized

### Entry point

The entry point for the bot is `main.py`. All this does right now is call the `run`
function in `bot/app.py`, which is where the bot configuration/instantiation
lives.

### Cogs

The main way nextcord lets you organize groups of commands is via [Cogs](https://docs.nextcord.dev/en/stable/ext/commands/cogs.html).

### DB

Models are configured in `db/model`. Whenever you make a new model, if you want
that to be picked up by the `create_all` CLI function, you need to import it in
`db/__init__.py`.

---

Quite a bit of this bot setup was shamelessly stolen from [Angela Lansbury 9000](https://github.com/calebdinsmore/angela-lansbury-9000), which I'm including a link to as a reference.