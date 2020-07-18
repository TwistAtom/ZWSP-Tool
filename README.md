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

![zwsp-tool](https://user-images.githubusercontent.com/38385977/87852935-777eb200-c906-11ea-983a-51190b377fba.png)

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
## :gear:  Options

### Clean module

| Parameter |  Type  |           Format          | Default |            Note            |
|:---------:|:------:|:-------------------------:|:-------:|:--------------------------:|
|     `-i`,<br/><nobr>`--ignore`<nobr>    | `string` | `"<char_1>, <char_2>, ..."` |         | Ignore characters.<img width=200/>         |
|     `-s`,<br/><nobr>`--specific`<nobr>    | `string` | `"<char_1>, <char_2>, ..."` |         | Clean specific characters. |

### Detect module

|   Parameter   |  Type  |           Format          | Default |                  Note                  |
|:-------------:|:------:|:-------------------------:|:-------:|:--------------------------------------:|
|  `-i`,<br/><nobr>`--ignore`<nobr> | `string` | `"<char_1>, <char_2>, ..."` |         | Ignore characters.<img width=200/>                     |
| `-r`,<br/><nobr>`--replace`<nobr> | `string` |  {`dotted`, `escaped`, `named`} |  `dotted` | Character replacing zero width spaces. |
|  `-s`,<br/><nobr>`--search`<nobr> | `string` | `"<char_1>, <char_2>, ..."` |         | Search characters.                     |

### Embed module

|     Parameter     |   Type  |           Format           |                       Default                      |                                                                                               Note                                                                                              |
|:-----------------:|:-------:|:--------------------------:|:--------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    `-c`,<br/><nobr>`--characters`<nobr>   |  `string` |  `"<char_1>, <char_2>, ..."` | `('\u200b', '\u200c', '\u200d', '\u200e', '\u200f')` | Zero width characters to use to encode the private text. Use the `list` argument to see some possible characters.<img width=200/>                                                                |
|  `-e`,<br/><nobr>`--encryption`<nobr> |  `string` |       {`AES`, `RSA`, `PGP`}      |                                                    | Encryption type.                                                                                                                                                                                |
|     `-m`,<br/><nobr>`--mask`<nobr>    |  `string` |        `<hidden_text>`       |                                                    | Text to hide in another text (public text).<br/>`Required`<br/>**Note:** cannot be used with `-M`, `--mfile`                                                                                                                                                     |
|    `-M`,<br/><nobr>`--mfile`<nobr>    |  `string` |       `<path_to_file>`       |                                                    | Text from a file to hide in another text (public text).<br/>`Required`<br/>**Note:** cannot be used with `-m`, `--mask`                                                                                                                                         |
|    `-s`,<br/><nobr>`--space`<nobr>    | `boolean` | `[[y/yes/true, n/no/false]]` |                        `True`                        | If enabled, it allows a better discretion by only putting spaces of zero width in existing visible spaces.                                                                                      |
|  `-t`,<br/><nobr>`--threshold`<nobr>  | `integer` |          `<number>`          |                         `35`                         | Size of an encoding string, the larger the number, the more it is possible to encode different characters. However it is best to keep a small size in order to remain discreet.  |
| `-u`,<br/><nobr>`--unconstrain`<nobr> | `boolean` | `[[y/yes/true, n/no/false]]` |                        `False`                       | If enabled (enabled by default), hides the masking parameters with the private text in the cover text (public text). In order not to need to remember the parameters at the time of extraction. |
|   `-z`,<br/><nobr>`--equalize`<nobr>  | `boolean` | `[[y/yes/true, n/no/false]]` |                        `True`                        | If enabled, evenly distribute the zero width spaces, corresponding to the hidden text (private text), on the set of visible spaces of the cover text (public text).                             |

### Extract module

|     Parameter    |   Type  |           Format          |                       Default                      |                                                                                       Note                                                                                      |
|:----------------:|:-------:|:-------------------------:|:--------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `-c`,<br/><nobr>`--characters`<nobr> |  string | `"<char_1>, <char_2>, ..."` | `('\u200b', '\u200c', '\u200d', '\u200e', '\u200f')` | Zero width characters to use to decode the private text. Use the 'list' argument to see some possible characters.<img width=200/>                                                               |
| `-e`,<br/><nobr>`--encryption`<nobr> |  `string` |      {`AES`, `RSA`, `PGP`}      |                                                    | Encryption type.                                                                                                                                                                |
|  `-t`,<br/><nobr>`--threshold`<nobr> | `integer` |          `<number>`         |                         `35`                         | Size of an encoding string, the larger the number, the more it is possible to encode different characters. However it is best to keep a small size in order to remain discreet. |

### Bruteforce module

|     Parameter    |   Type  |            Format            |                       Default                      |                                                                                   Note                                                                                  |
|:----------------:|:-------:|:----------------------------:|:--------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    `-b`,<br><nobr>`--base`<nobr>    | `integer` |            `<base>`            |                                                    | Manually choose a fixed base (e.g : 2 for binary) to force the text. Please note, the base chosen cannot exceed the number of zero width spaces available in the lists.<img width=200/> |
| `-c`,<br><nobr>`--characters`<nobr> |  `string` |   `"<char_1>, <char_2>, ..."`  | `('\u200b', '\u200c', '\u200d', '\u200e', '\u200f')` | Zero width characters to use to decode the private<br>                        text.                                                                                     |
|    `-d`,<br><nobr>`--demo`<nobr>    | `integer` |        `<preview_size>`        |                         `50`                         | Size of the preview in number of characters. This allows you to quickly view and analyze bruteforce attempts.                                                           |
| `-e`,<br><nobr>`--encryption`<nobr> |  `string` |        {`AES`, `RSA`, `PGP`}       |                                                    | Encryption type.                                                                                                                                                        |
|   `-s`,<br><nobr>`--search`<nobr>   |  `string` |   `"<term_1>, <term_2>, ..."`  |                                                    | Specific terms to search for validate a bruteforce attempt.<br>**Note:** cannot be used with `-w`, `--wily`                                                                     |
|  `-t`,<br><nobr>`--threshold`<nobr> |  `string` | `"<start_range>, <end_range>"` |                      `(10, 38)`                      | Size of an encoding string, the larger the number, the more it is possible to encode different characters. Select the threshold range to test.                          |
|    `-w`,<br><nobr>`--wily`<nobr>    | `boolean` |  `[[y/yes/true, n/no/false]]`  |                        True                        | Intelligent algorithm that only selects attempts that can be interesting to study. Please note that this is largely based on the composition of the latin alphabet.     |

### Arguments in common

|   Parameter   |   Type  |     Format     | Default |                                                Note                                               |
|:-------------:|:-------:|:--------------:|:-------:|:-------------------------------------------------------------------------------------------------:|
|  `-o`,<br/><nobr>`--output`<nobr> |  `string` |  `<output_file>` |         | File to store the results.<img width=300/>                                                                        |
|  `-p`,<br/><nobr>`--public`<nobr> |  `string` |  `<public_text>` |         | Visible text to use entered from the command line.<br/>`Required`<br/>**Note:** cannot be used with `-P`, `--pfile` |
|  `-P`,<br/><nobr>`--pfile`<nobr>  |  `string` | `<path_to_file>` |         | Visible text to use from a text file.<br/>`Required`<br/>**Note:** cannot be used with `-p`, `--public`             |
|  `-q`,<br/><nobr>`--quiet`<nobr>  | `boolean` |                |  `False`  | Disable output verbosity.                                                                         |
| `-v`,<br/><nobr>`--verbose`<nobr> | `boolean` |                |  `False`  | Increase output verbosity.                                                                        |

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

## :clipboard:  To-do list
- [ ] add other type of encryption
- [ ] improve zero width space detection
- [ ] operate the unconstrained mode

## :page_with_curl:  License

Copyright © 2020 TwistAtom  
Licensed under the [MIT](LICENSE).
