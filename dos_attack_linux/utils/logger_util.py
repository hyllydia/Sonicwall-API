import logging

def get_logger(logger_name, file_name):
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.FileHandler(file_name, mode='w')
    fh.setLevel(logging.DEBUG)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # define formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')

    # add formatter to handler
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

if __name__ == "__main__":
    get_logger('tcp_flood_logger', "tcp_flood.log")