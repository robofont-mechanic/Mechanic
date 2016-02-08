import sys
import logging

from mechanic import env


logger = logging.getLogger('Mechanic')
logger.setLevel(getattr(logging, env.log_level.upper(), logging.DEBUG))

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

formatting = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatting)
handler.setFormatter(formatter)

debug    = logger.debug
info     = logger.info
warn     = logger.warn
error    = logger.error
critical = logger.critical

info('Logger set to level %s', logging.getLevelName(logger.level))
