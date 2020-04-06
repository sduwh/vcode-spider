from logzero import setup_logger, LogFormatter
from config import spider_config

log_format = '%(color)s[%(levelname)s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
formatter = LogFormatter(fmt=log_format)
logger = setup_logger(name="vcode-spider",
                      logfile=spider_config.LOG_FILE,
                      level=spider_config.LOG_LEVEL,
                      maxBytes=1000000000,
                      backupCount=3,
                      formatter=formatter
                      )
