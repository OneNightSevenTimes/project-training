import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#采集资产的方式 AGENT,SALT,SSH
Mode = 'AGENT'

#是否是测试模式
TEST_MODE = True

#采集硬件数据的插件
PLUGINS_ITEMS = {
    'disk':'src.plugins.disk.Diskplugin',
    'nic':'src.plugins.nic.Nicplugin',
    'mem':'src.plugins.mem.Memplugin'
}

API = "http://127.0.0.1:8000/post_info/"
