import os
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from engine.ColorizedStreamHandler import ColorizedStreamHandler
import engine.Dump as Dump

# 日志级别
NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
WARNING = logging.WARNING
ERROR = logging.ERROR
FATAL = logging.FATAL
CRITICAL = logging.CRITICAL

# 日志忽略项
logging._srcfile = None
logging.logThreads = 0
logging.logMultiprocessing = 0
logging.logProcesses = 0

CommonFormatter = logging.Formatter(" - ".join(["%(asctime)s", "%(name)s", "%(levelname)s", "%(message)s"]))
LoggerPath = ""
CreatedModules = set()


class CommonLogger(logging.Logger):
	"""通用日志"""

	def LogLastExcept(self, exc_info=None) -> None:
		if exc_info:
			trace_info = "".join(traceback.format_exception(*exc_info))
		else:
			trace_info = traceback.format_exc()

		try:
			trace_var = Dump.RecordVar(exc_info)
		except Exception:
			trace_var = ""

		self.critical("\n".join([trace_info, trace_var]))
		Dump.SaveDump(trace_info, trace_var)


class CommonLoggerAdapter(logging.LoggerAdapter):
	"""玩家日志适配器"""

	def __init__(self, logger: CommonLogger, extra: dict, extra_string: str):
		super().__init__(logger, extra)
		formatter = logging.Formatter(" - ".join(["%(asctime)s", "%(name)s", "%(levelname)s", extra_string, "%(message)s"]))
		for handler in logger.handlers:
			handler.setFormatter(formatter)

	def LogLastExcept(self, exc_info=None) -> None:
		self.logger.LogLastExcept(exc_info)


def SetLoggerPath(log_path: str) -> None:
	global LoggerPath
	LoggerPath = log_path


def GetLogger(module_name: str = None, log_level: int = DEBUG) -> CommonLogger:
	global CreatedModules
	if module_name in CreatedModules:
		return logging.getLogger(module_name)

	logger = logging.getLogger(module_name)
	logger.setLevel(log_level)
	for handler in (TimedRotatingFileHandler(os.path.join(LoggerPath, f"{module_name}.log"), when="D", backupCount=7, delay=True), ColorizedStreamHandler()):
		handler.setLevel(log_level)
		handler.setFormatter(CommonFormatter)
		logger.addHandler(handler)
	CreatedModules.add(module_name)
	return logger


logging.setLoggerClass(CommonLogger)
