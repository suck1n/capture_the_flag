import os
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

        self.process = Popen(self.program, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        os.set_blocking(self.process.stdout.fileno(), False)

        os.chdir(cwd)

        self.running = True

        Thread(target=self.listen, args=[onchange]).start()

    def stop_program(self):
        if not self.running:
            return

        self.process.terminate()
        self.process.wait()
        self.process = None
        self.running = False

    def read_to_output(self, ter, output):
        ter.write(output, self.output)

        while self.running and self.terminal_open:
            value = self.process.stdout.read()
            if value:
                self.output += value.decode().replace("\n", "\n▷ ")
                ter.write(output, self.output)

    def listen(self, onchange=None):
        if not self.running:
            return

        self.process.wait()

        self.running = False

        if not self.terminal_open:
            self.output += "▷ " + "\n▷ ".join([b.decode() for b in self.process.stdout.readlines()])
            self.output += "\nexit return code: " + str(self.process.returncode)

            if type(onchange) == "function":
                onchange()

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
