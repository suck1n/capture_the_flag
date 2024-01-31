import asyncio
import os
import time

import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager

dotenv.load_dotenv(".env.local")

URL = f"{os.environ['PROTOCOL']}://{os.environ['SERVER_HOST']}:{int(os.environ['SERVER_PORT'])}"

if not os.path.exists("admin-password.txt"):
    with open("admin-password.txt", "wb") as f:
        f.write(os.getrandom(16).hex().encode())

with open("admin-password.txt", "rb") as f:
    admin_password = f.read().strip().decode()


def open_profile(user):
    print("starting browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    options.add_argument('--headless=new')

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options
) as browser:
        print("started!")

        browser.get(f"{URL}/login")

        print("logging in...")

        browser.find_element(By.NAME, "username").send_keys("admin")
        browser.find_element(By.NAME, "password").send_keys(admin_password)
        browser.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)

        print("logged in!")

        print(f"getting profile {user}")

        browser.get(f"{URL}/profile/{user}")

        print(f"Current url: {browser.current_url}")

        url = browser.find_element(By.TAG_NAME, "img").get_attribute("src")
        print(f"waiting for image to load request... {url}")

        # time.sleep(3)


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
