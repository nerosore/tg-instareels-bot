# tg-instareels-bot
Telegram bot that downloads video from Instagram reel link and replies with that video to user.

This bot will download instagram reel to your machine and send it via bot to user.
It uses Selenium for imitating visiting instagram reels section and searching video file in html file.

If downloaded video differs from what it is actually in that link, this means that it's age restricted (because bot is not using Instagram account for searching video, it only has access to public videos)

Usage:
1. Install Python
2. Install following libs: python-telegram-bot, selenium, requests
3. Download main.py
4. Create bot in Telegram @botfather and recieve token
5. Edit main.py - ApplicationBuilder().token('INSERT TOKEN HERE').build()
6. Save
7. Run main.py
8. You can now use your bot and add it to group chats!
