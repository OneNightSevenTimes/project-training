from config import settings
import importlib
def server_info(hostname=None):
    ret = {}
    for k,v in settings.PLUGINS_ITEMS.items():
        file_path,class_name = v.rsplit('.',1)
        m = importlib.import_module(file_path)
        cls = getattr(m,class_name)
        obj = cls(hostname)
        info = obj.execute()
        ret[k] = info.__dict__

    return ret
if __name__ == '__main__':
    server_info()