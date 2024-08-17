# import sys
import logging
import logging.handlers
import datetime

# from cloudwatch import cloudwatch
from config import environment

# sys.path.append('..')
# from utils.config import environment, aws_access_key_id, aws_secret_access_key, aws_region


class CustomLoggger:
    def __init__(self, name):
        self.log = logging.getLogger(name)
        self.log.propagate = True
        self.formatter = logging.Formatter("%(asctime)s;[%(levelname)s];%(message)s", "%Y-%m-%d %H:%M:%S")
        """
        https://docs.python.org/ko/3/library/logging.html#logging-levels
        """
        # self.levels = {
        #     "DEBUG" : logging.DEBUG,
        #     "INFO" : logging.INFO,
        #     "WARNING" : logging.WARNING,
        #     "ERROR" : logging.ERROR,
        #     "CRITICAL" : logging.CRITICAL }

    def set_stream_handler(self, level):
        """
        level :
        > "DEBUG" : logging.DEBUG ,
        > "INFO" : logging.INFO ,
        > "WARNING" : logging.WARNING ,
        > "ERROR" : logging.ERROR ,
        > "CRITICAL" : logging.CRITICAL ,
        """
        streamHandler = logging.StreamHandler()
        # streamHandler.setLevel(self.levels[level])
        streamHandler.setLevel(level)
        streamHandler.setFormatter(self.formatter)
        self.log.addHandler(streamHandler)
        return self.log

    def set_file_handler(self, file_name, mode, level):
        """
        file_name : ~.txt / ~.log
        mode : "w" / "a"
        level :
        > "DEBUG" : logging.DEBUG ,
        > "INFO" : logging.INFO ,
        > "WARNING" : logging.WARNING ,
        > "ERROR" : logging.ERROR ,
        > "CRITICAL" : logging.CRITICAL ,
        """
        fileHandler = logging.FileHandler(file_name, mode=mode)
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(self.formatter)
        self.log.addHandler(fileHandler)
        return self.log

    def set_Rotating_filehandler(self, file_name, mode, level, backupCount, log_max_size):
        """
        file_name : ~.txt / ~.log
        mode : "w" / "a"
        backupCount : backup할 파일 개수
        log_max_size : 한 파일당 용량 최대
        level :
        > "DEBUG" : logging.DEBUG ,
        > "INFO" : logging.INFO ,
        > "WARNING" : logging.WARNING ,
        > "ERROR" : logging.ERROR ,
        > "CRITICAL" : logging.CRITICAL ,
        """

        fileHandler = logging.handlers.RotatingFileHandler(filename=file_name, maxBytes=log_max_size, backupCount=backupCount, mode=mode)
        fileHandler.setLevel(level)
        fileHandler.setFormatter(self.formatter)
        self.log.addHandler(fileHandler)
        return self.log

    def set_timeRotate_handler(self, filename='./log.txt', when="M", level="DEBUG", backupCount=4, atTime=datetime.time(0, 0, 0), interval=1):
        """
        file_name :
        when : 저장 주기
        interval : 저장 주기에서 어떤 간격으로 저장할지
        backupCount : 5
        atTime : datetime.time(0, 0, 0)
        """
        fileHandler = logging.handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount, interval=interval, atTime=atTime)  # W0
        fileHandler.setLevel(level)
        fileHandler.setFormatter(self.formatter)
        self.log.addHandler(fileHandler)
        return self.log


def set_logger(group_name):
    custom_logger = CustomLoggger(group_name)
    logger = custom_logger.log
    # logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # today = date.today()
    #   streamHandler = logging.StreamHandler()
    logger = custom_logger.set_stream_handler(logging.DEBUG)
    #   formatter = logging.Formatter(u'%(asctime)s %(levelname)8s %(message)s')

    #   if(environment == "production"):
    #     # account-id: 570872761770
    #     # iam-user: sinho0689@gmail.com
    #     cloudWatchHandler = cloudwatch.CloudwatchHandler(
    #         log_group=group_name,
    #         log_stream=str(datetime.now().date()),
    #         region=aws_region,
    #         access_id=aws_access_key_id,
    #         access_key=aws_secret_access_key
    #     )
    #     cloudWatchHandler.setFormatter(formatter)
    #     logger.addHandler(cloudWatchHandler)

    #   logger.addHandler(streamHandler)

    return logger


if __name__ == "__main__":
    set_logger(environment)
