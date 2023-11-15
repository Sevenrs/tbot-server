# T-Bot Rewritten Python Server
This repository contains the source code for the T-Bot Rewritten Python server.

Open sourced for everyone to use. I'm not coming back to the scene.

This repository does not and will not contain any website logic. I'm not willing to share that portion as that is out of the scope of the project and portions of said code is still being using used for my current projects.

## Installation
1. Open `migrations/tbot-base.sql` and run the SQL commands. This will create the database required to run the server.
2. Run `cp default.env .env` to create a configuration file. This file will hold all shared variables such as database information that the server will be using to connect with.
3. Open `.env` and configure the server as you'd like it to be configured. Do note that `.env` is in `.gitignore` and will not be pushed to any git server for security reasons. Do not modify this behavior, as it is intended and good practice.
4. Run `python main.py` to start all servers and use a suitable client to connect and start playing.

A default account with username and password `icseon` is already available.

## Game Client Compatibility
A suitable T-Bot Rewritten client is required to connect to the server. If you do for some reason not trust me, you can use a regular Bots client as well and remove the xor and modify the authentication code to not read the username from the client.

By doing so, you will face the following limitations:
1. Games can not be started because file hash validation will always fail.
2. You will be automatically banned every time you finish a game due to the anti cheat doing its job.
3. You may not be able to connect to the game server. This is because the version string is not sent by Bots.
4. You will not be able to use the Warnet bonus. Bots does not support this. The Korean Bout client does support this and this code should be compatible with a season 2 Bout client as well.
5. You will not be able to use the in-room shop. Bots does not support this.
6. The shop, inventory and room have different packet structures than the ones from Bots. You will not be able to use these features without unexpected behavior or straight up crashing.
7. Your client will freeze when you login. T-Bot supports connections to be closed immediately while Bots/Bout does not - this is because these clients send an additional packet while T-Bot does not.
8. Multiple logins from the same IP address will no longer work. I modified the client to send the username along with the authentication request packet when connecting to the game server to combat this issue. Neither Bout or Bots does this natively.
9. In-room chat commands will not work. I added this feature myself.

Alterations can be made to combat these limitations but is out of the scope of this publication.

The latest T-Bot Rewritten client can be downloaded here: https://drive.google.com/file/d/1mwyJRZAcBjuXJzzC9EgoU6b-92iucymu/view

_Note: The launcher will not work. This is because T-Bot Rewritten has ceased operations._

## Notes
I wrote this code 3 years ago now. I'll be the first to admit that there are some bad practices in here. I've made the code PEP8 compliant and tried to remove most bad things without breaking the code.
