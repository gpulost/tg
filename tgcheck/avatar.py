import os
import sys
import json
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.types import InputPhoneContact
from dotenv import load_dotenv, find_dotenv
import random
from loguru import logger
from telethon import functions, types


# 配置logger同时显示到console和文件
logger.add("logs/avatar_{time}.log", rotation="1 day", retention="7 days", level="DEBUG")
logger.add(sys.stdout, level="DEBUG")


def get_session_string(app_id, app_hash, session_file):
    """
    从SQLite session文件获取StringSession

    Args:
        app_id: Telegram API ID
        app_hash: Telegram API Hash
        session_file: SQLite session文件名(不含.session后缀)

    Returns:
        str: session字符串, 失败返回None
    """
    # 使用 SQLite 文件中的 session 初始化客户端
    import logging
    logging.basicConfig(level=logging.DEBUG)
    client = TelegramClient(session_file, app_id, app_hash)

    try:
        # 连接并确认会话可用
        client.connect()
        if not client.is_user_authorized():
            print("Session 失效，需要重新登录。")
            return None

        # 将当前 session 转换为 StringSession
        session_string = StringSession.save(client.session)
        print("成功获取 StringSession：")
        print(session_string)
        return session_string

    except Exception as e:
        print(f"获取session失败: {str(e)}")
        return None

    finally:
        client.disconnect()


def generate_random_person_first_name():
    return random.choice(["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hank"])

def generate_random_person_last_name():
    return random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"])

def get_photo_url(client, user_id):
    """
    Photos(
        photos=[
            Photo(
                id=5778668688071838108,
                access_hash=-7005645242948420541,
                file_reference=b'\x00g\x86&@\x87\xa5_#\x93\x81cY\xbe\xe5\xa9\xc4\xb4\xc2T\xc7',
                date=datetime.datetime(2025, 1, 14, 8, 53, 46, tzinfo=datetime.timezone.utc),
                sizes=[
                    PhotoSize(
                        type='a',
                        w=160,
                        h=160,
                        size=11411
                    ),
                    PhotoSize(
                        type='b',
                        w=320,
                        h=320,
                        size=34705
                    ),
                    PhotoSize(
                        type='c',
                        w=640,
                        h=640,
                        size=97171
                    ),
                    PhotoStrippedSize(
                        type='i',
                        bytes=b'\x01((\xd3\xf3\x94\xf4\xa4\xf3\x94&X\x8c\xfa\n\xaa\xd8\x1c\x01\xcd1\x86\x00\xcd1\x138\xde\xac\xecB\xe7\xa0\x1d\xbe\xbe\xf5Z4\xc4\xd2\x00\xc7n\x01\x03\xd2\x9d\xe5\x99J&\xde\t\xc9>\xc2\xacI\x1a\x81\xd3\x93\xde\x91]\x00B\xa3\xa9-\x8f\xd6\x8a\x8a5 \xe4\x92=\x06h\xa7bG2\x88\xc6r\x18\xf7\xcd@\xcd\x92)\xe4\x11\xd6\x98>gP\x06i\x01f\x1c\xae\xd1\x82r2MH\xe3*}\xea\x11!\x07kv\xefO\xdd\x92\t=;PQ\x0eWy\r\xc1\x07\xbd\x14\xef7\xf7\x87p#\xf0\xa2\xa8\x91\x92\x03\x8cQ\n\x10\xfb\xcfaE\x15 \x84d\x91\x98\xb2\x95\xc59\x9bb\x81\xf3\x13\xeb\x8e\xb4QLw%YT\xf5\xe3\xebE\x14S$'
                    ),
                ],
                dc_id=4,
                has_stickers=False,
                video_sizes=[
                ]
            ),
        ],
        users=[
        ]
    )
    """
    

def main():
    # account info
    json_path = "accounts/12065061831.json"
    session_file = json_path.replace('.json', '')

    # prepare credentials 
    with open(json_path, 'r') as f:
        data = json.load(f)
    country_code = data['phone'][:2]
    phone_number = data['phone']
    app_id = str(data['app_id'])
    app_hash = data['app_hash']
    session = get_session_string(app_id, app_hash, session_file)
    print(phone_number, app_id, app_hash, session)

    if not app_id or not app_hash or not session:
        print("请设置 SESSION、TELEGRAM_API_ID 和 TELEGRAM_API_HASH 环境变量")
        sys.exit(1)

    to_be_check_phone_number = "+447743695156"
    proxy = {
        'proxy_type': 'http',
        'addr': 'zproxy.lum-superproxy.com',
        'port': 32223,
        'username': 'lum-customer-c_7dcc6b25-zone-10018772-dns-remote-country-US-session-18963979',
        'password': '0GD3GjHj9tlLO'
    }
    client = TelegramClient(StringSession(session), app_id, app_hash, proxy=proxy)
    try:
        client.connect()
        if not client.is_user_authorized():
            logger.error("用户未授权，请检查 StringSession 有效性。")
            return
        
        contact = InputPhoneContact(
            client_id=0,  # 可以是任意整数
            phone=to_be_check_phone_number,
            first_name=generate_random_person_first_name(),
            last_name=generate_random_person_last_name()
        )

        # 添加电话号码为联系人
        result = client(ImportContactsRequest([contact]))
        logger.info(result)

        if result.users:
            print(result.users[0])
            user_id = result.users[0].id
            logger.info(f"user_id: {user_id}")
            client.download_profile_photo(result.users[0], file="avatar.jpg", download_big=True)
            # result = client(functions.photos.GetUserPhotosRequest(
            #     user_id=user_id,
            #     offset=0,
            #     max_id=0,
            #     limit=5,
            # ))
            # # import pdb;pdb.set_trace()
            # print(result.stringify())
            # client.download_media(result.photos[0].sizes[0].url, file_name="avatar.jpg")

    except Exception as e:
        logger.error(f"检测失败: {str(e)}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
