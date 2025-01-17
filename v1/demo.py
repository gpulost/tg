from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from loguru import logger
import logging

logging.basicConfig(level=logging.DEBUG)
# Remember to use your own values from my.telegram.org!
# api_id = 4
# api_hash = '014b35b6184100b085b0d0572f9b5103'
creds = '4#@#014b35b6184100b085b0d0572f9b5103#@#1BJWap1sBuyb33RrWWp1lqwdL5CByOl8FejqK_cC-3F2_sHYlAf2xzdj8i4FdTnYZ2IU1_fSgGfIZCEuZjGWv94pHN8uSNNzHUThVMnF9dKl52h4FgEZoqveNv5JKkVjafQBmJeAPnrQ5Ypo8xYHdJ33VoK6WzJKVRnIDp7BfbdSo2QsyswXUeg44heoM_2j6CobzAZvIA-OUp4iz111fa5X6MKEY2Cabg_g36sYg0EVKXs3-BJzRTS84lIRpiaWP-RRDPnJAWF9fWbtiBibyo2p2DTnWhhGEyNK4Ga5Pcn4joM4VrrnrM9yOv83pFZ5JerPxIhpz7Ou2hqrR-ZFCWaOAlz62Wx0='
creds = '4#@#014b35b6184100b085b0d0572f9b5103#@#1BJWap1sBux7b0zfAc97C0dz38dgJepVZq-y2qagHPVab5n2EEolSIBTGx2KhSF5eZCsvEB_sPeZNpN9ePBZYzs4-UQo3GFXzfbYuZMDHjPh6nARf2EqgAGjs_SXe8gLdI6_yUxi27ULe6tHpaX-qjqbT7UkVux6Iab9IFIl1EOeF0gysssKNdROip61YTxIiLjZuh-MGpjQwJFq6f0WQXdheFAicxK4Z9thE7XOEZGjj9GATKfOjeH_mQVK_JrlfI3YnGNot67QKCWODspc_RA-PPvGpEV6PoxxMAnJmFzK35sk-6QJVubLN5ADGlNF2va96etCJaDcQQGYQgRCvuZhsF1c5bYg='
api_id, api_hash, session =  creds.split('#@#')
logger.info(f'api_id: {api_id}, api_hash: {api_hash}, session: {session}')
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    logger.info(f'client: {client}')
    client.loop.run_until_complete(client.send_message('gpulost', 'Hi'))


# async def main():
#     # Getting information about yourself
#     me = await client.get_me()

#     # "me" is a user object. You can pretty-print
#     # any Telegram object with the "stringify" method:
#     print(me.stringify())

#     # When you print something, you see a representation of it.
#     # You can access all attributes of Telegram objects with
#     # the dot operator. For example, to get the username:
#     username = me.username
#     print(username)
#     print(me.phone)

#     # You can print all the dialogs/conversations that you are part of:
#     async for dialog in client.iter_dialogs():
#         print(dialog.name, 'has ID', dialog.id)

#     # You can send messages to yourself...
#     # await client.send_message('me', 'Hello, myself!')
#     # # ...to some chat ID
#     # await client.send_message(-100123456, 'Hello, group!')
#     # ...to your contacts
#     # await client.send_message('+34600123123', 'Hello, friend!')
#     # ...or even to any username
#     await client.send_message('gpulost', 'Testing Telethon!')

#     # You can, of course, use markdown in your messages:
#     message = await client.send_message(
#         'gpulost',
#         'This message has **bold**, `code`, __italics__ and '
#         'a [nice website](https://example.com)!',
#         link_preview=False
#     )

#     # Sending a message returns the sent message object, which you can use
#     print(message.raw_text)

#     # You can reply to messages directly if you have a message object
#     await message.reply('Cool!')

#     # Or send files, songs, documents, albums...
#     # await client.send_file('me', '/home/me/Pictures/holidays.jpg')

#     # You can print the message history of any chat:
#     # async for message in client.iter_messages('me'):
#     #     print(message.id, message.text)

#     #     # You can download media from messages, too!
#     #     # The method will return the path where the file was saved.
#     #     if message.photo:
#     #         path = await message.download_media()
#     #         print('File saved to', path)  # printed after download is done

# with client:
#     client.loop.run_until_complete(main())