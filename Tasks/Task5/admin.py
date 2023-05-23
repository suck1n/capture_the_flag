import asyncio
import os
import time

import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

dotenv.load_dotenv(".env.local")

URL = f"http://{os.environ['SERVER_HOST']}:{int(os.environ['SERVER_PORT'])}"

if not os.path.exists("admin-password.txt"):
    with open("admin-password.txt", "wb") as f:
        f.write(os.getrandom(16).hex().encode())

with open("admin-password.txt", "rb") as f:
    admin_password = f.read().strip().decode()


def open_profile(user):
    browser = webdriver.Firefox()

    browser.get(f"{URL}/login")

    time.sleep(2)

    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys(admin_password)
    browser.find_element(By.TAG_NAME, "button").click()

    time.sleep(2)

    browser.get(f"{URL}/profile/{user}")

    time.sleep(2)


async def handle_request(reader, writer):
    connection_id = f"{time.strftime('%FT%T%z')}-{os.urandom(4).hex()}"
    
    print(f"New connection: {connection_id}")
    
    user_id = (await reader.readline()).strip().decode().upper()
    print(f"{connection_id}: Received User Complaint {user_id}")

    open_profile(user_id)

    print(f"{connection_id}: Connection done.")
    writer.close()


def main():
    # Starts the Server
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_request, os.environ['ADMIN_CONTACT_HOST'], int(os.environ['ADMIN_CONTACT_PORT']))
    server = loop.run_until_complete(coro)

    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Quitting server")


if __name__ == "__main__":
    main()
