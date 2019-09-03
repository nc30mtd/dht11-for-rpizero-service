# coding: UTF-8
# RaspberryPiでDHT11センサーから温湿度データを取得

import time
import dht11
import RPi.GPIO as GPIO
import datetime
import urllib.request
import json
import socket

#定義
#GPIO 14 as DHT11 data pin
Temp_sensor=14

SERVER_ADDRESS = "http://192.168.0.120/setdata.php"

#温湿度データ取得
def get_temp():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    instance = dht11.DHT11(pin=Temp_sensor)

    while True:
        #データ取得
        result = instance.read()
        return result.temperature,result.humidity

def postdata2server(dataobj):
    url = SERVER_ADDRESS
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    
    # PythonオブジェクトをJSONに変換する
    json_data = json.dumps(dataobj).encode("utf-8")

    response_body = ''
    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")

    return response_body

if __name__ == '__main__':
    
    try:
        while True:
	    #日付
            #dateStr = ''
            date = datetime.datetime.now()
            dateStr = date.strftime('%Y-%m-%d %H:%M:%S')
            
            
            #温湿度データ取得
            temperature,humidity = get_temp()

            #画面出力
            if temperature == 0:
                continue
            json_data = {}
            json_data['Temperature'] = temperature
            json_data['Humidity'] = humidity
            host = socket.gethostname()
            ip = socket.gethostbyname(host)
            json_data['Hostname'] = host
            json_data['IPAddress'] = ip
            json_data['Date'] = dateStr

            response_body = postdata2server(json_data)
            
            print(dateStr ,"Temperature = ",temperature,"C"," Humidity = ",humidity,"%")
            print(response_body)

            #指定された秒数スリープ
            time.sleep(60)

    except:
        import traceback
        traceback.print_exc()
        pass

