import logging


def left_pad(string, length, pad_char=" "):
    if len(string) >= length:
        return string
    else:
        padding = pad_char * (length - len(string))
        return padding + string


def run_chain(funcs):
    if len(funcs) == 0:
        return
    remaining = funcs[1:]
    func = funcs[0]

    def next():
        run_chain(remaining)

    func(next)


logger = None


def log(message):
    global logger

    if logger is None:
        logger = logging.getLogger("ipylivebash")
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler("debug.log")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    logger.debug(message)
