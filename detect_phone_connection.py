import uping
host = "" #スマートフォンのIPアドレスを入力

def detect_connection():
    connected = False
    send_num = 2
    timeout = 2.0 #s
    
    rcv = uping.ping(host, count=send_num, timeout=timeout*1000, interval=10, quiet=False, size=64)
    
    if rcv == (send_num,send_num):
        print("スマホ接続")
        connected = True
    else:
        print("スマホ未接続")
    return connected

if __name__ == "__main__":
    detect_connection()

