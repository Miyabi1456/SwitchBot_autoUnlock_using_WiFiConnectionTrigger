import time
import hashlib
import hmac
import base64
import urequests

# トークンとシークレットキーを入力する
token = ""
secret = ""

lock_deviceid = "" #SwitchBotロックのデバイスIDを入力する

host_domain = "https://api.switch-bot.com"
ver = "/v1.1"

def get_auth_header(token, secret):
    nonce = '' #空欄のままで良いらしい
    t = int(round((time.time() + 946684800) * 1000)) #UNIXとESP32のエポック基準時刻を合わせるために+946684800
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, 
    digestmod=hashlib.sha256).digest())
    #print ('Authorization: {}'.format(token))
    #print ('t: {}'.format(t))
    #print ('sign: {}'.format(str(sign, 'utf-8')))
    #print ('nonce: {}'.format(nonce))

    header={}
    header["Authorization"] = token
    header["sign"] = str(sign, 'utf-8')
    header["t"] = str(t)
    header["nonce"] = nonce
    return header

def get_device_list():
    #デバイスの一覧を取得する。APIが正しく操作できるか確認する用
    header = get_auth_header(token, secret)
    response = urequests.get(host_domain + ver + "/devices", headers=header)
    return_json = response.json()
    if return_json["message"] == "success":
        print("取得成功")
        return return_json["body"]
    elif return_json["message"] == "Unauthorized":
        print("認証エラー")
        return None
    else:
        print("エラー")
        return None

def lock():
    header = get_auth_header(token, secret)
    devices_url = host_domain + ver +"/devices/" + lock_deviceid + "/commands"
    data={
            "commandType": "command",
            "command": "lock",
            "parameter": "default",
        }
    try:
        # ロック
        res = urequests.post(devices_url, headers=header, json=data)
        print(res.text)
    except Exception as e:
        print("error:",e)
        
def unlock():
    header = get_auth_header(token, secret)
    devices_url = host_domain + ver +"/devices/" + lock_deviceid + "/commands"
    data={
            "commandType": "command",
            "command": "unlock",
            "parameter": "default",
        }
    try:
        # アンロック
        res = urequests.post(devices_url, headers=header, json=data)
        print(res.text)
    except Exception as e:
        print("error:",e)

def lock_status():
    #ロックとドアの状態を返す
    header = get_auth_header(token, secret)
    lockState, doorState = None, None
    try:
        res = urequests.get(host_domain + ver +"/devices/" + lock_deviceid + "/status",headers=header)
        lockState = res.json()["body"]["lockState"]  #"locked" / "unlocked"
        doorState = res.json()["body"]["doorState"]  # "closed" / "opened"
    except Exception as e:
        print("error:",e)
    return lockState, doorState

def test():
    device_list = get_device_list()
    print(device_list)
    lockState, doorState = lock_status()
    print(f"ロック:{lockState}  ドア{doorState}")
    
    if lockState == "locked":
        unlock()

if __name__ == "__main__":
    test()
