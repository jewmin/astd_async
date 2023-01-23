import os
import sys
import errno
import logging
import colorama
from typing import Callable, Optional, TextIO, Type, cast


class BrokenStdoutLoggingError(Exception):
	'''
	Raised if BrokenPipeError occurs for the stdout stream while logging.
	'''


def _is_broken_pipe_error(exc_class: Type[BaseException], exc: BaseException) -> bool:
	if exc_class is BrokenPipeError:
		return True

	# On Windows, a broken pipe can show up as EINVAL rather than EPIPE:
	# https://bugs.python.org/issue19612
	# https://bugs.python.org/issue30418
	if not WINDOWS:
		return False

	return isinstance(exc, OSError) and exc.errno in (errno.EINVAL, errno.EPIPE)


# windows detection, covers cpython and ironpython
WINDOWS = sys.platform.startswith('win') or (sys.platform == 'cli' and os.name == 'nt')


def _color_wrap(*colors: str) -> Callable[[str], str]:
	def wrapped(inp: str) -> str:
		return ''.join(list(colors) + [inp, colorama.Style.RESET_ALL])

	return wrapped


class ColorizedStreamHandler(logging.StreamHandler):
	'''带颜色的终端日志处理器'''

	# Don't build up a list of colors if we don't have colorama
	if colorama:
		COLORS = [
			# This needs to be in order from the highest logging level to lowest.
			(logging.ERROR, _color_wrap(colorama.Fore.RED)),
			(logging.WARNING, _color_wrap(colorama.Fore.YELLOW)),
			(logging.INFO, _color_wrap(colorama.Fore.GREEN)),
			(logging.DEBUG, _color_wrap(colorama.Fore.CYAN)),
		]
	else:
		COLORS = []

	def __init__(self, stream: Optional[TextIO] = None, no_color: bool = None) -> None:
		super().__init__(stream)
		self._no_color = no_color

		if WINDOWS and colorama:
			self.stream = colorama.AnsiToWin32(self.stream)

	def _using_stdout(self) -> bool:
		'''
		Return whether the handler is using sys.stdout.
		'''
		if WINDOWS and colorama:
			# Then self.stream is an AnsiToWin32 object.
			stream = cast(colorama.AnsiToWin32, self.stream)
			return stream.wrapped is sys.stdout

		return self.stream is sys.stdout

	def should_color(self) -> bool:
		# Don't colorize things if we do not have colorama or if told not to
		if not colorama or self._no_color:
			return False

		real_stream = (
			self.stream
			if not isinstance(self.stream, colorama.AnsiToWin32)
			else self.stream.wrapped
		)

		# If the stream is a tty we should color it
		if hasattr(real_stream, 'isatty') and real_stream.isatty():
			return True

		# If we have an ANSI term we should color it
		if os.environ.get('TERM') == 'ANSI':
			return True

		# If anything else we should not color it
		return False

	def format(self, record: logging.LogRecord) -> str:
		msg = super().format(record)

		if self.should_color():
			for level, color in self.COLORS:
				if record.levelno >= level:
					msg = color(msg)
					break

		return msg

	# The logging module says handleError() can be customized.
	def handleError(self, record: logging.LogRecord) -> None:
		exc_class, exc = sys.exc_info()[:2]
		# If a broken pipe occurred while calling write() or flush() on the
		# stdout stream in logging's Handler.emit(), then raise our special
		# exception, so we can handle it in main() instead of logging the
		# broken pipe error and continuing.
		if exc_class and exc and self._using_stdout() and _is_broken_pipe_error(exc_class, exc):
			raise BrokenStdoutLoggingError()

		return super().handleError(record)
