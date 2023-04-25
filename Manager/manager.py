#!/usr/bin/env python3

import curses
import math
import shlex
import traceback
from curses import wrapper
from threading import Thread

import terminal
from server import Server


def print_cmd(ter, output, cmd, desc, command_length, description_length):
    ter.write(output, f"{(' ' + cmd):<{command_length}}┃"
                      f"{(' ' + desc):<{description_length}}\n", clear=False)


def print_help(ter, output):
    curses.update_lines_cols()

    command_length = math.floor((curses.COLS - 2) * 0.3)
    description_length = math.floor((curses.COLS - 2) * 0.7)

    ter.write(output, f"{' Command':<{command_length}}┃"
                      f"{' Description':<{description_length}}\n")

    ter.write(output, "━" * command_length + "╋" +
              "━" * description_length + "\n",
              clear=False)

    print_cmd(ter, output, "CTRL+D", "Exit Program/Server/Help Page", command_length, description_length)
    print_cmd(ter, output, "help", "Shows this help page", command_length, description_length)
    print_cmd(ter, output, "add <name> <directory> <program>", "Add a new server. <directory> is the location of the "
                                                               "starting <program>", command_length, description_length)
    print_cmd(ter, output, "remove <id>", "Removes the server", command_length, description_length)
    print_cmd(ter, output, "start <id>", "Starts the server", command_length, description_length)
    print_cmd(ter, output, "stop <id>", "Stops the server", command_length, description_length)
    print_cmd(ter, output, "open <id>", "Opens the terminal for the server", command_length, description_length)


def print_servers(ter, output, servers):
    curses.update_lines_cols()

    id_length = max(4, len(str(len(servers))) + 2)
    server_length = math.floor((curses.COLS - 3 - id_length) * 0.8)
    running_length = math.floor((curses.COLS - 3 - id_length) * 0.2)

    ter.write(output, f"{'ID':^{id_length}}┃"
                      f"{' Server':<{server_length}}┃"
                      f"{' Running':<{running_length}}\n")

    ter.write(output,
              "━" * id_length + "╋" +
              "━" * server_length + "╋" +
              "━" * running_length + "\n",
              clear=False)

    for server_id, server in enumerate(servers):
        ter.write(output,
                  f"{(server_id + 1):^{id_length}}┃"
                  f"{(' ' + server.get_name()):<{server_length}}┃"
                  f"{(' ✓' if server.is_running() else ' ❌'):<{running_length - 2}}\n",
                  clear=False)


def console_listener(input_window, output_window, servers):
    ter = terminal.Terminal()
    show_help = False

    while True:
        try:
            result = ter.read(input_window)

            if result.equals(terminal.CTRL_D):
                if show_help:
                    show_help = False
                    ter.toggle_cursor()
                    print_servers(ter, output_window, servers)
                    continue
                break
            if result.equals(terminal.RESIZE):
                if show_help:
                    print_help(ter, output_window)
                else:
                    print_servers(ter, output_window, servers)
                continue

            cmd, *args = result.get_line().split(" ")

            if cmd == "add":
                if len(args) < 3:
                    continue

                server_name, directory, program_args = args[0], args[1], shlex.split(" ".join(args[2:]))
                servers.append(Server(server_name, directory, program_args))
                print_servers(ter, output_window, servers)
            elif cmd == "remove":
                if len(args) != 1:
                    continue

                for server_id, server in enumerate(servers):
                    if server_id == int(args[0]) - 1:
                        servers.pop(server_id)
                        print_servers(ter, output_window, servers)
                        break
            elif cmd == "start":
                if len(args) != 1:
                    continue

                for server_id, server in enumerate(servers):
                    if server_id == int(args[0]) - 1:
                        server.start_program(lambda: print_servers(ter, output_window, servers))
                        print_servers(ter, output_window, servers)
                        break
            elif cmd == "stop":
                if len(args) != 1:
                    continue

                for server_id, server in enumerate(servers):
                    if server_id == int(args[0]) - 1:
                        server.stop_program()
                        print_servers(ter, output_window, servers)
                        break
            elif cmd == "open":
                if len(args) != 1:
                    continue

                for server_id, server in enumerate(servers):
                    if server_id == int(args[0]) - 1:
                        server.open_terminal(input_window, output_window)
                        print_servers(ter, output_window, servers)
                        break
            elif cmd == "help":
                if len(args) != 0:
                    continue
                show_help = True
                print_help(ter, output_window)
                ter.toggle_cursor()
            elif cmd == "quit":
                break
        except:
            ter.write(output_window, "Error: " + traceback.format_exc())


def main(screen):
    text_window = curses.newwin(curses.LINES - 1, curses.COLS, 0, 0)
    input_window = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)

    text_window.keypad(True)
    input_window.keypad(True)

    text_window.scrollok(True)

    servers = []
    print_servers(terminal.Terminal(), text_window, servers)

    threads = [
        Thread(target=console_listener, args=[input_window, text_window, servers]),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for server in servers:
        server.stop_program()


if __name__ == "__main__":
    wrapper(main)
