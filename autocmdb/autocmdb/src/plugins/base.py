from config import settings
class Baseplugin(object):
    '''
    execute约束
    cmd公共方法
    '''
    def __init__(self,host=None):
        self.hostname = host
        self.test_mode = settings.TEST_MODE

    def execute(self):
        #判断系统是windows还是linux
        return self.linux()
    def linux(self):
        raise Exception('插件必须实现linux方法')
    def windows(self):
        raise Exception('插件必须实现windows方法')
    def cmd(self,c):
        '''
        判断当前采集资产用的哪种模式
        :param c:
        :return:
        '''
        from config import settings
        if settings.Mode == 'AGENT':
            result = self.agent_cmd(c)
        elif settings.Mode == 'SSH':
            result = self.ssh_cmd(c)
        elif settings.Mode == 'SALT':
            result =self.salt_cmd(c)
        else:
            raise Exception('配置文件中Mode设置错误')
        return result
    def agent_cmd(self,c):
        # import subprocess
        # v = subprocess.getoutput(c)
        v = 'agent'
        return v
    def ssh_cmd(self,c):
        # import paramiko
        #
        # private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
        #
        # # 创建SSH对象
        # ssh = paramiko.SSHClient()
        # # 允许连接不在know_hosts文件中的主机
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # # 连接服务器
        # ssh.connect(hostname=self.hostname, port=22, username='root', password='centos')
        #
        # # 执行命令
        # stdin, stdout, stderr = ssh.exec_command(c)
        # # 获取命令结果
        # result = stdout.read()
        #
        # # 关闭连接
        # ssh.close()
        result = 'ssh'
        return result

    def salt_cmd(self,c):
        # import salt.client
        # local = salt.client.LocalClient()
        # result = local.cmd(self.hostname, 'cmd.run', [c])
        result = 'salt'
        return result