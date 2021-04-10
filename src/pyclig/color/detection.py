"""
Disable color if your program is not in a terminal or the user requested it.

These things should disable colors:

stdout or stderr is not an interactive terminal (a TTY). It’s best to individually check—if you’re piping stdout to another program, it’s still useful to get colors on stderr.
The NO_COLOR environment variable is set.
The TERM environment variable has the value dumb.
The user passes the option --no-color.
You may also want to add a MYAPP_NO_COLOR environment variable in case users want to disable color specifically for your program.
Further reading: no-color.org, 12 Factor CLI Apps
"""

from dataclasses import dataclass
from os import getenv, stderr, stdout
from typing import Tuple


@dataclass
class ColorDetectionCriteria:
    messaging_is_tty: bool = False
    output_is_tty: bool = False
    no_color_env: bool = False
    terminal_is_dumb: bool = False
    no_color_flag: bool = False
    pyclig_no_color_env_set: bool = False

    def is_messaging_color_enabled(self) -> bool:
        if not self.messaging_is_tty:
            return False
        return self._is_metadata_enabled()

    def is_output_color_enabled(self) -> bool:
        if not self.output_is_tty:
            return False
        return self._is_metadata_enabled()

    def _is_metadata_enabled(self) -> bool:
        if self.no_color_flag:
            return False

        if self.no_color_env or self.pyclig_no_color_env_set:
            return False

        if self.terminal_is_dumb:
            return False

        return True


@dataclass
class ColorDetectionResult:
    criteria: ColorDetectionCriteria
    enable_output_color: bool = True
    enable_messaging_color: bool = True


class ColorDetection:
    _user_flag_no_color_set: bool = False

    def __init__(self, disable_color: bool = False):
        self._user_flag_no_color_set = disable_color

    def evaluate(self) -> ColorDetectionResult:
        """Disable color if your program is not in a terminal or the user requested it.

        These things should disable colors:

          * stdout or stderr is not an interactive terminal (a TTY). It’s best to individually check—if you’re piping stdout to another program, it’s still useful to get colors on stderr.
          * The NO_COLOR environment variable is set.
          * The TERM environment variable has the value dumb.
          * The user passes the option --no-color.
          * You may also want to add a MYAPP_NO_COLOR environment variable in case users want to disable color specifically for your program.

          Further reading: no-color.org, 12 Factor CLI Apps
        """
        evaluation = ColorDetectionCriteria(
            messaging_is_tty=self._is_stderr_tty(),
            output_is_tty=self._is_stdout_tty(),
            no_color_env=self._is_no_color_env_var_set(),
            terminal_is_dumb=self._is_terminal_dumb(),
            no_color_flag=self._user_flag_no_color_set,
            pyclig_no_color_env_set=self._is_pyclig_no_color_env_var_set(),
        )
        return ColorDetectionResult(
            enable_messaging_color=evaluation.is_messaging_color_enabled(),
            enable_output_color=evaluation.is_output_color_enabled(),
            criteria=evaluation,
        )

    @staticmethod
    def _is_no_color_env_var_set() -> bool:
        value = getenv("NO_COLOR")
        if value is None or value.lower() in ["no", "false"]:
            return False
        return True

    @staticmethod
    def _is_pyclig_no_color_env_var_set() -> bool:
        value = getenv("PYCLIG_NO_COLOR")
        if value is None or value.lower() in ["no", "false"]:
            return False
        return True

    @staticmethod
    def _is_terminal_dumb() -> bool:
        value = getenv("TERM")
        if value is None or value.lower() != "dumb":
            return False
        return True

    @staticmethod
    def _is_stdout_tty() -> bool:
        return stdout.is_tty()

    @staticmethod
    def _is_stderr_tty() -> bool:
        return stderr.is_tty()
