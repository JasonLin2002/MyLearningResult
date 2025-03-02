import machine
from umqtt.robust import MQTTClient
from machine import Pin, PWM, I2C
import network
import time
from ssd1306 import SSD1306_I2C

# 初始化 I2C 與 OLED 顯示
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

# 連線至無線網路
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('TUF-AX3000', 'n9U3Dgn9')

while not sta.isconnected():
    pass

print('Wi-Fi連線成功')

# 初始化 MQTT 客戶端
client = MQTTClient(
    client_id='',                 # 用戶端識別名稱
    server='io.adafruit.com',     # 中介伺服器網址
    #user="MY_USERNAME",              # AIO 帳戶名稱
    #password="MY_PASSWORD",          # AIO 金鑰
)

TOPIC = client.user.encode() + b'/feeds/esp32-deeplearing'  # 訂閱主題

# 連線至 MQTT 伺服器
client.connect()
print('MQTT連線成功')

# 全局變數，用於保存累計的字母
cumulative_results = ""

# 定義處理接收到的 MQTT 資料的回呼函數
def get_cmd(topic, msg):
    global cumulative_results
    try:
        msg = msg.decode()
        print(f"收到訊息: {msg}")

        # 累計顯示結果
        cumulative_results += msg + " "  # 將新的字母加入累計結果
        if len(cumulative_results) > 48:
            cumulative_results = msg + " "


        oled.fill(0)  # 清空顯示
        oled.text("results:", 0, 0)
        oled.text(cumulative_results[:16], 0, 16)  # 第一行
        oled.text(cumulative_results[16:32], 0, 32)  # 第二行
        oled.text(cumulative_results[32:48], 0, 48)  # 第三行
        oled.show()
        time.sleep(1)  # 給使用者足夠時間查看
    except Exception as e:
        print(f"處理訊息時出錯: {e}")

# 設定 MQTT 回呼函數並訂閱主題
client.set_callback(get_cmd)
client.subscribe(TOPIC)
print("已訂閱主題: esp32-deeplearing")

# 初始化 OLED 顯示內容
oled.fill(0)
oled.text("results:", 0, 0)
oled.text("No result", 0, 32)
oled.show()
time.sleep(1)

# 主迴圈
while True:
    try:
        # 確保與伺服器的連線保持活躍
        client.check_msg()
        client.ping()
    except Exception as e:
        print(f"主迴圈出錯: {e}")
        time.sleep(1)