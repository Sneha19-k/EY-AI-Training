import logging
class invalidMarksError(Exception):
    pass
def check_marks(marks):
    if marks<0 or marks>100:
        raise invalidMarksError("Marks must be between 0 and 100")

try:
    check_marks(120)
except invalidMarksError as e:
    logging.error(e)
    