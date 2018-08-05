#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import difflib
from poemtools import poemline


#VOWELS = 'аеиоуыэюя'
LETTERS_GROUP_PATTERN = '[бвгджзйклмнпрстфхцчшщъь]+|[а́еоуиыэюя]+'

ACUTUS = '́'

rules_for_consonants = {'дк': 'тк',
                        'сб': 'зб',
                        'тв': 'тв',
                        'вт': 'фт',
                        'вк': 'фк',
                        'бщ': 'пш',
                        'вс': 'фс',
                        'вт': 'фт',
                        'вч': 'фч',
                        'кд': 'гд',
                        'сб': 'зб',
                        'фг': 'вг',
                        'кз': 'гз',
                        'сг': 'зг',
                        'тб': 'дб',
                        'бб': 'б',
                        'пб': 'б',
                        'бп': 'п',
                        'вв': 'в',
                        'вф': 'ф',
                        'дд': 'д',
                        'дт': 'д',
                        'тт': 'т',
                        'тд': 'т',
                        'зз': 'з',
                        'сз': 'з',
                        'сс': 'с',
                        'зс': 'с',
                        'нн': 'нм',
                        'тс': 'ц',
                        'тьс': 'ц',
                        'мм': 'м',
                        'сс': 'с',
                        'пп': 'п',
                        'тт': 'т',
                        'кк': 'к',
                        'лл': 'л',
                        'сж': 'ж',
                        'зж': 'ж',
                        'сш': 'ш',
                        'зш': 'ш',
                        'зж': 'ж',
                        'жж': 'ж',
                        'ждь': 'шть',
                        'жд': 'жд',
                        'сч': 'сч',
                        'зч': 'зч',
                        'жч': 'щ',
                        'сщ': 'щ',
                        'зщ': 'щ',
                        'тц': 'ц',
                        'дц': 'ц',
                        'тск': 'цк',
                        'дск': 'цк',
                        'тч': 'ч',
                        'дч': 'ч',
                        'чн': 'чн',
                        'кт': 'кт',
                        'стн': 'сн',
                        'здн': 'зн',
                        'стл': 'сл',
                        'стк': 'стк',
                        'здк': 'здк',
                        'стск': 'с',
                        'нтк': 'нтк',
                        'ндк': 'ндк',
                        'нтск': 'нцк',
                        'ндск': 'нцк',
                        'вств': 'фств',
                        'рдц': 'рц',
                        'рдч': 'рч',
                        'лнц': 'нц',
                        'вск': 'фск',
                        'жск': 'шск'}
rules_for_cons_at_the_end = {'б': 'п',
                             'в': 'ф',
                             'г': 'к',
                             'д': 'т',
                             'ж': 'ш',
                             'з': 'с',
                             'здь': 'сть'}
rules_for_vowels = {'ё': 'йо',
                    'ю': 'йу',
                    'я': 'йа',
                    'Ё': 'йО',
                    'Ю': 'йУ',
                    'Я': 'йА'}
consonance_rules = {'б': 'п',
                    'в': 'ф',
                    'г': 'к',
                    'д': 'т',
                    'ж': 'ш',
                    'з': 'с',
                    'м': 'н',
                    'р': 'л',
                    'х': 'к',
                    'щ': 'ш'}


def pseudophonetic_representation(clause):
    phon = []
    letters_group = re.findall(LETTERS_GROUP_PATTERN, clause)
    ltg_len = len(letters_group)
    for num, lgroup in enumerate(letters_group, start=1):
        if lgroup in rules_for_consonants.keys():
            lgroup = rules_for_consonants[lgroup]
        elif lgroup in rules_for_vowels.keys():
            lgroup = rules_for_vowels[lgroup]
        if lgroup in rules_for_cons_at_the_end.keys() and num == ltg_len:
            lgroup = rules_for_cons_at_the_end[lgroup]
        phon.append(lgroup)
    return phon

def consonance_form(word):
    translated_word = []
    word_as_letters = re.findall('[абвгдежзийклмнопрстуфхцчшщъыьэюя]', word)
    for ltr in word_as_letters:
        if ltr in consonance_rules.keys():
            ltr = consonance_rules[ltr]
        translated_word.append(ltr)
    return translated_word

def consonance(c1, c2):
    c1 = consonance_form(c1)
    c2 = consonance_form(c2)
    if difflib.SequenceMatcher(None, c1, c2).ratio() >= 0.5:
        return True
    return False

def alike(first_clause, second_clause):
    '''
    Сравнение клаузул для поиска рифм.
    '''
    #stressed_vowel_1 = first_clause[first_clause.index(ACUTUS)-1]
    #stressed_vowel_2 = second_clause[second_clause.index(ACUTUS)-1]
    #if stressed_vowel_1 != stressed_vowel_2:
        #return False
    #ph_1 = pseudophonetic_representation(first_clause)
    #ph_2 = pseudophonetic_representation(second_clause)
    if difflib.SequenceMatcher(None, first_clause, second_clause).ratio() >= 0.5:
        return True
    else:
        return consonance(first_clause, second_clause)
    return False

def verse_info(verse, versename):
    '''
    Обрабатывает строфы, т.е. несколько стихотворных строк,
    собранных вместе.
    Возвращает список кортежей, содержащих информацию о каждой из строк.
    Кортеж с первым элементом равном нулю описывает вообще стихотворение:
    (0, versename, verse_len, stress_scheme)
    Здесь 0 просто условный указатель,
          versename — имя стихотворения,
          verse_len — общее число строк,
          stress_scheme — схема ударений
    Остальные элементы имеют следующий вид:
    (num (rhyme, [(rhyme1, num1), (rhyme2, num2), ...]))
    Здесь num — номер строки,
          rhyme — рифма, т.е. слова, содержащие клаузул, в этой строке,
          rhyme1 — слово в другой строке, с которым рифмуется rhyme,
          num1 — номер строки, в которой содержится rhyme1,
          rhyme2 и num2 — ещё одни рифма и номер строки с ней.
    Поскольку строк, с которыми рифмуется текущая может быть несколько,
    список может тоже содержать несколько кортежей вида (rhyme, num).
    '''

    info_list = []

    # Общая информация о стихотворении.
    verse_len = len(verse)
    #verse_general_info = (0, versename, verse_len)
    #info_list.append(verse_general_info)
    stress_scheme = ['-'] * verse_len

    # Обрабатываем каждую стихотворную строку.
    # Для этого сравниваем её клаузулу с клаузулами всех остальных
    for line_index, line in enumerate(verse, start=1):
        linfo = []
        pl_obj_first = poemline(line)
        for other_line_index, other_line in enumerate(verse, start=1):
            # Проверяем индекс.
            if other_line_index != line_index:
                pl_obj_second = poemline(other_line)
                clause_of_line = pl_obj_first.clause()
                clause_of_other_line = pl_obj_second.clause()
                if alike(clause_of_line, clause_of_other_line):
                    linfo.append((pl_obj_second.clause_as_words(),
                                 other_line_index))
                    stress_place_1 = stress_scheme[line_index-1]
                    stress_place_2 = stress_scheme[other_line_index-1]
                    if stress_place_1 == '-' or stress_place_2 == '-':
                        stress_scheme[line_index-1] = line_index
                        stress_scheme[other_line_index-1] = line_index
        info_list.append((line_index, (pl_obj_first.clause_as_words(), linfo)))

    stress_scheme = ''.join([str(i) for i in stress_scheme])
    verse_general_info = (0, versename, verse_len, stress_scheme)
    info_list.insert(0, verse_general_info)
     
    return info_list


if __name__ == '__main__':
    st = ['Не ве́тер бушу́ет над бо́ром,', 'Не с го́р побежа́ли ручьи́ -',
          'Моро́з-воево́да дозо́ром', 'Обхо́дит владе́нья свои́.', 'Моро́з-воево́да позо́ром',
          'Моро́з-воево́да дозо́ром']
    print(verse_info(st, 'NEKR'))
    for i in verse_info(st, 'NEKR'):
        if i[0] != 0:
            line_num =  i[0]
            rhyme = i[1][0]
            rhymes_with = i[1][1]
            for rh in rhymes_with:
                print('Строка ', line_num, ': ', rhyme, ' рифмуется с ', rh[0], ' из ', rh[1], ' строки.')
    #s = 'воздух'
    #s1 = 'востки'
    #print(pseudophonetic_representation(s))
    #print(pseudophonetic_representation(s1))
    #print(consonance(s, s1))

