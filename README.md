<h1 align="center">QuickInfoBot Telegram Bot</h1>

<p align="center">
  <a href="https://github.com/bisnuray/QuickInfoBot/stargazers"><img src="https://img.shields.io/github/stars/bisnuray/QuickInfoBot?color=blue&style=flat" alt="GitHub Repo stars"></a>
  <a href="https://github.com/bisnuray/QuickInfoBot/issues"><img src="https://img.shields.io/github/issues/bisnuray/QuickInfoBot" alt="GitHub issues"></a>
  <a href="https://github.com/bisnuray/QuickInfoBot/pulls"><img src="https://img.shields.io/github/issues-pr/bisnuray/QuickInfoBot" alt="GitHub pull requests"></a>
  <a href="https://github.com/bisnuray/QuickInfoBot/graphs/contributors"><img src="https://img.shields.io/github/contributors/bisnuray/QuickInfoBot?style=flat" alt="GitHub contributors"></a>
  <a href="https://github.com/bisnuray/QuickInfoBot/network/members"><img src="https://img.shields.io/github/forks/bisnuray/QuickInfoBot?style=flat" alt="GitHub forks"></a>
</p>

<p align="center">
  <em>QuickInfoBot: an advanced Telegram bot script designed to fetch detailed information about shared users, bots, groups, and channels.</em>
</p>
<hr>

## ✨ Features

- 👤 Fetch information about users and bot.
- 📋 Fetch information about private and public groups.
- 📢 Fetch information about private and public channel.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher.
- `telethon` librarie.
- A Telegram bot token (you can get one from [@BotFather](https://t.me/BotFather) on Telegram).
- API ID and Hash: You can get these by creating an application on [my.telegram.org](https://my.telegram.org).

## Installation

To install `telethon` run the following command:

```bash
pip install telethon
```

**Note: If you previously installed `pyrogram`, uninstall it before installing `pyrofork`.**

## Configuration

1. Open the `config.py` file in your favorite text editor.
2. Replace the placeholders for `API_ID`, `API_HASH`, `SESSION_STRING`, and `BOT_TOKEN` with your actual values:
   - **`API_ID`**: Your API ID from [my.telegram.org](https://my.telegram.org).
   - **`API_HASH`**: Your API Hash from [my.telegram.org](https://my.telegram.org).
   - **`BOT_TOKEN`**: The token you obtained from [@BotFather](https://t.me/BotFather).

## Deploy the Bot

```sh
git clone https://github.com/bisnuray/QuickInfoBot
cd QuickInfoBot
python quickinfo.py
```

## How It Works

1. **Start the Bot**: Send the `/start` command to the bot.
2. **Choose an Option**:
   - **Chats**: Fetch details about private and public groups.
   - **Channels**: Fetch details about shared channels.
   - **Bots**: Fetch information about bots.
   - **Users**: Fetch details about private users.
3. **Get Detailed Results**: The bot will display the requested information in a structured format.

✨ **Note**: If you found this repo helpful, please fork and star it. Also, feel free to share with proper credit!

## Author

- Name: Bisnu Ray
- Telegram: [@itsSmartDev](https://t.me/itsSmartDev)

Feel free to reach out if you have any questions or feedback.
