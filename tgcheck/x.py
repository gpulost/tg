from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, CreateNewSession, UseCurrentSession
import asyncio

async def main():
    
    # Load TDesktop client from tdata folder
    #tdataFolder = r"C:\Users\<username>\AppData\Roaming\Telegram Desktop\tdata"
    tdataFolder = "/tmp/tdata/"
    tdesk = TDesktop(tdataFolder, api=API.TelegramMacOS)
        # Check if we have loaded any accounts
    assert tdesk.isLoaded()

    # Using official iOS API with randomly generated device info
    # print(api) to see more
#    api = API.TelegramIOS.Generate()
#
#    # Convert TDesktop session to telethon client
#    # CreateNewSession flag will use the current existing session to
#    # authorize the new client by `Login via QR code`.
#    client = await tdesk.ToTelethon("newSession.session", CreateNewSession, api)
#
#    # Although Telegram Desktop doesn't let you authorize other
#    # sessions via QR Code (or it doesn't have that feature),
#    # it is still available across all platforms (APIs).
#
#    # Connect and print all logged in devices
#    await client.connect()
#    await client.PrintSessions()

asyncio.run(main())
