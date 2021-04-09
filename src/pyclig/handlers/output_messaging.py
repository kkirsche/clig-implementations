from typing import Protocol
from logging import StreamHandler, NullHandler, Handler, DEBUG, WARNING
from os import stdout, stderr
from dataclasses import dataclass

from pyclig.filters.info_filter import InfoFilter


def new_output_messaging_handlers(output_level: int = DEBUG, messaging_level: int = WARNING) -> OutputMessagingHandlersResult:
  """This creates new output and messaging handlers.

  From CLIG (https://clig.dev/#the-basics):

  Send output to stdout. The primary output for your command should go to stdout.
  Anything that is machine readable should also go to stdout—this is where piping
  sends things by default.

  Send messaging to stderr. Log messages, errors, and so on should all be sent to
  stderr. This means that when commands are piped together, these messages are
  displayed to the user and not fed into the next command.
  """
  output_handler = StreamHandler(stdout)
  messaging_handler = StreamHandler(stderr)

  output_handler.setLevel(output_level)
  output_handler.addFilter(InfoFilter())

  messaging_handler.setLevel(messaging_level)

  return OutputMessagingHandlersResult(output_handler=output_handler, messaging_handler=messaging_handler)


@dataclass
class NullHandlersResult(OutputMessagingHandlerPair):
  output_handler: NullHandler
  messaging_handler: NullHandler

def new_null_handlers() -> NullHandlersResult:
  return NullHandlersResult(output_handler=NullHandler(), messaging_handle=NullHandler())