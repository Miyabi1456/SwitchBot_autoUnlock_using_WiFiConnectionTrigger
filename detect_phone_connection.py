import uping
host = "" #スマートフォンのIPアドレスを入力

def detect_connection():
    connected = False
    timeout = 2.0 #s
    
    send, rcv = uping.ping(host, count=5, timeout=timeout*1000, interval=10, quiet=False, size=64)
    
    if rcv > 0: # 1つでも届けば接続状態とする
        print("スマホ接続")
        connected = True
    else:
        print("スマホ未接続")
    return connected

if __name__ == "__main__":
    detect_connection()

