import os
import signal
from subprocess import PIPE, Popen, STDOUT
from threading import Thread

import terminal


class Server:

    def __init__(self, name, directory, program):
        self.name = name
        self.directory = directory
        self.program = program
        self.output = ""
        self.running = False
        self.terminal_open = False
        self.process = None

    def get_name(self):
        return self.name

    def is_running(self):
        return self.running

    def start_program(self, onchange):
        if self.running:
            return

        cwd = os.getcwd()
        os.chdir(self.directory)

        # TODO Add environment (?)
        self.process = Popen(self.program, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        os.set_blocking(self.process.stdout.fileno(), False)

        os.chdir(cwd)

        self.running = True

        Thread(target=self.wait, args=[onchange]).start()

    def stop_program(self):
        if not self.running:
            return

        os.kill(self.process.pid, signal.SIGKILL)

    def wait(self, onchange=None):
        if not self.running:
            return

        self.process.wait()
        self.running = False

        if not self.terminal_open:
            lines = [b.decode() for b in self.process.stdout.readlines()]
            self.output += ("▷ " if len(lines) != 0 else "") + "▷ ".join(lines)
            self.output += "\nexit return code: " + str(self.process.returncode)

            if callable(onchange):
                onchange()

        self.process = None

    def read_to_output(self, ter, output):
        ter.write(output, self.output)

        new_line = True
        while self.running and self.terminal_open:
            value = self.process.stdout.read()
            if value:
                self.output += ("▷ " if new_line else "") + value.decode()
                new_line = b"\n" in value
                ter.write(output, self.output)

    def write(self, message):
        if not self.running:
            return

        self.process.stdin.write(message.encode())
        self.process.stdin.flush()

    def open_terminal(self, input_window, output_window):
        self.terminal_open = True

        ter = terminal.Terminal()

        t = Thread(target=self.read_to_output, args=[ter, output_window])
        t.start()

        while True:
            ter.write(input_window, "> ")

            result = ter.read(input_window)

            if result.equals(terminal.CTRL_D):
                self.terminal_open = False
                t.join()
                break
            if result.equals(terminal.RESIZE):
                ter.write(output_window, self.output)
                continue

            self.write(result.get_line() + "\n")
