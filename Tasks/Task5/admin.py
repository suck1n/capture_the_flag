import asyncio
import os
import time

import requests as req
from bs4 import BeautifulSoup

URL = "http://127.0.0.1:5005"
CHROME_PATH = "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

if not os.path.exists("admin-password.txt"):
    with open("admin-password.txt", "wb") as f:
        f.write(os.urandom(16).hex().encode())
        # f.write(os.getrandom(16).hex().encode())

with open("admin-password.txt", "rb") as f:
    admin_password = f.read().strip()


def open_profile(user):
    session = req.Session();

    session.post(f"{URL}/login", data={"username": "admin", "password": admin_password})

    response = session.get(f"{URL}/profile/{user}")

    soup = BeautifulSoup(response.text, 'html.parser')
    image_url = soup.div.div.div.img["src"]

    if image_url.startswith("https") or image_url.startswith("http"):
        session.get(image_url)


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
    coro = asyncio.start_server(handle_request, "127.0.0.1", 6005)
    server = loop.run_until_complete(coro)

    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Quitting server")


if __name__ == "__main__":
    main()
