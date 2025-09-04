import time
from speech import *
import data_acq as da
from init import *
import pandas as pd
from pocketsphinx import LiveSpeech
from icecream import ic as icA
from datetime import datetime
import os.path
from os import path

def time_format():
    return f'{datetime.now()}  Assistant BOT|> '
icA.configureOutput(prefix=time_format)
icA.configureOutput(includeContext=False)  # use True for including script file context file


class BOT():

    def bl(self, pl, st, ts):

        # First greeting
        icA('Hello friend, how can i help you?')
        if path.exists('Hello friend.wav'):
            pl.play('Hello friend.wav')
        else:
            ts.save2file(ts.tts_request('Hello friend, how can I help you?'), ttsfile)
            pl.play(ttsfile)
        time.sleep(sys_delay)
        rep_pl = 0

        while True:
            pl.record(userresponcefile)
            time.sleep(sys_delay)
            try:
                userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
            except:
                userresponcestring = ''
            # make commands case-insensitive
            userresponcestring = userresponcestring.lower()
            icA(userresponcestring)
            time.sleep(sys_delay)

            if len(userresponcestring) == 0:
                icA('Sorry, could you repeat, please?')
                if path.exists('Sorry.wav'):
                    pl.play('Sorry.wav')
                else:
                    ts.save2file(ts.tts_request('Sorry, could you repeat, please?'), ttsfile)
                    pl.play(ttsfile)
                time.sleep(sys_delay)
                rep_pl = rep_pl + 1
                if rep_pl == 3:
                    break
                else:
                    continue

            if 'stop it' in userresponcestring:
                icA('Ok, goodbye my friend')
                if path.exists('Goodbye.wav'):
                    pl.play("Goodbye.wav")
                else:
                    ts.save2file(ts.tts_request('Goodbye my friend'), ttsfile)
                    pl.play(ttsfile)
                time.sleep(sys_delay)
                return

            # ==== GYM STATUS ====
            if "gym status" in userresponcestring:
                # here should be analytics request to manager
                icA('Data request..')
                ts.save2file(ts.tts_request('All systems are in normal state. Would you like to listen to the report?'), ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)

                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring = ''
                userresponcestring = userresponcestring.lower()
                icA(userresponcestring)

                if "yes" in userresponcestring:
                    dfW = da.fetch_data(db_name, 'data', 'SensitivityMeter').value
                    if len(dfW) == 0:
                        W_report = 'currently unavailable'
                    else:
                        W_report = str((pd.to_numeric(dfW, errors='ignore', downcast='float')).mean())

                    dfE = da.fetch_data(db_name, 'data', 'ElectricityMeter').value
                    if len(dfE) == 0:
                        E_report = 'currently unavailable'
                    else:
                        E_report = str((pd.to_numeric(dfE, errors='ignore', downcast='float')).mean())

                    text_msg = (
                        'The current gym state: electricity average consumption is ' + E_report +
                        ' kilowatt per hour and operated under normal condition, '
                        'Sensitivity average value is ' + W_report +
                        ' (noise/occupancy index) and it is usual for the current season'
                    )
                    ts.save2file(ts.tts_request(text_msg), ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)

                    icA('Something else ?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        continue
                    elif 'no' in userresponcestring:
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

                else:
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

            # ==== GYM TEMPERATURE ====
            if "gym temperature" in userresponcestring:
                # analytics request to manager
                icA('Data request..')
                temperature = da.read_IOT_data('data', 'DHT-1')[-1][2]
                textS = 'The gym temperature is ' + temperature + ' degrees Celsius. Would you like to turn on the air conditioner?'
                icA(textS)
                ts.save2file(ts.tts_request(textS), ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)

                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring = ''
                userresponcestring = userresponcestring.lower()
                icA(userresponcestring)

                if 'yes' in userresponcestring:
                    icA('How many degrees Celsius would you like to set?')
                    if path.exists("how_many_celcius.wav"):
                        pl.play("how_many_celcius.wav")
                    else:
                        ts.save2file(ts.tts_request('How many degrees Celsius would you like to set?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    # If STT failed, use default 22
                    if userresponcestring == '':
                        userresponcestring = '22'

                    da.update_IOT_dev((userresponcestring, 'sound'))
                    time.sleep(sys_delay)
                    icA('Data request..')

                    ack = 'The air conditioner is set to ' + str(userresponcestring) + ' degrees Celsius. Something else?'
                    icA(ack)
                    ts.save2file(ts.tts_request(ack), ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

                else:
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

            # ==== POWER CONSUMPTION REPORTS ====
            if "power consumption" in userresponcestring:
                icA('Data request..')
                icA('do you wish to see the daily, weekly or monthly power consumption report ?')
                if path.exists('Do you wish.wav'):
                    pl.play('Do you wish.wav')
                else:
                    ts.save2file(ts.tts_request('Do you wish to see the daily, weekly or monthly power consumption report?'), ttsfile)
                    pl.play(ttsfile)
                time.sleep(sys_delay)

                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring = ''
                userresponcestring = userresponcestring.lower()
                icA(userresponcestring)

                if 'daily' in userresponcestring:
                    icA('Data request..')
                    ts.save2file(ts.tts_request('daily report'), ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

                if 'monthly' in userresponcestring:
                    icA('Data request..')
                    ts.save2file(ts.tts_request('monthly report'), ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

                if 'weekly' in userresponcestring:
                    icA('Data request..')
                    ts.save2file(ts.tts_request('weekly report'), ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue
                else:
                    time.sleep(sys_delay)
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)
                    continue

            # ==== Sensitivity Volume (kept as-is, just flow tidy) ====
            if "sensitivity volume" in userresponcestring:
                icA('Data request..')
                ts.save2file(ts.tts_request('The sensitivity volume is 30N , would you like to turn on the sound ?'), ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)

                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring = ''
                userresponcestring = userresponcestring.lower()
                icA(userresponcestring)

                if 'yes' in userresponcestring:
                    icA('The sound turned on')
                    if path.exists('The_boiler_turned_on.wav'):
                        pl.play('The_boiler_turned_on.wav')
                    else:
                        ts.save2file(ts.tts_request('The sound turned on'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue
                else:
                    icA('Something else?')
                    if path.exists("something else.wav"):
                        pl.play("something else.wav")
                    else:
                        ts.save2file(ts.tts_request('Something else?'), ttsfile)
                        pl.play(ttsfile)
                    time.sleep(sys_delay)

                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring = ''
                    userresponcestring = userresponcestring.lower()
                    icA(userresponcestring)

                    if 'yes' in userresponcestring:
                        icA('What else can I do to help you?')
                        if path.exists('What_else.wav'):
                            pl.play('What_else.wav')
                        else:
                            ts.save2file(ts.tts_request('What else can I do to help you?'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        continue
                    elif 'no' in userresponcestring:
                        time.sleep(sys_delay)
                        icA('Ok, goodbye my friend')
                        if path.exists("Goodbye.wav"):
                            pl.play("Goodbye.wav")
                        else:
                            ts.save2file(ts.tts_request('Ok, goodbye my friend'), ttsfile)
                            pl.play(ttsfile)
                        time.sleep(sys_delay)
                        return
                    else:
                        continue

            else:
                continue


if __name__ == '__main__':
    pl = Player()
    st = STT()
    ts = TTS()

    bot = BOT()
    keyphrase = 'gym'  # wake word updated from 'house' to 'gym'
    icA('BOT started..')
    speech = LiveSpeech(lm=False, keyphrase=keyphrase, kws_threshold=1e-20)
    while 1:
        for phrase in speech:
            icA(phrase)
            if keyphrase in phrase.segments(detailed=True)[0][0]:
                bot.bl(pl, st, ts)
                icA('Ending current busyness logic iteration')
                break
