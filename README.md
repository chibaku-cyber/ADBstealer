# ADBstealer

This tool is a PoC (Proof of Concept) of original bug reported to Google Chrome for Android.
Vulnerability : https://bugs.chromium.org/p/chromium/issues/detail?id=1129358
The vulnerability that exists in Android versions prior to Android 11, which allows anyone to connect to Android Debug Bridge listening on port 5555 without any authentication.
Google Chrome for Android stores plaintext passwords in /data/data/com.android.chrome/app_chrome/Default/Login Data 
Therefore, If an Android device is rooted remote attacker can steal passwords stored in Google Chrome's private data folder.
However if an Android device is not rooted, this tool will not work.

## Requirements

-   Python 3
-   ADB Tools
-   pure-python-adb

## Install Dependencies
```
sudo apt-get install git python3-pip
sudo apt-get install android-tools-adb
sudo pip install pure-python-adb
git clone https://github.com/chibaku-cyber/adbstealer
cd adbstealer
```

## Usage

```
Start ADB server using : adb devices
python3 adbstealer.py <target>
```
It will take some time and Login Data file will be created in your current working directory. Open Login Data file with SQLite database browser.

# License

The ADBstealer is under a BSD license.
Please see [LICENSE](LICENSE) for more details.

## Disclaimer
This tool is a PoC (Proof of Concept) and does not guarantee results.
Usage of ADBstealer for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program. 
This tool is only for academic purposes and testing  under controlled environments.