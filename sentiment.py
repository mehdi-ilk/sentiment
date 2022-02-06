import string
from hazm.POSTagger import StanfordPOSTagger
from hazm.Normalizer import Normalizer
from hazm.InformalNormalizer import InformalNormalizer
import emoji
import re
import json
import time


with open('bad_words_list.json', 'r') as f1:
    bad_word_list = json.load(f1)

with open('bad_words_list_separated.json', 'r') as f2:
    bad_word_list_separated = json.load(f2)

with open('third_list.json', 'r') as f3:
    third_list = json.load(f3)


punctuation_marks_codepoints = '\u061B\u0640\u066A\u066B\u066C'
string_punctuation = list(string.punctuation)
string_punctuation.remove('.')
string_punctuation.remove('!')
string_punctuation.remove(':')
emojis_allowed = ['🙁', '😡', '🙂']


def former_validity_check(input_string: str):
    if len(input_string) > 255:
        return False
    else:
        for i in input_string:
            if i in string.ascii_letters or i in string_punctuation or i in punctuation_marks_codepoints or i in string.digits:
                return False
    # return_value_for_emoji_existence = emoji.emoji_count(input_string)
    # if return_value_for_emoji_existence > 0:
    #     return False
    for item in emoji.emoji_lis(input_string):
        if item['emoji'] not in emojis_allowed:
            return False

    return input_string


def check_for_repetition(in_string: str):
    if not former_validity_check(in_string):
        return False
    return True
    # for i in range(len(in_string)):
    #     if i == len(in_string) - 1 or i == len(in_string) - 2:
    #         return True
    #     else:
    #         if in_string[i] == in_string[i + 1] and in_string[i + 1] == in_string[i + 2]:
    #             return False


def text_cleaner(raw_input_string: str):
    if not check_for_repetition(raw_input_string):
        return False

    if 'گرممه' in raw_input_string or 'ممه' in raw_input_string or 'یید' in raw_input_string or 'ئید' in raw_input_string:

        if 'ری' in raw_input_string and 'ید' in raw_input_string:
            print('here')
            normalizer = Normalizer()
            informal_normalizer = InformalNormalizer()
            first_filtered_string = ''.join([char for char in raw_input_string if char not in string_punctuation])

            second_filtered_string = normalizer.character_refinement(first_filtered_string)

            third_filtered_as_string = ''
            for i in range(len(second_filtered_string)):
                if i == len(second_filtered_string) - 1:
                    third_filtered_as_string += second_filtered_string[i]
                else:
                    if second_filtered_string[i] != second_filtered_string[i + 1]:
                        third_filtered_as_string += second_filtered_string[i]
            exceptions = [['', ''], ['', ' '], [' ', ''], [' ', ' ']]
            if third_filtered_as_string.split('رید') in exceptions:
                return False
            if len(third_filtered_as_string.split('رید')) > 1 and third_filtered_as_string.split('رید') not in exceptions:
                for i in range(len(third_filtered_as_string.split('رید'))):
                    if i != len(third_filtered_as_string.split('رید')) - 1:
                        if len(third_filtered_as_string.split('رید')[i]) > 0 and len(third_filtered_as_string.split('رید')[i + 1]) > 0:
                            if third_filtered_as_string.split('رید')[i][len(third_filtered_as_string.split('رید')[i]) - 1] == ' ' and third_filtered_as_string.split('رید')[i + 1][0] == ' ':
                                return False
            third_filtered_string_as_list = []
            for i in range(len(third_filtered_as_string.split())):
                third_filtered_string_as_list.append(
                    informal_normalizer.normalized_word(third_filtered_as_string.split()[i])[0])

            fourth_filtered_as_string = ' '.join(third_filtered_string_as_list)

            return fourth_filtered_as_string
        else:

            normalizer = Normalizer()
            informal_normalizer = InformalNormalizer()
            first_filtered_string = ''.join([char for char in raw_input_string if char not in string_punctuation])

            second_filtered_string = normalizer.character_refinement(first_filtered_string)

            third_filtered_string_as_list = []
            for i in range(len(second_filtered_string.split())):
                third_filtered_string_as_list.append(
                    informal_normalizer.normalized_word(second_filtered_string.split()[i])[0])

            third_filtered_as_string = ' '.join(third_filtered_string_as_list)

            return third_filtered_as_string
    else:
        normalizer = Normalizer()
        informal_normalizer = InformalNormalizer()
        first_filtered_string = ''.join([char for char in raw_input_string if char not in string_punctuation])

        second_filtered_string = normalizer.character_refinement(first_filtered_string)
        # print(second_filtered_string, 1000)

        third_filtered_as_string = ''
        for i in range(len(second_filtered_string)):
            if i == len(second_filtered_string) - 1:
                third_filtered_as_string += second_filtered_string[i]
            else:
                if second_filtered_string[i] != second_filtered_string[i + 1]:
                    third_filtered_as_string += second_filtered_string[i]
        # print(third_filtered_as_string, 234)
        third_filtered_string_as_list = []
        for i in range(len(third_filtered_as_string.split())):
            third_filtered_string_as_list.append(
                informal_normalizer.normalized_word(third_filtered_as_string.split()[i])[0])

        fourth_filtered_as_string = ' '.join(third_filtered_string_as_list)
        # print(fourth_filtered_as_string, 2000)

        return fourth_filtered_as_string


def with_no_space_check(s: str):
    exceptions = [['', ''], ['', ' '], [' ', ''], [' ', ' ']]
    if s.split('رید') in exceptions:
        return False, ''
    if len(s.split('رید')) > 1 and s.split('رید') not in exceptions:
        for i in range(len(s.split('رید'))):
            if i != len(s.split('رید')) - 1:
                if len(s.split('رید')[i]) > 0 and len(s.split('رید')[i + 1]) > 0:
                    if s.split('رید')[i][len(s.split('رید')[i]) - 1] == ' ' and s.split('رید')[i + 1][0] == ' ':
                        return False, ''
    pattern_for_specific_word = re.compile(r'((\b\u0631){2,}\u06cc\u062f|\b\s\u0631{2,}\u06cc\u062f|\u0631{2,}\u06cc\u062f)')
    matches_for_specific_word = pattern_for_specific_word.finditer(s)
    for match in matches_for_specific_word:
        if match:
            print(432)
            return False, ''
    m = text_cleaner(s)
    if not m:
        return False, ''
    else:
        lst = m.split()
        stanford_tagger = StanfordPOSTagger(model_filename='resources/persian.tagger',
                                            path_to_jar='resources/stanford-postagger.jar')

        my_list = stanford_tagger.tag(lst)
        my_dict = {}
        for i in range(len(my_list)):
            my_dict[my_list[i][0]] = my_list[i][1]

        for item in my_dict:
            for bad_word in bad_word_list:
                if item.find(bad_word) >= 0:

                    new_list = item.split(bad_word)
                    new_item = ''.join(item.split(bad_word))

                    if item in bad_word_list:
                        # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                        print(1)
                        return False, ''

                    if new_item in bad_word_list:
                        # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                        print(2)
                        return False, ''

                    pos_before_modification = my_dict[item]
                    pos_after_modification = stanford_tagger.tag([new_item])[0][1]

                    if len(new_list[0]) == 0 and len(new_list[1]) <= 3:
                        if new_list[1] == 'ا' or new_list[1] == 'یا' or new_list[1] == 'ها' or new_list[1] == 'تو' or new_list[1] == 'شو' or new_list[1] == 'م'\
                                or new_list[1] == 'مون' or new_list[1] == 'تون' or new_list[1] == 'شون':
                            # lenz_debug_logger(response_code=231101, action="action", bad_word=bad_word)
                            print(3)
                            return False, ''

                    if pos_before_modification == 'N' and pos_after_modification == 'N':
                        if len(new_list[0]) > 3 and len(new_list[1]) > 3:
                            # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                            print(4)
                            return False, ''
                        if ((len(new_list[0]) == 0 and len(new_list[1]) > 3) or (
                                len(new_list[0]) > 3 and len(new_list[1]) == 0)) and item not in third_list:
                            # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                            print(5)
                            return False, ''
                        if (len(new_list[0]) <= 2 and len(new_list[1]) == 0) and item not in third_list:
                            # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                            print(6)
                            return False, ''
                        if len(new_list[0]) == 0 and len(new_list[1]) <= 2 and item not in third_list:
                            # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                            print(7)
                            return False, ''
                        if len(new_item) <= 4 and item not in third_list:
                            value = -1
                            for word in third_list:
                                if item.find(word) == 0:
                                    value = 1
                                    break
                                else:
                                    continue
                            if value < 0:
                                # lenz_debug_logger(response_code=231101, action="action", keyword=item)
                                print(8)
                                return False, ''
        for bad_word in bad_word_list_separated:
            if bad_word in s:
                # lenz_debug_logger(response_code=231101, action="action", bad_word=bad_word)
                print(9)
                return False, ''

        final_string_to_be_returned = ''
        for i in lst:
            if i == lst[len(lst) - 1]:
                final_string_to_be_returned += i
            else:
                final_string_to_be_returned += i
                final_string_to_be_returned += ' '

        return True, final_string_to_be_returned


def regex_validity_check(s: str):
    persian_alpha_codepoints = '\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651' \
                               '\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC'
    persian_num_codepoints = '\u06F0-\u06F9'
    space_codepoints = '\u0020\u2000-\u200F\u2028-\u202F'

    pattern_1 = re.compile(r'([' + persian_alpha_codepoints + ']+[' + persian_num_codepoints + ']+)+')
    pattern_2 = re.compile(r'(\b([' + persian_alpha_codepoints + ']{1,2}([' + space_codepoints + '])+)){4,}')
    pattern_3 = re.compile(r'((\b\u06F0\u06F9|\b\u06F9)([' + persian_num_codepoints + '])|(\u06F0\u06F9|\u06F9)([' + persian_num_codepoints + '])|(\b[' + persian_num_codepoints + ']{4,9}[' + space_codepoints + ']*)|([' + persian_num_codepoints + ']{4,9}[' + space_codepoints + ']*))')
    # pattern_6 = re.compile(r'[' + persian_num_codepoints + ']{1,2}:[' + persian_num_codepoints + ']{1,2}')

    def regex_creation(word):
        return "(\\s|\\.)*".join(list(word)) + "(\\s|\\.)*"

    l1 = "|".join(list(map(regex_creation, bad_word_list)))
    l2 = "\\b" + "|\\b".join(list(map(regex_creation, bad_word_list_separated)))

    sss1 = "(" + l1 + ")"
    sss2 = "(" + l2 + ")"

    pattern_4 = re.compile(r'{}'.format(sss1))
    pattern_5 = re.compile(r'{}'.format(sss2))

    matches_1 = pattern_1.finditer(s)
    matches_2 = pattern_2.finditer(s)
    matches_3 = pattern_3.finditer(s)
    matches_4 = pattern_4.finditer(s)
    matches_5 = pattern_5.finditer(s)
    # matches_6 = pattern_6.finditer(s)

    for match in matches_1:
        if match:
            print(10)
            return False
    for match in matches_2:
        if match:
            print(11)
            return False
    for match in matches_3:
        if match:
            print(12)
            return False
    for match in matches_4:

        if s[match.span()[1] - 1] == ' ':
            i = match.span()[0] - 1
            j = match.span()[1] - 1
        else:
            i = match.span()[0] - 1
            j = match.span()[1]

        bad_word_found = s[match.span()[0]:j]
        p = s[match.span()[0]:j]

        while i >= 0 and s[i] != ' ':
            p = s[i] + p
            i -= 1
        while j < len(s) and s[j] != ' ':
            p = p + s[j]
            j += 1
        k = -1
        for white_word in third_list:
            if p in white_word or white_word in p:
                if bad_word_found in white_word:
                    k += 1
                    break
                else:
                    continue

        if k >= 0:
            k = 0
            continue
        if k < 0:
            print(13)
            return False

    for match in matches_5:
        if match:
            print(14)
            return False
    return True


def sentiment_user_comment(raw_input_string):
    boolean_part_output, string_part_output = with_no_space_check(raw_input_string)
    if boolean_part_output:
        return regex_validity_check(string_part_output)
    return boolean_part_output


t1 = time.time()
print(sentiment_user_comment(''))
t2 = time.time()
print(t2 - t1)
