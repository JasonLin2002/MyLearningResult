import subprocess
import time
import os
import sys
import win32com.shell.shell as shell

ASADMIN = 'asadmin'

if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    sys.exit(0)

# 指定第一個捷徑檔案路徑
lnk_path1 = r'C:\Users\jk121\Desktop\点我启动.exe.lnk'
# 使用 os.startfile 方法模仿雙擊打開第一個捷徑檔案
os.startfile(lnk_path1)

# 延遲7秒
time.sleep(7)

# 指定第二個捷徑檔案路徑
url_path2 = r'C:\Users\jk121\Desktop\《Apex 英雄》.url'

# 使用 os.startfile 方法模仿雙擊打開第二個捷徑檔案
os.startfile(url_path2)
