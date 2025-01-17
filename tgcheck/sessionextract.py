import asyncio
import logging
import os
import sys
from telethon.sessions import StringSession
from telethon import TelegramClient, errors
from getpass import getpass
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

proxy_CL = {
    'proxy_type': 'http',
    'addr': 'zproxy.lum-superproxy.com',
    'port': 32223,
    'username': 'lum-customer-c_7dcc6b25-zone-10018772-dns-remote-country-CL-session-24574397',
    'password': '0GD3GjHj9tlLO'
}

async def login(phone: str) -> TelegramClient:
    """Create a telethon session or reuse existing one"""
    logging.info("Logging in...")
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    client = TelegramClient(phone, API_ID, API_HASH, proxy=proxy_CL)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(
                phone, input("Enter the code (sent on telegram): ")
            )
        except errors.SessionPasswordNeededError:
            pw = getpass(
                "Two-Step Verification enabled. Please enter your account password: "
            )
            await client.sign_in(password=pw)
    logging.info("Done.")
    return client

async def main():
    if len(sys.argv) != 2:
        print("Usage: python session2str.py <phone_number>")
        sys.exit(1)

    phone_number = sys.argv[1]
    client = await login(phone_number)
    string = StringSession.save(client.session)
    print(string)
    with open(f"{phone_number}.txt", "w") as f:
        f.write(string)

if __name__ == "__main__":
    asyncio.run(main())