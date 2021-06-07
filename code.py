from tkinter import *
import tkinter.font
import gspread
import urllib.request
import requests
import json
import random
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from urllib.request import urlopen
from pyifttt.webhook import send_notification
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT,initial=GPIO.HIGH)

def monitor():
    #create a worksheet
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = {"type": "service_account",
        "project_id": "ecstatic-bounty-315822",
        "private_key_id": "d6991d3e9fb1d7276675ec853c3e0b11a8146025",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC7y2QwH/lpY3OX\nhJ5zKBN51+ziBa31taFX2SaOoyizjfIA/USSi5jd+1pPmFE76fLuTmRBU55MMLhK\nP9KoV8IC/mECUQfrgRWlf54WDPu08a8iE3N9Wg+uQEHdERHGHEsPa2ViYWU4Uy2V\nMiJQTTiAVWPcAo7+t4Us6f4/dtDYsX+eP6iAz7+pHBD+CFraJ+ntnWniyO3ZihHK\nT7d7dnaaY6hJFXGr2a9/9LAD5//PczUQaCaTVXZa8aZiLzUtkervH9JAMDCWBINw\n5E+FWEQPjadEQ+D+aEDLjAWBhBIff/jCFnCZBn1SR7HOfMfZj+hyEK7qYAce2GpC\nQupspnDdAgMBAAECggEALssNWdh9wz7erKCFAti3kaK2CdO0dwcc/tDDBMOu/p6d\n8JUrIwDZxGY/KJohk7ZFrA+od4aoaP+yy/1/Nic31psf/P3H5Wyywhw8fe4aQgn+\nw5TpMBDi215ziuwX669dHKh8CLmQCSrgrs5hMnUrYP7l9QpGKz37VyevDI1EmNmk\nSOFp5dXzx4SwaArkjwwOMZsiTh6LUKgL0AiXO1O0GbCQ18tkRPE4GAkSVi22iq18\nmxOBaf4fbIlWxoK4CzhQgkJUzPww76GHvY9K05xnPAjUWUCBZTSLq+bQCNB+SyC4\n9djFTjWk1NEo6L2QAOKiTn0+S7FanBpZ8T1C+t/nwQKBgQDinLhjve6gWf8tkVuX\nD3ZMI9a7iZnFToJPox/Q5CwCyB7vNtxfcl8kOP20kwfRhiCRkbyzoRHw5z2pr45t\nKxPkzj4fjpCsh0ENqdz+5VRtURrJmQ4j5lIzpmVwMKF03SX+xIELUT+tQ06M4VNw\n9l3Ap+Y3Ep7dVQSNLGACwv2upQKBgQDUJfc4GzQ++/TZ8b/ZfT3PHL9gioVjkAaH\nPSjTj5Aw9EbApy3QeKnnF2ozKuTvarayyVH9gS31l69LfbYn05UCm53lPwLYLnRV\nh3WMFpL0HXrK0vvhsB6Q0nbhUoHfM4Fi49C6u/UK5sdD77mdpRs3qxIIFbbX3uHI\npkfsBMob2QKBgBQSh66mCzX+4sB5iKBXyUWzQvj3ljxI2PgO3emV3GQer8bGmDyI\nF+9QcQCGqYGgnM/oFcvfb4RkJy0ZlMcMssVok04eRahSjquUKTQWwiSws2u59+us\nIgnbKk8Gr7Z3RD9NzpRfDQHe3V1TNB3kZKeE97pXFuVJ+445qQN1nBzVAoGAZH3n\ncUhRo1QuU97UBe3xjV4MuWpkbRkYPo+V+0ESCF5t9Ww7o3jE4paQ09QJxe9Cw8Xh\ndLfwUVmcy6Gs24i6GRYl4SXL7yNyL+GOqOE4kzIzrEfs0KdgkzFe5rTymAwJyhIo\nGYxXMubGlUPFJQvErMX4MKQ4jGEjiqxZfU93fWECgYAzORIdrSYs4sRq9Igx6n4o\njXSGFGLs8MUfdrcdEKLZxDq+VYpMxVALZS4dVLoLC4CRmIN7/MDv/L/uIS+crHRz\nLzZEvYYarJh3mBkVF9oRc1WYdrIyi00+QgCpZ/jCHRwc0yEYXSuOaPCp/cVMa2K0\nD0+9DvHqJKU6Wj8vzXQCkA==\n-----END PRIVATE KEY-----\n",
        "client_email": "history@ecstatic-bounty-315822.iam.gserviceaccount.com",
        "client_id": "101884783431170385704",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/history%40ecstatic-bounty-315822.iam.gserviceaccount.com"}
    client = gspread.service_account_from_dict(credentials)
    sh = client.open("history")
    a = datetime.datetime.now()
    b = a.strftime("%b")
    c = a.strftime("%d")
    d = str(b) + ' ' +str(c)
    sheet1 = sh.add_worksheet(title=d, rows="100", cols="20")
    #insert title columns 
    row = ["power on","power off",0]
    sheet1.insert_row(row)


    #read monitor signal from thingspeak
    READ_API_KEY='ASB4N9AKSICHYV5O'
    CHANNEL_ID='1406818 '
    m = urlopen("https://api.thingspeak.com/channels/1406818/feeds.json?results=2".format(CHANNEL_ID,READ_API_KEY))
    response = m.read()
    data1=json.loads(response.decode('utf-8'))
    print(data1)
    print (data1["feeds"][1]["field1"])
    r=data1["feeds"][1]["field1"]
    print(r)
    k = str(r)
    READ_API_KEY='HY230ZM8I3ES0II2'
    CHANNEL_ID='1404639'
    
    y = None
    x = None

    #check monitor signal on or off and start monitoring 
    while k=="1":
        TS = urlopen("https://api.thingspeak.com/channels/1404639/feeds.json?api_key=HY230ZM8I3ES0II2&results=2".format(CHANNEL_ID,READ_API_KEY))
        response = TS.read()
        data=json.loads(response.decode('utf-8'))
        print(data)
        print (data["feeds"][1]["field1"])
        #read temperature from thingspeak 
        TEMPERATURE=data["feeds"][1]["field1"]
        print(TEMPERATURE)
        K = TEMPERATURE
        
        #convert current time to seconds
        e = datetime.datetime.now()
        hours = int(e.strftime("%H"))*3600
        minutes = int(e.strftime("%M"))*60
        f = int(e.strftime("%S"))
        seconds = hours+minutes+f
        print(seconds)
        
            #if temperature is less than 18 and power on switch off power
        if float(K) == 22:
            x = datetime.datetime.now()#store power on time and date
            print(x)
            GPIO.output(4,0)
            

        #if time is between 2pm and 4pm power off
        elif seconds>=7200 and seconds<=14400:
            GPIO.output(4, 0)
            

        #if temperature>27 and power offf power on
        elif float(K) >= 25:
            y = datetime.datetime.now()#store power off time and date
            print(y)
            GPIO.output(4, 1)
            pass
        if x!=None and y!=None:
            hours = int(x.strftime("%H"))*3600
            minutes = int(x.strftime("%M"))*60
            seconds = int(x.strftime("%S"))
            z1 = hours+minutes+seconds
            hours = int(y.strftime("%H"))*3600
            minutes = int(y.strftime("%M"))*60
            seconds = int(y.strftime("%S"))
            z2 = hours+minutes+seconds
            z = z2-z1
            print(z)
            #insert row of power on time power off time and total consumption in seconds
            row = [str(x),str(y),str(z)] 
            sheet1.insert_row(row)
            sheet1.get()
            
        #else do nothing
        else:
            pass
        #resume montitoring after 10 minutes
        time.sleep(600)
        
    TS.close()

#convert seconds to time format
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)        
    
def ifttt():
#access google sheet
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = {
        "type": "service_account",
        "project_id": "ecstatic-bounty-315822",
        "private_key_id": "d6991d3e9fb1d7276675ec853c3e0b11a8146025",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC7y2QwH/lpY3OX\nhJ5zKBN51+ziBa31taFX2SaOoyizjfIA/USSi5jd+1pPmFE76fLuTmRBU55MMLhK\nP9KoV8IC/mECUQfrgRWlf54WDPu08a8iE3N9Wg+uQEHdERHGHEsPa2ViYWU4Uy2V\nMiJQTTiAVWPcAo7+t4Us6f4/dtDYsX+eP6iAz7+pHBD+CFraJ+ntnWniyO3ZihHK\nT7d7dnaaY6hJFXGr2a9/9LAD5//PczUQaCaTVXZa8aZiLzUtkervH9JAMDCWBINw\n5E+FWEQPjadEQ+D+aEDLjAWBhBIff/jCFnCZBn1SR7HOfMfZj+hyEK7qYAce2GpC\nQupspnDdAgMBAAECggEALssNWdh9wz7erKCFAti3kaK2CdO0dwcc/tDDBMOu/p6d\n8JUrIwDZxGY/KJohk7ZFrA+od4aoaP+yy/1/Nic31psf/P3H5Wyywhw8fe4aQgn+\nw5TpMBDi215ziuwX669dHKh8CLmQCSrgrs5hMnUrYP7l9QpGKz37VyevDI1EmNmk\nSOFp5dXzx4SwaArkjwwOMZsiTh6LUKgL0AiXO1O0GbCQ18tkRPE4GAkSVi22iq18\nmxOBaf4fbIlWxoK4CzhQgkJUzPww76GHvY9K05xnPAjUWUCBZTSLq+bQCNB+SyC4\n9djFTjWk1NEo6L2QAOKiTn0+S7FanBpZ8T1C+t/nwQKBgQDinLhjve6gWf8tkVuX\nD3ZMI9a7iZnFToJPox/Q5CwCyB7vNtxfcl8kOP20kwfRhiCRkbyzoRHw5z2pr45t\nKxPkzj4fjpCsh0ENqdz+5VRtURrJmQ4j5lIzpmVwMKF03SX+xIELUT+tQ06M4VNw\n9l3Ap+Y3Ep7dVQSNLGACwv2upQKBgQDUJfc4GzQ++/TZ8b/ZfT3PHL9gioVjkAaH\nPSjTj5Aw9EbApy3QeKnnF2ozKuTvarayyVH9gS31l69LfbYn05UCm53lPwLYLnRV\nh3WMFpL0HXrK0vvhsB6Q0nbhUoHfM4Fi49C6u/UK5sdD77mdpRs3qxIIFbbX3uHI\npkfsBMob2QKBgBQSh66mCzX+4sB5iKBXyUWzQvj3ljxI2PgO3emV3GQer8bGmDyI\nF+9QcQCGqYGgnM/oFcvfb4RkJy0ZlMcMssVok04eRahSjquUKTQWwiSws2u59+us\nIgnbKk8Gr7Z3RD9NzpRfDQHe3V1TNB3kZKeE97pXFuVJ+445qQN1nBzVAoGAZH3n\ncUhRo1QuU97UBe3xjV4MuWpkbRkYPo+V+0ESCF5t9Ww7o3jE4paQ09QJxe9Cw8Xh\ndLfwUVmcy6Gs24i6GRYl4SXL7yNyL+GOqOE4kzIzrEfs0KdgkzFe5rTymAwJyhIo\nGYxXMubGlUPFJQvErMX4MKQ4jGEjiqxZfU93fWECgYAzORIdrSYs4sRq9Igx6n4o\njXSGFGLs8MUfdrcdEKLZxDq+VYpMxVALZS4dVLoLC4CRmIN7/MDv/L/uIS+crHRz\nLzZEvYYarJh3mBkVF9oRc1WYdrIyi00+QgCpZ/jCHRwc0yEYXSuOaPCp/cVMa2K0\nD0+9DvHqJKU6Wj8vzXQCkA==\n-----END PRIVATE KEY-----\n",
        "client_email": "history@ecstatic-bounty-315822.iam.gserviceaccount.com",
        "client_id": "101884783431170385704",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/history%40ecstatic-bounty-315822.iam.gserviceaccount.com"}

    client = gspread.service_account_from_dict(credentials)
    sh = client.open("history")
    sheet1 = sh.get_worksheet(0)
    #get all powerconsumption sessions duration in a list
    klist = sheet1.col_values(3)
    seconds = sum(klist)
    print(seconds)
    #convert seconds to time
    duration = convert(seconds)
    #send duration of whole session to ifttt event webhook
    p = str(duration)
    data = dict(value1=p)
    key = "nyKzze-xGwVACg8i-Q8HU"
    send_notification("ifttt", data, key)#send notification

def thingspeak_post():
    #setting monitor signal on 
    val=1
    #send monitor signal to thingspeak
    data=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=ASB4N9AKSICHYV5O&field1="+str(val))
    print(data)
    time.sleep(2)
    #start monitoring
    monitor()
    
def thingspeak_post1():
    #setting monitor signal off
    val=0
    #send monitor signal to thingspeak
    data=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=ASB4N9AKSICHYV5O&field1="+str(val))
    print(data)
    #end session and send ifttt notification
    ifttt()
    
def close():
    win.destroy()
#creating gui
win = Tk()
win.title("Monitor")
myFont = tkinter.font.Font(family = 'Helvetica',size = 12,weight="bold")
ledButton = Button(win, text='START MONITORING', font=myFont, command=thingspeak_post, bg='bisque2', height=1, width=24)
ledButton.grid(row=2,column=6)
ledButton1 = Button(win, text='STOP MONITORING', font=myFont, command=thingspeak_post1, bg='bisque2', height=1, width=24)
ledButton1.grid(row=4,column=6)                     
win.protocol("WM_DELETE_WINDOW", close) 
win.mainloop()
