import logging

logging.basicConfig(
    filename= 'app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug('this is a debug message')
logging.info('this is a info message')
logging.warning('this is a warning message')
logging.error('this is a error message')
logging.critical('this is a critical message')

try:
    value= int(input("enter a number"))
    print(10/value)
except ValueError:
    print("please enter a valid integer")
except ZeroDivisionError:
    print("cannot divide by zero")
finally:
    print("execution finished")