import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler('fabiano.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('Start reading database')
# read database here
records = {'john': 55, 'tom': 66}
logger.info('Records: %s', records)
logger.info('Updating records ...')
# update records here
logger.info('Finish updating records')
