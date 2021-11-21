# Booloader unlock code bruteforce

This simple tool can help with unlocking bootloader on phone with locked bootloader with code.
For example some Huawei phones have this stupid things. I don't know on which phones this works.

# Run
1. Install `adb` and `fastboot`
2. Create config file `config.json` with payload like this:

```
{
    "bruteforceProtection": true,
    "imei": 123456789123456,
    "autosave": true,
    "failAttempts": 4,
    "autosaveCount": 200
}
```

`bruteforceProtection` - Enable this, if your device reboots when is entered wrong unlock code.

`imei` - Phone IMEI

`autosave` - If enabled, program will save progress of bruteforcing, so the unlocking process can be resumed later.

`failAttempts` - After how many wrong attemtp device reboot (For bruteforceProtection)

`autosaveCount` - After how many code should be the progress be saved.

3. `python3 main.py`