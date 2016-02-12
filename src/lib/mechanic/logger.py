import sys
import logging
import os

from mechanic import env

name = 'Mechanic'
formatting = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatting)

logger = logging.getLogger(name)
logger.setLevel(getattr(logging, env.log_level.upper(), logging.DEBUG))

# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(formatter)
# logger.addHandler(handler)

if env.environment == 'development':
    current_dir = os.path.dirname(__file__)
    tmp_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'tmp'))
    log_dir = os.path.join(tmp_dir, 'logs')
    log_path = os.path.join(log_dir, "{}.log".format(env.environment))

    try:
        os.makedirs(log_dir)
    except OSError:
        pass

    fileHandler = logging.FileHandler(log_path)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

debug    = logger.debug
info     = logger.info
warn     = logger.warn
error    = logger.error
critical = logger.critical

debug('--- Booting')
info('Logger set to level %s', logging.getLevelName(logger.level))
