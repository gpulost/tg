from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest

# 替换为你的 API ID 和 Hash
api_id = '4'
api_hash = '014b35b6184100b085b0d0572f9b5103'
# phone_number = '+123456789'  # 你的 Telegram 账号绑定的手机

# 创建客户端
# client = TelegramClient('demox01', api_id, api_hash)
from telethon import TelegramClient

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('demox01', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))

async def check_telegram_account(phone):
    async with client:
        # 添加联系人
        result = await client(ImportContactsRequest([{'phone': phone}]))
        
        if result.users:
            print(f"号码 {phone} 是有效的 Telegram 用户")
            # 获取更多信息
            print(result.users[0])
        else:
            print(f"号码 {phone} 不是 Telegram 用户")

        # 删除联系人（避免联系人列表堆积）
        await client(DeleteContactsRequest([phone]))

# 检测号码
phone_to_check = '+66910020199'
phone_to_check = '+447743695156'
# client.loop.run_until_complete(check_telegram_account(phone_to_check))
