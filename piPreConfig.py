# questions.py
from questionnaire import Questionnaire
import json, os
q = Questionnaire()

output_dir = "output"
config_file = "config.txt"
ssh_file = "ssh"
wifi_file = "wpa_supplicant.conf"

def set_config(key, value):
    global output_dir
    global config_file
    print("Setting " + key + " in config.txt...")
    filename = output_dir + '/' + config_file
    f = open(filename, 'a')
    f.write(key + "=" + value + "\n");
    f.close()


# Sets a key value pair in the config.txt that tells the raspberry pi
# what configuration options are available at boot time.
def set_config_comment(key, value):
    global output_dir
    global config_file

    filename = output_dir + '/' + config_file
    f = open(filename, 'a+')
    f.write(key + "=" + value + "\n");
    f.close()


# Creates an empty ssh file that tells the raspberry pi to enable ssh
def enable_ssh(enable):
    global output_dir
    global config_file
    filename = output_dir + '/' + ssh_file
    
    if enable == "true":
        print("Creating empty 'ssh' file used to enable ssh...")
        open(filename, 'w').close()
    elif enable == "false" and os.path.isfile(filename):
        print("Removing empty 'ssh' file used to enable ssh if it exists...")
        os.remove(filename)


# Creates the wpa_supplicant.conf file and enters the neccessary data.
def set_wifi(enable="false", ssid="", passphrase=""):
    global output_dir
    global config_file
    filename = output_dir + '/' + wifi_file

    if enable == "true":
        print("Creating wpa_supplicant.conf file...")
        f = open(filename, 'w')
        f.write('network={'+"\n");
        f.write('ssid="' + ssid  + '"'+"\n");
        f.write('psk="' + passphrase + '"'+"\n");
        f.write('}'+"\n");
        f.close()
    elif enable == "false" and os.path.isfile(filename):
        print("Removing wpa_supplicant.conf file if it exists...")
        os.remove(filename)

# Check if the output directory exists.  If not abort.
if not os.path.exists('./' + output_dir):
    os.makedirs('./' + output_dir)

filename = output_dir + '/' + config_file
if os.path.exists(filename):
    os.remove(filename)
    
#Start the Questionaire code
q.one('enable_lcd_rotate', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Rotate LCD? (For use with PiFoundation TFT Touchscreen)')

q.one('lcd_rotate', ('0', '0 degrees (default)'), ('90', '90 degrees'), ('180', '180 degrees'), ('270', '270 degrees'), prompt='Set lcd_rotate?').condition(('enable_lcd_rotate', 'true'))

q.one('enable_wifi', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable Wifi?')

q.raw('ssid', prompt='WIFI SSID: ').condition(('enable_wifi', 'true'))
q.raw('passphrase', prompt='WIFI Passphrase: ', secret=True).condition(('enable_wifi', 'true'))

q.one('enable_ssh', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable SSH?')

q.one('enable_i2c', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable I2C?')
q.one('enable_i2s', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable I2S?')
q.one('enable_SPI', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable SPI?')

q.run()

os.system('clear')

answers = q.format_answers()
data  = json.loads(answers)

for row in data:
    if row == 'lcd_rotate':
        set_config('lcd_rotate', data[row])
    elif row == 'enable_i2c' and data[row] == "true":
        set_config('dtparam=i2c_arm', "on")
    elif row == 'enable_i2s' and data[row] == "true":
        set_config('dtparam=i2s', "on")
    elif row == 'enable_spi' and data[row] == "true":
        set_config('dtparam=spi', "on")
    elif row == 'enable_ssh':
        enable_ssh(data[row])
    elif row == 'enable_wifi':
        if data[row] == "true":
            set_wifi(data[row], data['ssid'], data['passphrase'])
        else:
            set_wifi(data[row])
        
# Add some additional default parameters that the user doesn't need to care about.
set_config('dtparam=audio', "on")