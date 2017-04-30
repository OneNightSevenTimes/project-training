from config import settings
from src import client


def run():
    if settings.Mode == 'AGENT':
        obj = client.Agentclient()
    elif settings.Mode == 'SSH':
        obj = client.Sshclient()
    elif settings.Mode == 'SALT':
        obj = client.Saltclient()
    else:
        raise Exception('模式选择错误')
    obj.process()
