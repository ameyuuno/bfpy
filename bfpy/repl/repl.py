__all__ = ["Repl", "ReplImpl"]

import abc
import typing as t

from bfpy.core.io.stream import ByteInputStream, ByteOutputStream, BytesBidirectionalStreamOverTextIo
from bfpy.core.machine.machine import Machine, MachineError


class Repl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, reader: t.TextIO, writer: t.TextIO) -> None: ...


class ReplImpl(Repl):
    __PROMPT_INPUT_START = "bfpy> "
    __PROMPT_INPUT_CONTINUATION = "bfpy| "
    __PROMPT_OUTPUT_END = "\n"

    __COMMAND_QUIT = "\\q"

    def __init__(self, machine: Machine) -> None:
        self.__machine = machine

    def run(self, reader: t.TextIO, writer: t.TextIO) -> None:
        input_stream = BytesBidirectionalStreamOverTextIo(reader)
        output_stream = BytesBidirectionalStreamOverTextIo(writer)

        while True:
            code = self.__read(reader, writer)
            if self.__is_quit(code):
                return

            result = self.__evaluate(input_stream, output_stream, code)

            self.__print(writer, result)

    def __read(self, reader: t.TextIO, writer: t.TextIO) -> t.Text:
        code_buffer: t.List[t.Text] = []

        should_read_line = True
        prompt = self.__PROMPT_INPUT_START
        while should_read_line:
            writer.write(prompt)
            prompt = self.__PROMPT_INPUT_CONTINUATION

            line = reader.readline().strip()

            should_read_line = len(line) > 0 and line[-1] == '\\'
            cleaned_line = line[:-1] if should_read_line else line

            code_buffer.append(cleaned_line)

        return "".join(code_buffer)

    def __evaluate(self, input_stream: ByteInputStream, output_stream: ByteOutputStream, code: t.Text) -> t.Text:
        try:
            self.__machine.execute(input_stream, output_stream, code)

        except MachineError as error:
            return str(error)

        return ""

    def __print(self, writer: t.TextIO, result: t.Text) -> None:
        writer.write(result)
        writer.write(self.__PROMPT_OUTPUT_END)

    def __is_quit(self, text: t.Text) -> bool:
        return text == self.__COMMAND_QUIT
