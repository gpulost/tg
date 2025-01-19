import os
import time
import sys
import json
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.types import InputPhoneContact
from dotenv import load_dotenv, find_dotenv
import random
import string

# 加载环境变量
_ = load_dotenv(find_dotenv())

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

def check_phone_numbers(app_id, app_hash, session_string, phone_numbers):
    """
    批量检测电话号码是否注册 Telegram
    """
    client = TelegramClient(StringSession(session_string), app_id, app_hash)
    results = {}

    try:
        client.connect()
        if not client.is_user_authorized():
            print("用户未授权，请检查 StringSession 有效性。")
            return results

        # 修改为每次只处理5个号码
        batch_size = 50
        for i in range(0, len(phone_numbers), batch_size):
            batch = phone_numbers[i:i + batch_size]
            contacts = []
            
            print(f"\n正在处理第 {i+1}-{min(i+batch_size, len(phone_numbers))} 个号码...")
            
            # 每个批次前增加较长的随机延迟
            batch_delay = random.uniform(8.0, 15.0)
            print(f"batch_delay: {batch_delay}")
            time.sleep(batch_delay)
            
            for phone in batch:
                # 每个号码处理前增加短暂延迟
                delay = random.uniform(1.0, 2.5)
                print(f"short delay: {delay}")
                time.sleep(delay)
                
                random_client_id = random.randint(10000000, 99999999)
                first_name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8)))
                last_name = ''.join(random.choices(string.ascii_letters, k=random.randint(3, 6)))
                
                contact = InputPhoneContact(
                    client_id=random_client_id,
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name
                )
                contacts.append(contact)

            try:
                result = client(ImportContactsRequest(contacts))
                
                with open('result.txt', 'a', encoding='utf-8') as f:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    for user in result.users:
                        if hasattr(user, 'phone'):
                            results[user.phone] = True
                            msg = f"[{timestamp}] 号码 {user.phone} 已注册 Telegram"
                            print(msg)
                            f.write(msg + '\n')
                    
                    for contact in contacts:
                        if contact.phone not in results:
                            results[contact.phone] = False
                            msg = f"[{timestamp}] 号码 {contact.phone} 未注册 Telegram"
                            print(msg)
                            f.write(msg + '\n')

                # 删除添加的联系人前增加延迟
                time.sleep(random.uniform(2.0, 4.0))
                if result.users:
                    client(DeleteContactsRequest(result.users))
                    # 删除后增加额外延迟
                    time.sleep(random.uniform(3.0, 5.0))

            except Exception as e:
                error_msg = f"处理批次 {i+1}-{min(i+batch_size, len(phone_numbers))} 时出错: {str(e)}"
                print(error_msg)
                with open('error_log.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] {error_msg}\n")
                
                # 发生错误时增加更长的等待时间
                time.sleep(random.uniform(20.0, 30.0))
                continue

    except Exception as e:
        print(f"检测过程发生错误: {str(e)}")
        with open('error_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] 检测过程发生错误: {str(e)}\n")

    finally:
        client.disconnect()
        
    return results

# 主函数
if __name__ == "__main__":
    # 从环境变量中读取 API 配置
    dir_path = "./"
    for file in os.listdir(dir_path):
        if not file.endswith('.json'):
            continue
        json_path = os.path.join(dir_path, file)
        session_file = json_path.replace('.json', '')
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

        # 读取待检测的号码列表
        # phone_numbers = ["918337074129"]
        # with open('input', 'r') as f:
        #     for line in f:
        #         phone = line.strip()
        #         if phone:
        #             phone_numbers.append(phone)

        # 批量检测号码
        with open("ctusmr6p2jvlleut3oc0.txt", "r") as f:
            phone_numbers = [line.strip() for line in f.readlines()]
        results = check_phone_numbers(app_id, app_hash, session, phone_numbers)

        ## 输出结果
        #for phone, is_registered in results.items():
        #    status = "已注册" if is_registered else "未注册"
        #    print(f"号码 {phone} {status} Telegram")
