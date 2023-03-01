![Supported Python versions](https://img.shields.io/badge/python-3.6-blue.svg?style=flat-square)

# WinGenFileIntegrityInfo
Add a custom context menu for windows that copies the integrity information of a file to the clipboard

BoB 디포트랙 과제 메일 제출시 무결성 정보 첨부 편의용

This was partly written by chatGPT OpenAI.


## How to install
Double click GenFileIntegInfo_*_install.py

You can choose one of the three options
### GenFileIntegInfo_FULL_install.py
- add both(md5+sha1, sha2) context menu

### GenFileIntegInfo_md5sha1_install.py
- add md5+sha1 context menu
- delete sha2 context menu

### GenFileIntegInfo_sha2_install.py
- add sha2 context menu
- delete md5+sha1 context menu

The installation files in the paperclip_lib_ver folder use the piperclip library instead of the tkinter library, and install the piperclip library automatically.

## How to uninstall
Double click GenFileIntegInfo_uninstall.py



## How to use

1 right click a file

2 click "Copy FileInfo with SHA256 to clipboard"

![image](https://user-images.githubusercontent.com/33446356/218667692-2fe090bf-bf0f-40ab-a583-d3708b94e91a.png)

3 Paste it to any text area

![image](https://user-images.githubusercontent.com/33446356/218667940-635f2e06-f0d7-412e-8665-f48ce8793846.png)

1. Or Run the program from CMD, which is run by administrator privileges.

![image](https://user-images.githubusercontent.com/33446356/222165017-d9b7badd-c5b4-4090-bdd2-5252fdd2c721.png)


## structure
![image](https://user-images.githubusercontent.com/33446356/218670215-45ab63f5-9915-4fea-bf1f-424f8b33dcaf.png)


