#!/usr/bin/env python3

# MIT License
#
# Copyright (C) 2020, TwistAtom. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import sys
import math
import json
import argparse
import itertools
from alive_progress import alive_bar, standard_bar_factory, scrolling_spinner_factory, unknown_bar_factory

HELP_DESCRIPTION = "Wonderful tools to detect, hide, read and encrypt data in text."

REPLACEMENT_PATTERN = '|*\\-@O@-\\*|'
DEFAULT_PREVIEW_SIZE = 50
DEFAULT_SPACE_MODE_VALUE = True
DEFAULT_UNCONSTRAIN_VALUE = False #bug
DEFAULT_EQUALIZATION_VALUE = True
DEFAULT_THRESHOLD_VALUE = 35
DEFAULT_ENCRYPTION_VALUE = None

ZERO_WIDTH_SPACE = '\u200b'
ZERO_WIDTH_NON_JOINER = '\u200c'
ZERO_WIDTH_JOINER = '\u200d'
LEFT_TO_RIGHT_MARK = '\u200e'
RIGHT_TO_LEFT_MARK = '\u200f'

MONGOLIAN_VOWEL_SEPARATOR = '\u180e'
ZERO_WIDTH_NO_BREAK_SPACE = '\ufeff'

ZWSP_LIST = [
    ZERO_WIDTH_SPACE,
    ZERO_WIDTH_NON_JOINER,
    ZERO_WIDTH_JOINER,
    LEFT_TO_RIGHT_MARK,
    RIGHT_TO_LEFT_MARK,
]

ZWSP_FULL_LIST = [
    ZERO_WIDTH_SPACE,
    ZERO_WIDTH_NON_JOINER,
    ZERO_WIDTH_JOINER,
    LEFT_TO_RIGHT_MARK,
    RIGHT_TO_LEFT_MARK,
    MONGOLIAN_VOWEL_SEPARATOR,
    ZERO_WIDTH_NO_BREAK_SPACE
]

DETERMINATED_BAR = standard_bar_factory(
    chars="▏▎▍▌▋▊▉█",
    #chars=("\033[32m▏\033[0m", "▎", "\033[32m▍\033[0m", "▌", "▋", "▊", "▉", "\033[32m█\033[0m"),
    borders=("╚|\033[32m", "\033[0m|╝"),
    tip=None,
    errors=(" \033[31m⚠\033[0m", " \033[31m✗\033[0m")
)

#INFINITE_BAR = unknown_bar_factory(scrolling_spinner_factory(('\033[32m►\033[0m',), 5, 2, hiding=False))

class ZWSPTool:
    def __init__(self,  replacement_patten):
        self.replacement_patten = replacement_patten
        self.start()

    def start(self):
        os.system('clear')
        os.system('echo "$(cat banner/banner.txt)"')

    def to_base(self, num, b, numerals='0123456789abcdefghijklmnopqrstuvwxyz'):
        return ((num == 0) and numerals[0]) or (self.to_base(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
        
    def get_padding(self, nb_possibility, threshold):
        return int(threshold/nb_possibility)

    def embed(self, public_text, private_text, zwsp_list, equalize, threshold, space_mode, unconstrain_mode, encryption):
        hidden_codes, final_text, padding = '', '', self.get_padding(len(zwsp_list), threshold)
        position, block_size, nb_spaces = 0, 1, public_text.count(' ')

        if unconstrain_mode:
            settings = json.dumps({
                'zwsp_list': zwsp_list,
                'threshold': threshold
            }, separators=(',',':'))
            private_text = ''.join((settings, private_text))

        nbOperations = len(private_text)*padding
        if(space_mode and nb_spaces > 0):
            nbOperations += nb_spaces
        else:
            nbOperations += len(public_text)

        with alive_bar(nbOperations, bar=DETERMINATED_BAR) as bar:
            print(padding)
            print(equalize)

            for char in private_text:
                code = str(self.to_base(ord(char), len(zwsp_list))).zfill(padding)
                #print(code)
                for code_char in code:
                    hidden_codes += zwsp_list[int(code_char)]
                    bar("Encoding")


            if(nb_spaces <= 0 or not space_mode):
                if(equalize and (len(public_text) - 1) <= len(hidden_codes)):
                    block_size = int(len(hidden_codes)/(len(public_text) - 1))
                elif(not equalize):
                    block_size = len(hidden_codes)
                else:
                    return
                
                print("block_size : " + str(block_size))
                for i in range(len(public_text)):
                    hidden_text = ''

                    if(i == (len(public_text) - 1)):
                        final_text += public_text[i]
                    else:
                        if(position + block_size <= len(hidden_codes) and i < (len(public_text) - 2)):
                            hidden_text = hidden_codes[position: position + block_size]
                        elif(len(hidden_codes) - position > 0):
                            hidden_text = hidden_codes[position:]
                        else:
                            break
                        final_text += public_text[i] + hidden_text
                        position += block_size
                    bar("Masking")
                print()  
                return final_text
            else:
                final_text = public_text
                if(equalize and nb_spaces <= len(hidden_codes)):
                    block_size = int(len(hidden_codes)/nb_spaces)
                elif(not equalize):
                    block_size = len(hidden_codes)
                else:
                    return

                for i in range(nb_spaces):
                    replacement_text = self.replacement_patten
                    if(position + block_size <= len(hidden_codes)):
                        replacement_text += hidden_codes[position: position + block_size]
                    elif(len(hidden_codes) - position > 0):
                        replacement_text += hidden_codes[position:]
                    else:
                        break
                    
                    final_text = final_text.replace(' ', replacement_text, 1)
                    position += block_size    # + 1 ?
                    bar("Masking")
                print() 
                return final_text.replace(self.replacement_patten, ' ')
        
    def extract(self, public_text, zwsp_list, threshold, encryption):
        encoded_text, private_text, padding = '', '', self.get_padding(len(zwsp_list), threshold)
        current_encoded_char = ''

        for char in public_text:
            if char in zwsp_list:
                encoded_text += str(zwsp_list.index(char))
                #bar()
            
        for index, char in enumerate(encoded_text):
            current_encoded_char += char
            if((index + 1) % padding == 0 and index > 0):
                private_text += chr(int(current_encoded_char, len(zwsp_list)))
                current_encoded_char = ''
                #bar()
        #print()    
        return private_text

    def bruteforce(self, public_text, zwsp_list, threshold_range, preview_size, searched_text, encryption, output):
        cpt = 1

        #def powerset(iterable):
            #s = list(iterable)
            #return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

        #print(list(powerset(zwsp_list)))
        #print(len(list(powerset(zwsp_list)))*(threshold_range[1] - threshold_range[0]))
        #nbOperations = (math.factorial(len(zwsp_list)))*(threshold_range[1] - threshold_range[0])

        nbOperations = 0
        for i in range(2, len(zwsp_list) + 1):
                nbOperations += len(list(itertools.permutations(zwsp_list[0:i])))
        nbOperations *= (threshold_range[1] - threshold_range[0])

        print(searched_text)
        with alive_bar(nbOperations, bar=DETERMINATED_BAR) as bar:
            if searched_text:
                if output:
                    file = open(output, "a")
                    for i in range(2, len(zwsp_list) + 1):
                        current_zwsp_list = list(itertools.permutations(zwsp_list[0:i]))
                        
                        for j in range(len(current_zwsp_list)):
                            for threshold in range(threshold_range[0], threshold_range[1]):
                                result = self.extract(public_text, current_zwsp_list[j], threshold, encryption)
                                if(re.search(searched_text, result, re.IGNORECASE)):
                                    file.write("\n{0}. {1}".format(cpt, result[0:preview_size]))
                                    cpt += 1 
                                bar()
                    file.close()
                    print(display.info + "\033[37;1mBruteforce matches have been saved in '\033[36;1m" + output + "\033[0m'")
                else:
                    for i in range(2, len(zwsp_list) + 1):
                        current_zwsp_list = list(itertools.permutations(zwsp_list[0:i]))
                        for j in range(len(current_zwsp_list)):
                            for threshold in range(threshold_range[0], threshold_range[1]):
                                result = self.extract(public_text, current_zwsp_list[j], threshold, encryption)
                                if(re.search(searched_text, result, re.IGNORECASE)):
                                    print("\n\033[37;1m{0}___________________________________◢  \033[32;1mMatch #{1}\033[0m ◣____________________________________\033[0m\n".format('_' * (len(str(cpt)) - 1), cpt))
                                    print(result[0:preview_size])
                                    print("\n\033[37;1m{0}____________________________________________________________________________________\033[0m\n".format('_' * (len(str(cpt)) - 1)))
                                    cpt += 1   
                                bar()     
            else:
                if output:
                    file = open(output, "a")

                    for i in range(2, len(zwsp_list) + 1):
                        current_zwsp_list = list(itertools.permutations(zwsp_list[0:i]))
                        for j in range(len(current_zwsp_list)):
                            for threshold in range(threshold_range[0], threshold_range[1]):
                                file.write("\n{0}. {1}".format(cpt, self.extract(public_text, current_zwsp_list[j], threshold, encryption)[0:preview_size]))
                                cpt += 1
                                bar()
                    file.close()
                    print(display.info + "\033[37;Bruteforce attempts have been saved in '\033[36;1m" + output + "\033[0m'")
                else:
                    for i in range(2, len(zwsp_list) + 1):
                        current_zwsp_list = list(itertools.permutations(zwsp_list[0:i]))
                        for j in range(len(current_zwsp_list)):
                            for threshold in range(threshold_range[0], threshold_range[1]):
                                print("\n\033[37;1m{0}___________________________________◢  \033[32;1mAttempt #{1}\033[0m ◣____________________________________\033[0m\n".format('_' * (len(str(cpt)) - 1), cpt))
                                print(self.extract(public_text, current_zwsp_list[j], threshold, encryption)[0:preview_size])
                                print("\n\033[37;1m_______________________________________________________________________________________\033[0m\n")
                                cpt += 1
                                bar()
        print()
            
class Display(object):
    success = '\033[37;1m[\033[32;1m+\033[37;1m]\033[0m '
    info = '\033[37;1m[\033[36;1m*\033[37;1m]\033[0m '
    error = '\033[37;1m[\033[31;1m-\033[37;1m]\033[0m '
    delimiter = '\n\033[37;1m===================================================================\033[0m\n'

def str2bool(value):
    if isinstance(value, bool):
       return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

display = Display()
zwsp_tool = ZWSPTool(REPLACEMENT_PATTERN)

parser = argparse.ArgumentParser(prog="zwsp-tool", description=HELP_DESCRIPTION)

subparsers = parser.add_subparsers(help='sub-command help', dest="command")

clean_parser = subparsers.add_parser('clean', help='Clean zero width space in text.', description='Clean zero width space in text.')
detect_parser = subparsers.add_parser('detect', help='Detect zero width space in text.', description='Detect zero width space in text.')
embed_parser = subparsers.add_parser('embed', help='Hide private text, with zero width spaces in a cover text.', description='Hide private text, with zero width spaces in a cover text.')
extract_parser = subparsers.add_parser('extract', help='Extract private text from cover text containing zero width spaces.', description='Extract private text from cover text containing zero width spaces.')

clean_parser.add_argument("-i", "--ignore", dest="cleanIgnore", metavar="<ignored_character>", help="Ignore characters.", type=str)
clean_public_group = clean_parser.add_mutually_exclusive_group(required=True)
clean_public_group.add_argument("-p", "--public", dest="cleanPublic", metavar="<public_text>", help="Text to clean.", type=str)
clean_public_group.add_argument("-P", "--pfile", dest="cleanPublicFile", metavar="<path_to_file>", help="Text from a file to clean up.", type=str)
clean_parser.add_argument("-s", "--specific", dest="cleanSpecific", metavar="<specific_character>", help="Clean specific characters.", type=str)

detect_parser.add_argument("-i", "--ignore", dest="detectIgnore", metavar="<ignored_character>", help="Ignore characters.", type=str)
detect_public_Group = detect_parser.add_mutually_exclusive_group(required=True)
detect_public_Group.add_argument("-p", "--public", dest="detectPublic", metavar="<public_text>", help="Suspected text, that could to contain zero width spaces.", type=str)
detect_public_Group.add_argument("-P", "--pfile", dest="detectPublicFile", metavar="<path_to_file>", help="Suspected text from a file, that could to contain zero width spaces.", type=str)
detect_parser.add_argument("-r", "--replace", dest="detectReplace", help="Character replacing zero width spaces.", choices=['dotted', 'escaped', 'named'],)
detect_parser.add_argument("-s", "--search", dest="detectSearch", metavar="<search_character>", help="Search characters.", type=str)

#embed_parser.add_argument("-a", "--auto", dest="embedAuto", metavar="[y/yes/true, n/no/false]", help="-", nargs='?', const=True, default=True, type=str2bool)
embed_parser.add_argument("-c", "--characters", dest="embedCharacters", metavar="[<char_1>, <char_2>]", help="Zero width space characters to use to form the binary code.", type=str)
embed_parser.add_argument("-e", "--encryption", dest="embedEncryption", metavar="[PGP, RSA, AES]", help="Encryption type.", type=str)
embed_mask_group = embed_parser.add_mutually_exclusive_group(required=True)
embed_mask_group.add_argument("-m", "--mask", dest="embedPrivate", metavar="<hidden_text>", help="Text to hide in another text (public text).", type=str)
embed_mask_group.add_argument("-M", "--mfile", dest="embedPrivateFile", metavar="<path_to_file>", help="Text from a file to hide in another text (public text).", type=str)
embed_public_group = embed_parser.add_mutually_exclusive_group(required=True)
embed_public_group.add_argument("-p", "--public", dest="embedPublic", metavar="<public_text>", help="Cover text for hidden text (private text).", type=str)
embed_public_group.add_argument("-P", "--pfile", dest="embedPublicFile", metavar="<path_to_file>", help="Use text cover from a file, for hidden text (private text).", type=str)
embed_parser.add_argument("-s", "--space", dest="embedSpace", metavar="[y/yes/true, n/no/false]", help="If enabled, it allows a better discretion by only putting spaces of zero width in existing visible spaces.", nargs='?', const=True, default=DEFAULT_SPACE_MODE_VALUE, type=str2bool)
embed_parser.add_argument("-t", "--threshold", dest="embedThreshold", metavar="<number>", help="Size of an encoding string, the larger the number, the more it is possible to encode different characters. However it is best to keep a small size in order to remain discreet.", type=int)
embed_parser.add_argument("-u", "--unconstrain", dest="embedUnconstrain", metavar="[y/yes/true, n/no/false]", help="If enabled (enabled by default), hides the masking parameters with the private text in the cover text (public text). In order not to need to remember the parameters at the time of extraction.", nargs='?', const=True, default=DEFAULT_UNCONSTRAIN_VALUE, type=str2bool)
embed_parser.add_argument("-z", "--equalize", dest="embedEqualize", metavar="[y/yes/true, n/no/false]", help="If enabled, evenly distribute the zero width spaces, corresponding to the hidden text (private text), on the set of visible spaces of the cover text (public text).", nargs='?', const=True, default=DEFAULT_EQUALIZATION_VALUE, type=str2bool)

extract_parser.add_argument("-b", "--bruteforce", dest="bruteforce", help="Test all possible characters and combinations to extract data.", action="store_true")
extract_public_group = extract_parser.add_mutually_exclusive_group(required=True)
extract_public_group.add_argument("-p", "--public", dest="extractPublic", metavar="<public_text>", help="Cover text containing zero width space characters to extract.", type=str)
extract_public_group.add_argument("-P", "--pfile", dest="extractPublicFile", metavar="<path_to_file>", help="Use text cover from a file, containing zero width space characters for extraction.", type=str)

parser.add_argument("-o", "--output", dest="output", metavar="<output_file>", help="File to store the results.", type=str)
verbose_group = parser.add_mutually_exclusive_group()
verbose_group.add_argument("-q", "--quiet", dest="quiet", help="Disable output verbosity.", action="store_true")
verbose_group.add_argument("-v", "--verbose", dest="verbose", help="Increase output verbosity.", action="store_true")

args = parser.parse_args()


try:
    if args.command == "clean": 
        initial_text, analyzed_text = "", ""
        if args.cleanPublic:
            initial_text = args.cleanPublic.encode('ascii', 'ignore').decode('unicode_escape')
        elif args.cleanPublicFile:
            file = open(args.cleanPublicFile, "r")
            initial_text = file.read()
            file.close()

        with alive_bar(len(initial_text), bar=DETERMINATED_BAR) as bar:
            for i in range(len(initial_text)-1):
                bar()
            cleanedText = initial_text.encode('ascii', 'ignore').decode('unicode_escape')
            bar()
        print()

        if args.output:
            file = open(args.output, "a")
            file.write("\n" + cleanedText)
            file.close()
            print(display.success + "\033[37;1mThe text has been cleaned up\033[0m")
            print(display.info + "\033[37;1mText saved in '\033[36;1m" + args.output + "\033[0m'")
        else:
            print(display.success + "\033[37;1mThe text has been cleaned up\033[0m")
            print(display.delimiter)
            print(cleanedText)
            print(display.delimiter + "\n")

    elif args.command == "detect":
        initial_text, analyzed_text = "", ""
        if args.detectPublic:
            initial_text = args.detectPublic
        elif args.detectPublicFile:
            file = open(args.detectPublicFile, "r")
            initial_text = file.read()
            file.close()
            
        if args.detectReplace == "escaped" or args.detectReplace == "named":
            with alive_bar(len(initial_text)) as bar:
                for i in range(len(initial_text)-1):
                    bar()
                if args.detectReplace == "escaped":
                    analyzed_text = initial_text.encode("ascii", "backslashreplace")
                else:
                    analyzed_text = initial_text.encode("ascii", "namereplace")
                bar()
        else:
            with alive_bar(len(initial_text), bar=DETERMINATED_BAR) as bar:
                for i in range(len(initial_text)-1):
                    bar()
                if args.output:
                    analyzed_text = re.sub('&#.{4,5};', '•', initial_text.encode("ascii", "xmlcharrefreplace").decode('utf-8'))
                else:
                    analyzed_text = re.sub('&#.{4,5};', '\033[31;1m•\033[0m', initial_text.encode("ascii", "xmlcharrefreplace").decode('utf-8'))
                bar()
        print()

        if args.output:
            file = open(args.output, "a")
            file.write("\n" + analyzed_text)
            file.close()
            print(display.success + "\033[37;1mThe text has been correctly analyzed\033[0m")
            print(display.info + "\033[37;1mAnalyzed text saved in '\033[36;1m" + args.output + "\033[0m'")
        else:
            print(display.success + "\033[37;1mThe text has been correctly analyzed\033[0m")
            print(display.delimiter)
            print(analyzed_text)
            print(display.delimiter + "\n")
    elif args.command == "embed":
        public_text, private_text, final_text = "", "", ""
        print(args.embedEqualize)
        equalize = args.embedEqualize
        space_mode = args.embedSpace
        unconstrain_mode = args.embedUnconstrain
        threshold = args.embedThreshold if args.embedThreshold else DEFAULT_THRESHOLD_VALUE
        encryption = args.embedEncryption if args.embedEncryption else DEFAULT_ENCRYPTION_VALUE

        if args.embedPublic:
            public_text = args.embedPublic
        elif args.embedPublicFile:
            file = open(args.embedPublicFile, "r")
            public_text = file.read()
            file.close()

        if args.embedPrivate:
            private_text = args.embedPrivate
        elif args.embedPrivateFile:
            file = open(args.embedPrivateFile, "r")
            private_text = file.read()
            file.close()

        final_text = zwsp_tool.embed(public_text, private_text, ZWSP_LIST, equalize, threshold, space_mode, unconstrain_mode, encryption)
        print()

        if args.output:
            file = open(args.output, "a")
            file.write("\n" + final_text)
            file.close()
            print(display.success + "\033[37;1mThe text has been correctly hidden\033[0m")
            print(display.info + "\033[37;1mText saved in '\033[36;1m" + args.output + "\033[0m'")
        else:
            print(display.success + "\033[37;1mThe text has been correctly hidden\033[0m")
            print(display.delimiter)
            print(final_text)
            print(display.delimiter + "\n")
    elif args.command == "extract":
        public_text, private_text = "", ""
        #equalize = args.embedEqualize if args.embedEqualize else DEFAULT_EQUALIZATION_VALUE
        threshold = DEFAULT_THRESHOLD_VALUE
        encryption = DEFAULT_ENCRYPTION_VALUE

        if args.extractPublic:
            public_text = args.extractPublic
        elif args.extractPublicFile:
            file = open(args.extractPublicFile, "r")
            public_text = file.read()
            file.close()

        if args.bruteforce:
            threshold_range = (35, 38)
            clever_mode = True
            searched_text = ""

            #r'[a-zA-Z\d]'
            regex = r'[a-zA-Z]{3}' if clever_mode else (".*" + searched_text + ".*")
            zwsp_tool.bruteforce(public_text, ZWSP_FULL_LIST, threshold_range, DEFAULT_PREVIEW_SIZE, regex, encryption, args.output)
        else:
            with alive_bar(bar=DETERMINATED_BAR) as bar:
                private_text = zwsp_tool.extract(public_text, ZWSP_LIST, threshold, encryption)
            if args.output:
                file = open(args.output, "a")
                file.write(private_text)
                file.close()
                print(display.success + "\033[37;1mText has been correctly extracted\033[0m")
                print(display.info + "\033[37;1mText saved in '\033[36;1m" + args.output + "\033[0m'")
            else:
                print(display.success + "\033[37;1mText has been correctly extracted\033[0m")
                print(display.delimiter)
                print(private_text)
                print(display.delimiter + "\n")

    elif args.verbose:
        print("verbosity turned on")
    else:
        parser.print_help()
except FileNotFoundError:
    print(display.error + "\033[37;1mThe file was not found !\033[0m\n")
except UnicodeEncodeError:
    pass