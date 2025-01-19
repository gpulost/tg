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
import time
import logging

logging.basicConfig(level=logging.DEBUG)

stumps = ["+15413006705", "+447743695156", "919038216291","918348412132","919903308121","916290476009","918420747293","919830325666","919830648745","919330543746","919836763322","919830814171","919123863542","919123530455","918348000919","917003797559","919123517291","918420373088","919831559633","919874472267","919163253738","919875080029","919088033199","917003079668","916290567101","918777232576","919051428079"]

pdf_reader = None # PDFReader()
# 获取随机片段


# 配置logger同时显示到console和文件
logger.remove()
logger.add("logs/0118_{time}.log", rotation="1 day", retention="7 days", level="DEBUG")
logger.add(sys.stdout, level="DEBUG")

# 加载环境变量
_ = load_dotenv(find_dotenv())

def parse_proxy_string(proxy_str):
    """
    Parse proxy string in format username:password@addr:port into proxy dict
    """
    # Split address and credentials
    creds_addr = proxy_str.split('@')
    if len(creds_addr) != 2:
        raise ValueError("Invalid proxy string format")
    
    # Split username:password and addr:port
    username_pass = creds_addr[0].split(':')
    addr_port = creds_addr[1].split(':')
    
    if len(username_pass) != 2 or len(addr_port) != 2:
        raise ValueError("Invalid proxy string format")
        
    return {
        'proxy_type': 'http',
        'addr': addr_port[0],
        'port': int(addr_port[1]),
        'username': username_pass[0],
        'password': username_pass[1]
    }

with open("proxies_(random)_10000.txt", "r") as f:
    proxies = [parse_proxy_string(line.strip()) for line in f.readlines()]
proxy = random.choice(proxies)
logger.info(f"using proxy: {proxy}")

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
    client = TelegramClient(session_file, app_id, app_hash, proxy=proxy)

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


def mock_send_message(client: TelegramClient):
    try:
        phone = "+15413006705"
        # 先尝试直接发送消息
        try:
            logger.info(f"Sending message to {phone}")
            client.send_message(phone, "how are you")
            return
        except ValueError:
            # 如果失败，说明需要先建立联系人
            contact = InputPhoneContact(
                client_id=0,
                phone=phone,
                first_name="Test",
                last_name=""
            )
            # 添加为联系人
            result = client(ImportContactsRequest([contact]))
            if result.users:
                # 使用获取到的用户实体发送消息
                client.send_message(result.users[0], "test")
                client(DeleteContactsRequest(result.users))
    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}")


def generate_random_person_first_name():
    return random.choice(["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hank"])

def generate_random_person_last_name():
    return random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"])


def check_core(client: TelegramClient, phone_number):
    contact = InputPhoneContact(
        client_id=random.randint(10000000, 99999999),  # 可以是任意整数
        phone=phone_number,
        first_name=generate_random_person_first_name(),
        last_name=generate_random_person_last_name()
    )

    silent = random.randint(5, 13)
    logger.info(f"waiting for {silent} seconds before import contacts")
    time.sleep(silent)

    # 添加电话号码为联系人
    result = client(ImportContactsRequest([contact]))
    logger.info(result)


    if result.users:
        logger.info(f"号码 {phone_number} 是有效的 Telegram 用户。")
    # 删除联系人（清理临时联系人）
        if result.users:
            silent = random.randint(5, 13)
            logger.info(f"waiting for {silent} seconds before delete contacts")
            time.sleep(silent)
            client(DeleteContactsRequest(result.users))
    else:
        if phone_number in stumps:
            logger.info(f"stumps {phone_number} 未注册 Telegram。")
            sys.exit(-1)
        else:
            logger.error(f"号码 {phone_number} 未注册 Telegram。")
    

def check_phone_numbers(app_id, app_hash, session_string, phone_numbers):
    """
    检测电话号码是否注册 Telegram

    Args:
        app_id: Telegram API ID
        app_hash: Telegram API Hash
        session_string: StringSession 字符串
        phone_numbers: 待检测的电话号码 (格式: +1234567890)

    Returns:
        bool: True 表示已注册 Telegram, False 表示未注册或失败
    """
    # 使用 StringSession 初始化客户端
    client = TelegramClient(StringSession(session_string), app_id, app_hash, proxy=proxy)

    try:
        # # 连接客户端
        client.connect()
        if not client.is_user_authorized():
            logger.error("用户未授权，请检查 StringSession 有效性。")
            return False

        # mock_send_message(client)
        
        print(client.get_me().stringify())
        for index, phone_number in enumerate(phone_numbers):
            logger.info(f"Checking {index + 1} / {len(phone_numbers)}: {phone_number}")
            if not client.is_user_authorized():
                logger.error("用户未授权，请检查 StringSession 有效性。")
                return False
            # mock_send_message(client)
            # 创建 InputPhoneContact 对象
            check_core(client, phone_number)

            # 随机静默
            # silent = random.randint(3, 10)
            # import time; time.sleep(silent)
            # logger.info(f"waiting for {silent} seconds")

            # 有效性检查
            if index % 10 == 0:
                check_core(client, random.choice(stumps))
    except Exception as e:
        logger.error(f"检测失败: {str(e)}")
    finally:
        client.disconnect()

# 主函数
if __name__ == "__main__":
    # 从环境变量中读取 API 配置
    with open("0118/573235459850.json", 'r') as f:
        data = json.load(f)
    country_code = data['phone'][:2]
    phone_number = data['phone']
    app_id = str(data['app_id'])
    app_hash = data['app_hash']
    session_file = f"0118/{data['session_file']}"
    session = get_session_string(app_id, app_hash, session_file)
    print(phone_number, app_id, app_hash, session)

    if not app_id or not app_hash or not session:
        print("请设置 SESSION、TELEGRAM_API_ID 和 TELEGRAM_API_HASH 环境变量")
        sys.exit(1)

    with open("ctusmr6p2jvlleut3oc0.txt", "r") as f:
       phone_numbers = [line.strip() for line in f.readlines()]
    check_phone_numbers(app_id, app_hash, session, phone_numbers[3000+24+23:5000])
