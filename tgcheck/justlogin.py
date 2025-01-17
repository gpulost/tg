from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import json

import logging
logging.basicConfig(level=logging.DEBUG)
import os
# 替换为实际的 session 文件路径
from tg import get_session_string

data = json.load(open("12065061784.json", "r"))
session_file = data['session_file']
api_id = data['app_id']
api_hash = data['app_hash']

# session_string = "1AZWarzYBuyvIjgMY3b6_3hhY6N8KeyOtys0zCFsPMFnDyyVBrUbTpecs1cIr9AZdvShWbJrG1DaFC9A8gk5zyy0zrbiBr2gJpMQWrV9Z0pZtHxLib4pD4-ZDk1H_dtFYDa1UupZqZvKb2PQvkczPDlDAIPUXGAaxwcThQRJaQFUv_xqU8xJ9r6TRU0ihUti7BU-TwqL0fdbMwEMq1yO2SzmKrosGXRHS_T0dNfz5eryyzbswfBXvOk9ySW2hUpUWm8Er_DGYBu8WzaeWUplSS_nbE3v_CPRpMTlAfHZcgfOv-9bIsNRXk9aKTDg_Ezi-uGl5lPDFhLclMmSQTOxXaQwSw0fFuVE="
# 初始化客户端
client = TelegramClient(
    StringSession(get_session_string(api_id, api_hash, session_file)),
    api_id,
    api_hash,
    device_model=data['device_model'],
    system_version=data['sdk'],
    app_version=data['app_version'],
    lang_code=data['lang_code'],
    system_lang_code=data['system_lang_code'],
)
client.session.save_entities = False

def main():
    # 连接到 Telegram
    client.connect()
    
    # 获取当前登录的用户信息
    me = client.get_me()
    print(f"Logged in as: {me.first_name} {me.last_name}")

    # 发送测试消息
    client.send_message("gpulost", "Hello from bot!")

# 运行
main()
