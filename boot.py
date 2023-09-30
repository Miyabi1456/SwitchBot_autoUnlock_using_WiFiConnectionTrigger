import time
import ntp
import wifi
import detect_phone_connection
import switchbot

interval_time = 2.0 #sec スマホの接続確認をする時間間隔

def main():
    in_area = True #帰宅/外出状態を保持する
    wifi.do_connect() #マイコンを自宅WiFiに接続
    ntp.set_ntptime() #時計合わせ
    
    while True:
        connected = detect_phone_connection.detect_connection() #スマホへpingを送信してWiFi接続状態の確認
    
        if connected and not in_area: #外出→帰宅したときのみ解錠する
            switchbot.unlock()
        
        #帰宅/外出状態の更新
        if connected:
            in_area = True
        else:
            in_area = False
        
        time.sleep(interval_time)
    

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(10.0)
