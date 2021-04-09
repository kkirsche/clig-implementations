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

from os import getenv
from dataclasses import dataclass

@dataclass
class ColorDetectionCriteria:
  messaging_is_tty: bool
  output_is_tty: bool
  no_color_env: bool
  terminal_is_dumb: bool
  no_color_flag: bool
  pyclig_no_color_env_set: bool

  def is_messaging_color_enabled(self) -> bool:
    if not self.messaging_is_tty:
      return False
    return self._is_metadata_enabled()

  def is_output_color_enabled(self) -> bool:
    if not self.output_is_tty:
      return False
    return self._is_metadata_enabled()
  
  def _is_metadata_enabled(self) -> bool:
    return all(
      !self.no_color_env,
      !self.pyclig_no_color_env_set,
      !self.terminal_is_dumb,
      !self.no_color_flag
    )
  

@dataclass
class ColorDetectionResult:
  enable_output_color: bool = True
  enable_messaging_color: bool = True
  criteria: ColorDetectionCriteria

class ColorDetection:
    _user_flag_no_color_set: bool = False

    def __init__(self, disable_color: bool = False):
      self._user_flag_no_color_set  = disable_color

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
        no_color_flag=self._user_flag_no_color_set
        pyclig_no_color_env_set=self._is_pyclig_no_color_env_var_set()
      )
      return ColorDetectionResult(
        enable_messaging_color=evaluation.is_messaging_color_enabled(),
        enable_output_color=evaluation.is_output_color_enabled(),
        criteria=evaluation
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

    def _is_tty(self) -> Tuple[bool, bool]
      return (self._is_stdout_tty(), self._is_stderr_tty())

    @staticmethod
    def _is_stdout_tty() -> bool:
        return stdout.is_tty()
    
    @staticmethod
    def _is_stderr_tty() -> bool:
      return stderr.is_tty()