import logging
import multiprocessing
import os.path
from concurrent.futures import ThreadPoolExecutor

from generator.const import (
    ID_ALPHABET,
    MAX_VALUE_FILEPATH,
    MAX_ID_ALPHABET_LEN,
)


logger = logging.getLogger(__name__)

# shared memory - this shared object is thread-safe throw all threads, processes
# for more read: https://docs.python.org/3/library/multiprocessing.html#managers
last_generate_id = multiprocessing.Manager().dict()  # keys last value integer & human readtable
# A non-recursive lock object. Once a process or thread has acquired a lock, subsequent attempts 
# to acquire it from any process or thread will block until it is released.
# for more read: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Lock
last_generate_id_lock = multiprocessing.Lock()


def convert_decimal_to_characters_system(value):
    """
    Function that convert decimal value to characters system via alphabet defined in constants - ID_ALPHABET.
    """
    start_value = value
    return_val = []
    characters_system_len = len(ID_ALPHABET)
    while value > 0:
        odds = value % characters_system_len
        return_val.insert(0, ID_ALPHABET[odds])
        value = value // characters_system_len

    return_val = "".join(return_val)
    if MAX_ID_ALPHABET_LEN > len(return_val):
        return_val = "".join([ID_ALPHABET[0]]*(MAX_ID_ALPHABET_LEN - len(return_val))) + return_val

    logger.debug(f"Value ({start_value}) converted to characters system is {return_val}")
    return return_val


def __get_init_value():
    """
    Get initial value. If it's first run return 0000000 value.
    If the generator was called more then once it takes latest generated value.
    """
    if not os.path.exists(MAX_VALUE_FILEPATH):
        logger.warning("The system didn't found file with max value. System set counter to 0.")
        return int(ID_ALPHABET[0])
    with open(MAX_VALUE_FILEPATH) as f_read:
        line = f_read.readline()
    return int(line)


def __set_init_value(val_int):
    """
    Save current generated maximum value to avoid issues if the system will be
    terminated and raised again (avoiding duplicates).
    """
    line = f"{val_int}"
    with open(MAX_VALUE_FILEPATH, "w+") as f_overwrite:
        logger.debug(f"The system set current max value ({line}) to file")
        f_overwrite.seek(0)
        f_overwrite.write(line)
        f_overwrite.truncate()


def init():
    """
    Function that init the system - especially for first run - get initial value
    """
    with last_generate_id_lock:
        if not last_generate_id:
            val_int = __get_init_value()
            val_human = convert_decimal_to_characters_system(val_int)
            last_generate_id['max_val_int'] = val_int
            last_generate_id['max_val_human'] = val_human
            logger.debug(f"The system on init mode set max value to ({val_int}, {val_human})")


def __base_generate(count=1):
    """
    Base function to generate scope of IDs.
    """
    start_point = None
    end_point = None
    with last_generate_id_lock:
        start_point = last_generate_id['max_val_int'] + 1
        end_point = last_generate_id['max_val_int'] + count
        last_generate_id['max_val_int'] = end_point
        __set_init_value(end_point)
        return start_point, end_point


def generate():
    """
    Function that generate ID by given alphabet (that is defined in constants module)
    """
    _, end_point = __base_generate()
    human_id = convert_decimal_to_characters_system(end_point)
    return human_id


def generate_bulk(count):
    """
    Function that generate a bunch of IDs by given alphabet (that is defined in constants module)
    """
    start_point, end_point = __base_generate(count)
    return [convert_decimal_to_characters_system(item) for item in range(start_point, end_point+1)]


init()
