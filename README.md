# :mag:  ZWSP-Tool

<p align=center>
    <a href="https://github.com/TwistAtom/ZWSP-Tool/issues">
        <img src="https://img.shields.io/github/issues/TwistAtom/ZWSP-Tool">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/python-3.2%20%7C%203.3%20%7C%203.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/ZWSP--Tool-v1.2-blueviolet">
    </a>
</p>

___

## About ZWSP Toolkit

```
ZWSP-Tool is a powerful toolkit that allows to manipulate 
zero width spaces quickly and easily. ZWSP-Tool allows in 
particular to detect, clean, hide, extract and bruteforce 
a text containing zero width spaces.
```

## :inbox_tray: Installation

Clone the repository :
```sh
$ git clone https://github.com/TwistAtom/ZWSP-Tool.git
```

Move in the folder :
```sh
$ cd ZWSP-Tool
```

Add the execution right to the installation file :
```sh
$ chmod +x install.sh
```

Finally, run the installation file :
```sh
$ ./install.sh
```

## :rocket: Launch

After installation, you can now launch the ZWSP toolkit from anywhere by typing :
```sh
$ zwsp-tool
```

## :x: Uninstallation

```sh
$ cd ZWSP-Tool
$ ./uninstall.sh
```

## :black_nib:  Examples
1 - Detect zero width characters in text file by displaying them as red dotted markers on standard output :
```sh
$ zwsp-tool detect -P path_to_file/suspicious_text.txt
```
2 - Remove zero width characters from a text file :
```sh
$ zwsp-tool clean -P path_to_file/suspicious_text.txt
```
3 - Hide private text in cover text with encryption and store the result in an external file : 
```sh
$ zwsp-tool -o result.txt embed -p "Public text" -m "Private text" -e AES
```
4 - Extract a private text contained in a cover text and display it on standard output :
```sh
$ zwsp-tool extract -P path_to_file/text.txt -e AES 
```
5 - Bruteforce a suspicious text containing zero-width characters :
```sh
$ zwsp-tool bruteforce -P path_to_file/suspicious_text.txt
```

## License

Copyright © 2020 TwistAtom  
Licensed under the [MIT](LICENSE).
