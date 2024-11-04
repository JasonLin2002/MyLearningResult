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

# 指定第一個EXE檔案路徑
exe_path1 = r'C:\Users\jk121\Desktop\点我启动.exe.lnk'
# 執行第一個EXE檔案
subprocess.Popen(exe_path1)

# 延遲7秒
time.sleep(7)

# 指定第二個EXE檔案路徑
exe_path2 = r'C:\Users\jk121\Desktop\《Apex 英雄》.url'

# 執行第二個EXE檔案
subprocess.Popen(exe_path2)