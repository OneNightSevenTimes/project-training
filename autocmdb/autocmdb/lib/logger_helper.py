import logging
#
# def error_log(message):
#     file_1_1 = logging.FileHandler('error.log', 'a+', encoding='utf-8')
#     fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
#     file_1_1.setFormatter(fmt)
#     # 创建日志对象
#     logger1 = logging.Logger('error', level=logging.ERROR)
#     # 日志对象和文件对象创建关系
#     logger1.addHandler(file_1_1)
#
#     logger1.log(logging.FATAL,message)
#
# def run_log(message):
#     file_1_1 = logging.FileHandler('run.log', 'a+', encoding='utf-8')
#     fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
#     file_1_1.setFormatter(fmt)
#     # 创建日志对象
#     logger1 = logging.Logger('run', level=logging.ERROR)
#     # 日志对象和文件对象创建关系
#     logger1.addHandler(file_1_1)
#
#     logger1.log(logging.FATAL,message)

class LoggerHelper(object):
    _i = None
    @classmethod
    def instance(cls):
        if cls._i:
            return cls._i
        else:
            cls._i = LoggerHelper()
            return cls._i
    def __init__(self):
        #错误日志
        error_log = logging.FileHandler('error.log', 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
        error_log.setFormatter(fmt)

        # 定义日志
        error_logger = logging.Logger('s1', level=logging.ERROR)
        error_logger.addHandler(error_log)
        self.error_logger = error_logger

        #执行日志
        run_log = logging.FileHandler('run.log', 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
        run_log.setFormatter(fmt)

        # 定义日志
        run_logger = logging.Logger('s1', level=logging.ERROR)
        run_logger.addHandler(error_log)
        self.run_logger = run_logger
if __name__ == '__main__':
    #单例模式，用户获取第一次创建的对象
    a1 = LoggerHelper.instance()
    print(a1)
    a2 = LoggerHelper.instance()
    print(a2)
    a3 = LoggerHelper.instance()
    print(a3)