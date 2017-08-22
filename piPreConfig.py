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
    open(filename, 'w').close()

def set_config_comment(key, value):
    global output_dir
    global config_file

    filename = output_dir + '/' + config_file
    open(filename, 'w').close()


def enable_ssh():
    global output_dir
    global config_file
    print("Creating empty 'ssh' file use to enable ssh...")
    filename = output_dir + '/' + ssh_file
    open(filename, 'w').close()


def set_wifi(ssid, passphrase):
    global output_dir
    global config_file
    print("Creating wpa_supplicant.conf file...")

    filename = output_dir + '/' + wifi_file
    
    f = open(filename, 'w')
    f.write("testing");
    f.close()


# Check if the output directory exists.  If not abort.
if not os.path.exists('./' + output_dir):
    os.makedirs('./' + output_dir)
    
#Start the Questionaire code
q.one('lcd_rotate', ('0', '0 degrees (default)'), ('90', '90 degrees'), ('180', '180 degrees'), ('270', '270 degrees'), prompt='Set lcd_rotate?')

q.one('enable_wifi', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable Wifi?')

q.raw('ssid', prompt='WIFI SSID: ').condition(('enable_wifi', 'true'))
q.raw('passphrase', prompt='WIFI Passphrase: ', secret=True).condition(('enable_wifi', 'true'))

q.one('enable_ssh', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable SSH?')

q.one('enable_i2c', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable I2C?')
q.one('enable_i2s', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable I2S?')
q.one('enable_SPI', ('false', 'disabled (default)'), ('true', 'enabled'), prompt='Enable SPI?')

q.run()

answers = q.format_answers()
data  = json.loads(answers)

for row in data:
    if row == 'lcd_rotate':
        set_config('lcd_rotate', data[row])
    if row == 'lcd_rotate':
        set_config('lcd_rotate', data[row])
    elif row == 'enable_ssh' and data[row] == "enabled":
        enable_ssh()
    elif row == 'enable_wifi' and data[row] == "enabled":
        set_wifi(data['ssid'], data['passphrase'])
    elif row == 'enable_i2c' and data[row] == "enabled":
        set_config('dtparam=i2c_arm', "on")
    elif row == 'enable_i2s' and data[row] == "enabled":
        set_config('dtparam=i2s', "on")
    elif row == 'enable_i2s' and data[row] == "enabled":
        set_config('dtparam=spi', "on")
        
# Add some additional default parameters that the user doesn't need to care about.
set_config('dtparam=audio', "on")