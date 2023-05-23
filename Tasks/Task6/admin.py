import asyncio
import os
import time

import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = f"http://{os.environ['SERVER_HOST']}:{int(os.environ['SERVER_PORT'])}"

if not os.path.exists("admin-password.txt"):
    with open("admin-password.txt", "wb") as f:
        f.write(os.getrandom(16).hex().encode())

with open("admin-password.txt", "rb") as f:
    admin_password = f.read().strip().decode()


def open_url(url):
    browser = webdriver.Chrome()

    browser.get(f"{URL}/login")

    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys(admin_password)
    browser.find_elements(By.TAG_NAME, "input")[2].click()

    browser.get(url)

    time.sleep(2)


async def handle_request(reader, writer):
    connection_id = f"{time.strftime('%FT%T%z')}-{os.urandom(4).hex()}"

    print(f"New connection: {connection_id}")

    url = (await reader.readline()).strip().decode()
    print(f"{connection_id}: Received Contact Form: {url}")

    if url.startswith("https") or url.startswith("http"):
        open_url(url.split(" ")[0])

    print(f"{connection_id}: Connection done.")
    writer.close()


def main():
    dotenv.load_dotenv(".env.local")

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
