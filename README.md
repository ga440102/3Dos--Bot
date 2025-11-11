# 🔗 3Dos BOT

> Automated 3Dos node management with multi-threading and advanced proxy support

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vonssy/3Dos-BOT.svg)](https://github.com/vonssy/3Dos-BOT/stargazers)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Setup & Usage](#setup--usage)
- [Support](#support)
- [Contributing](#contributing)

## 🎯 Overview

3Dos BOT is a automated tool designed to manage 3Dos nodes efficiently with multi-threading support. It provides seamless integration with free and private proxies, automated token extraction, and connection management with 3Dos Node Extension.

**🔗 Get Started:** [Register on 3Dos Network](https://dashboard.3dos.io/register?ref_code=a78e39)  
**🎁 Use My Code:** `a78e39`

## ✨ Features

- 🔄 **Automated Account Management** - Retrieve account information automatically
- 🌐 **Flexible Proxy Support** - Run with or without proxy configuration
- 🔀 **Smart Proxy Rotation** - Automatic rotation of invalid proxies
- 🔌 **Extension Integration** - Auto-connect with 3Dos Node Extension
- ⏰ **Daily Check-In** - Automated claim daily check-in
- ⚡ **Multi-Threading Support** - Handle multiple accounts simultaneously
- 🛡️ **Advanced Security** - Multiple proxy layers for enhanced protection

## 📋 Requirements

- **Python:** Version 3.9 or higher
- **pip:** Latest version recommended
- **Capmonster Key:** Optional (for automated captcha solving)

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vonssy/3Dos-BOT.git
cd 3Dos-BOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
# or for Python 3 specifically
pip3 install -r requirements.txt
```

## ⚙️ Configuration

### Captcha Key Setup (Optional)

Create or edit `capmonster_key.txt` in the project directory:

```
your_capmonster_key
```

### Account Configuration

Create or edit `accounts.json` in the project directory:

```json
[
    {
        "Email": "your_email_address_1",
        "Password": "your_password_1"
    },
    {
        "Email": "your_email_address_2",
        "Password": "your_password_2"
    }
]
```

### Automatic Token Generation

The bot can automatically fetch access tokens using your capmonster key through the setup script.

### Manual Token Setup (Alternative)

If you prefer to fetch tokens manually or don't have a capmonster key, you can extract access tokens from the 3Dos dashboard:

<div align="center">
  <img src="images/example.png" alt="3Dos Access Token Example" width="500">
  <p><em>Example of extracting access tokens manually using browser developer tools</em></p>
</div>

Create or edit `tokens.json`:

```json
[
    {
        "Email": "your_email_address_1",
        "access_token": "your_access_token_1"
    },
    {
        "Email": "your_email_address_2",
        "access_token": "your_access_token_2"
    }
]
```

### Proxy Configuration (Optional)

Create or edit `proxy.txt` in the project directory:

```
# Simple format (HTTP protocol by default)
192.168.1.1:8080

# With protocol specification
http://192.168.1.1:8080
https://192.168.1.1:8080

# With authentication
http://username:password@192.168.1.1:8080
```

## 🚀 Setup & Usage

### Automatic Token Setup (Recommended)

Run the setup script to automatically fetch access tokens using your configured capmonster key and account credentials:

```bash
python setup.py
# or for Python 3 specifically
python3 setup.py
```

> **💡 What does setup.py do?**
> - Automatically logs in to your 3Dos accounts
> - Solves captchas using your capmonster key
> - Extracts access tokens automatically
> - Saves tokens to `tokens.json` for the bot to use

### Start the Bot

After running the setup, launch the 3Dos BOT:

```bash
python bot.py
# or for Python 3 specifically
python3 bot.py
```

### Runtime Options

When starting the bot, you'll be prompted to choose:

1. **Proxy Mode Selection:**
   - Option `1`: Run with proxies
   - Option `2`: Run without proxy

## 💖 Support the Project

If this project has been helpful to you, consider supporting its development:

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. ⭐ **Star this repository** if you find it useful
2. 👥 **Follow** for updates on new features
3. 🐛 **Report issues** via GitHub Issues
4. 💡 **Suggest improvements** or new features
5. 🔧 **Submit pull requests** for bug fixes or enhancements

## 📞 Contact & Support

- **Developer:** vonssy
- **Purchase:** [Telegram @NextGen Nexus](https://t.me/Next_Gen_nexus)

<div align="center">

**Made with ❤️ by [AKHII](https://github.com/dopezayn)**

*Thank you for your interest in 3Dos BOT!*  

</div>
