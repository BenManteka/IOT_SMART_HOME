# intended to manage the FitGuard system
# insert data to FitGuard DB

import paho.mqtt.client as mqtt
import time
import random
from init import *
import data_acq as da
from icecream import ic
from datetime import datetime

def time_format():
    return f'{datetime.now()}  Manager|> '

ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False)  # use True for including script file context file

# Define callback functions
def on_log(client, userdata, level, buf):
    ic("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        ic("connected OK")
    else:
        ic("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    ic("DisConnected result code " + str(rc))

def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    ic("message from: " + topic, m_decode)
    insert_DB(topic, m_decode)

def send_msg(client, topic, message):
    ic("Sending message: " + message)
    client.publish(topic, message)

def client_init(cname):
    r = random.randrange(1, 10000000)
    ID = str(cname + str(r + 21))
    client = mqtt.Client(ID, clean_session=True)  # create new client instance
    # define callback function
    client.on_connect = on_connect  # bind callback function
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.on_message = on_message
    if username != "":
        client.username_pw_set(username, password)
    ic("Connecting to broker ", broker_ip)
    client.connect(broker_ip, int(port))  # connect to broker
    return client

def insert_DB(topic, m_decode):
    # DHT case:
    if 'DHT' in m_decode:
        value = parse_data(m_decode)
        if value != 'NA':
            da.add_IOT_data(m_decode.split('From: ')[1].split(' Temperature: ')[0], da.timestamp(), value)
            # TODO: update IOT device last_updated
    # Elec Meter case:
    elif 'Meter' in m_decode:
        try:
            elec = m_decode.split(' Electricity: ')[1].split(' Sensitivity: ')[0]
            sens = m_decode.split(' Sensitivity: ')[1]
            da.add_IOT_data('ElectricityMeter', da.timestamp(), elec)
            da.add_IOT_data('SensitivityMeter', da.timestamp(), sens)
        except Exception:
            pass

def parse_data(m_decode):
    # 'From: ' + self.name+ ' Temperature: '+str(temp)+' Humidity: '+str(hum)
    try:
        return m_decode.split(' Temperature: ')[1].split(' Humidity: ')[0]
    except Exception:
        return 'NA'

def enable(client, topic, msg):
    ic(topic + ' ' + msg)
    client.publish(topic, msg)

def sound(client, topic, msg):
    ic(topic)
    enable(client, topic, msg)

def actuator(client, topic, msg):
    enable(client, topic, msg)

def check_DB_for_change(client):
    # בדיקת "רעש/עומס" (SensitivityMeter)
    df = da.fetch_data(db_name, 'data', 'SensitivityMeter')
    if len(df.value) != 0:
        try:
            current = float(df.value.iloc[-1])
            if current > sensitivityMax:
                msg = f'[FitGuard] High noise/occupancy level! Current: {current}'
                ic(msg)
                client.publish(comm_topic + 'sound', msg)
        except Exception:
            pass  # ignore parse errors

    # בדיקת צריכת חשמל (ElectricityMeter)
    df = da.fetch_data(db_name, 'data', 'ElectricityMeter')
    if len(df.value) != 0:
        try:
            current = float(df.value.iloc[-1])
            if current > Elec_max:
                msg = f'[FitGuard] High electricity consumption! Current: {current}'
                ic(msg)
                client.publish(comm_topic + 'sound', msg)
        except Exception:
            pass

def check_Data(client):
    try:
        rrows = da.check_changes('iot_devices')
        for row in rrows:
            topic = row[17]
            if row[10] == 'sound':
                msg = 'Set temperature to: ' + str(row[15])
                sound(client, topic, msg)
                da.update_IOT_status(int(row[0]))
            else:
                msg = 'actuated'
                actuator(client, topic, msg)
    except Exception:
        pass

def main():
    cname = "Manager-"
    client = client_init(cname)
    # main monitoring loop
    client.loop_start()  # Start loop
    client.subscribe(comm_topic + '#')
    try:
        while conn_time == 0:
            check_DB_for_change(client)
            time.sleep(conn_time + manag_time)
            check_Data(client)
            time.sleep(3)
        ic("con_time ending")
    except KeyboardInterrupt:
        client.disconnect()  # disconnect from broker
        ic("interrrupted by keyboard")

    client.loop_stop()  # Stop loop
    # end session
    client.disconnect()  # disconnect from broker
    ic("End manager run script")

if __name__ == "__main__":
    main()
