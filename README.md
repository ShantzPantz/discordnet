# DiscordNet

Discord net is a collection of bot plugins and services that interact with a Discord Server.

## Getting Started

```bash
git clone this respository
mv discordnet/config.py.template discordnet/config.py
# edit config.py to include your Discord API key and any additional API keys
```

## Requirements

- Python 3.4+

## Python Setup (Conda)

- Install Anaconda or Miniconda [Here](https://conda.io/miniconda.html)
- Add conda to your System PATH

### Verify Conda Install

Verify that the conda install worked and create a new environment

```bash
conda --version
conda create --name python3 python=3.6
activate python3
pip install -r requirements.txt
```

### Run the App

Once you are inside the new conda environment you created, you can start the bot.

```bash
cd discordnet
python discordbot.py
```

Heavily inspired by a Facebook Messenger bot: [https://github.com/sentriz/steely](https://github.com/sentriz/steely)