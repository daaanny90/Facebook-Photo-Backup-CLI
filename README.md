# Facebook Photo Backup (CLI version) :camera:
A simple CLI tool to download and save all your personal photos (not divided by album) and all the images in which you are tagged.


## Installation
Clone or download the repo:
```
git clone https://github.com/daaanny90/Facebook-Photo-Backup-CLI.git
```

Install the dependencies:
```
cd Facebook-Photo-Backup-CLI
py -m pip install requirements
```

The script needs Firefox installed to work. If you don't have Firefox installed, you can get it from [this link](https://www.mozilla.org/en-US/firefox/new/) (and I suggest you to use it as your default browser).

Than you should put into the `Facebook-Photo-Backup-CLI` folder the right `geckodriver.exe` for your OS. You can download it from [here](https://github.com/mozilla/geckodriver/releases).

## How to use it
Just start the script with:
```
py fpb_cli.py
```
The script will ask you your name on Facebook, your password and the path where you want to save the pictures.

When you write your password nothing will be shown while typing. Is normal, just write the password and hit enter.

The path must be written with backslash, even at the end, for example:
```
C:\\Users\\myname\\Desktop\\
```

Then just wait until all your pictures are safe.

**If you have any problem please open an issue. If you are a programmer, please make a PR!**
