import os
import math
import subprocess
import json

imei = None
autosave = False
bruteforceProtection = False
config = None
autosaveCode = 1000000000000000
failattempts = 4
autosaveCount = 200


print("\033[H\033[J", end="")

try:
    config = open("config.json", "r")
except:
    print("Config file not found!")
    print("Create config file and run script again")
    exit(1)

data = json.load(config)
if(data["imei"] != None and data["autosave"] != None and data["bruteforceProtection"] != None and data["failAttempts"] != None and data["autosaveCount"] != None):
    imei = data["imei"]
    autosave = data["autosave"]
    bruteforceProtection = data["bruteforceProtection"]
    failattempts = data["failAttempts"]
    autosaveCount = data["autosaveCount"]

    config.close()
else:
    print("Invalid config file!")
    exit(1)

try:
    autosaveFile = open("autosave.txt", "r")
    autosaveData = autosaveFile.read()
    autosaveCode = int(autosaveData)
    autosaveFile.close()
except:
    pass


print("Bootloader bruteforce unlock")
print("==========================")
print("Config:")
print()
print("IMEI: "+str(imei))
print("Autosave: "+str(autosave))
print("Bruteforce protection: " + str(bruteforceProtection))
print("Autosave code not found" if autosaveCode ==
      1000000000000000 else "Autosave code found " + str(autosaveCode))
print("==========================")
print("NOTE: All data will be erased!")
print("")
input("Press any key to start...")

os.system('adb devices')


def bruteforceBootloader(increment):
    algoOEMcode = autosaveCode
    autoreboot = bruteforceProtection
    autorebootcount = failattempts
    savecount = autosaveCount

    failmsg = "check password failed"

    unlock = False
    n = 0
    while (unlock == False):
        print("\033[H\033[J", end="")
        print("Bruteforce is running...\nCurrently testing code "+str(algoOEMcode).zfill(16) +
              "\nProgress: "+str(round((algoOEMcode/10000000000000000)*100, 2))+"%")
        output = subprocess.run("fastboot oem unlock " + str(algoOEMcode).zfill(
            16), shell=True, stderr=subprocess.PIPE).stderr.decode('utf-8')
        print(output)
        output = output.lower()
        n += 1

        if 'success' in output:
            bak = open("unlock_code.txt", "w")
            bak.write("Your saved bootloader code : "+str(algoOEMcode))
            bak.close()
            print("Your bruteforce result has been saved in \"unlock_code.txt\"")
            return(algoOEMcode)
        if 'reboot' in output:
            print("Target device has bruteforce protection!")
            print("Waiting for reboot and trying again...")
            os.system("adb wait-for-device")
            os.system("adb reboot bootloader")
            print("Device reboot requested, turning on reboot workaround.")
            autoreboot = True
        if failmsg in output:
            #print("Code " + str(algoOEMcode) + " is wrong, trying next one...")
            pass
        if 'success' not in output and 'reboot' not in output and failmsg not in output:
            # fail here to prevent continuing bruteforce on success or another error the script cant handle
            print("Could not parse output.")
            print("Please check the output above yourself.")
            print(
                "If you want to disable this feature, switch variable unknownfail to False")
            exit()

        if (n % savecount == 0):
            bak = open("autosave.txt", "w")
            bak.write(str(algoOEMcode))
            bak.close()
            print("Autosave.")

        if (n % autorebootcount == 0 and autoreboot):
            print("Rebooting to prevent bootloader from rebooting...")
            os.system('fastboot reboot bootloader')

        algoOEMcode += increment

        if (algoOEMcode > 10000000000000000):
            print("OEM Code not found!\n")
            os.system("fastboot reboot")
            exit()


def luhn_checksum(imei):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(imei)
    oddDigits = digits[-1::-2]
    evenDigits = digits[-2::-2]
    checksum = 0
    checksum += sum(oddDigits)
    for i in evenDigits:
        checksum += sum(digits_of(i*2))
    return checksum % 10


checksum = 1
while (checksum != 0):
    checksum = luhn_checksum(imei)
    if (checksum != 0):
        print('IMEI incorrect!')
        if(imei > 0):
            exit()
increment = int(math.sqrt(imei)*1024)
os.system('adb reboot bootloader')

codeOEM = bruteforceBootloader(increment)

os.system('fastboot getvar unlocked')

print()
print('Device unlocked! OEM CODE: '+codeOEM)
exit()
