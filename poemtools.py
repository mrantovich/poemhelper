#!/usb/bin/env python3
# -*- encoding: utf-8 -*-


__all__ = ['poemline']


import re
from operator import truth


# Ударные гласные.
# Не уверен, что в будущем понадобится.
STRESSED_VOWELS = 'а́е́ёи́о́у́ы́э́ю́я́'

# Согласные.
CONSONANTS = 'бвгджзйклмнпрстфхцчшщъь'

# Пунктуационные символы и пробел. При обработке строки в них нет надобности.
PUNCTUATION_MARKS = [',', '.',  ':',  ';',  '—',  '-',  '!',  '?', 
                     '!..',  '?..',  '…',  ' ',  '\'', '"', '«',  '»']

# Акцент. Необходим для составления схемы ударений
# и нахождения клаузулы с анакрузой.
ACUTUS = '́'

# Шаблоны для размеров.
METRES = {'DI': [('iambus', '0[01]'),
                 ('choree', '[01]0')],
          'TRI': [('dactyl', '[01]00'),
                  ('amphibrach', '0[01]0'),
                  ('anapest', '00[01]')]}
# Шаблоны для каталектических окончаний.
DIMETER_R = {'iambus': '0',
             'choree': '[01]'}
TRIMETER_R = {2: {'dactyl': '[01]0',
                  'amphibrach': '0[01]',
                  'anapest': '00'},
              1: {'dactyl': '[01]',
                  'amphibrach': '0',
                  'anapest': '0'}}


class _PoemLine:
    '''
    Класс для обработки стихотворной строки.
    Позволяет получить нужную нам о ней информацию.
    Класс не используется напрямую.
    Следует обратиться к функции poemline.
    '''
    def __init__(self, line):
        # Приводим строку в нижний регистр.
        line = line.lower()
        self.original_line = line

        # «Склеиваем» буквы строки, удаляя лишние символы.
        self.glued_line = self._remove_symbols(line, PUNCTUATION_MARKS)
        
        # Преобразуем строку, удаляя согласные.
        # В итоге — строка из одних гласных.
        self.line_as_vowels = self._remove_symbols(self.glued_line, CONSONANTS)

    def clause(self):
        # Определяет клаузулу, т.е. буквы от последнего ударного гласного
        # до конца строки.
        # Возвращает строку без пунктуационных символов и пробелов.
        clause = ''
        i = self.glued_line.rfind(ACUTUS)
        if i != -1:
            clause = self.glued_line[i-1:]
        return clause

    def clause_as_words(self):
        # Возвращает слова, содержащие клаузулу.
        clause_as_words = ''
        i = self.original_line.rfind(ACUTUS)
        if i != -1:
            while i>0:
                if self.original_line[i-1] in PUNCTUATION_MARKS:
                    break
                i -= 1
            clause_as_words = self.original_line[i:]
        clause_as_words = self._remove_symbols(clause_as_words, PUNCTUATION_MARKS)
        return clause_as_words

    def anacrusis(self):
        # Возвращает анакрузу, т.е. буквы от начала слова до первого ударного гласного.
        anacrusis = ''
        i = self.glued_line.find(ACUTUS)
        if i != -1:
            anacrusis = self.glued_line[:i+1]
        return anacrusis

    def metre(self):
        # Определяет возможные размеры.
        # Возвращает список со словами iambus, choree, dactyl, amphibrach
        # или anapest.
        possible_metres = []
        
        # Длина стопы в диметрах и триметрах.
        dimeter_len = 2
        trimeter_len = 3

        str_scheme = self.stress_scheme()
        str_scheme_len = len(str_scheme)

        # Определяем, сколько стоп с стихотворной строке, и смотрим,
        # есть ли каталектическое окончание.
        # Ямб и хорей.
        dimeter_count, dimeter_remainder = divmod(str_scheme_len, dimeter_len)
        # Дактиль, амфибрахий и анапест.
        trimeter_count, trimeter_remainder = divmod(str_scheme_len, trimeter_len)

        # Проверяем, какой схеме ударений соответствует наша строка.
        # Добавляем в список возможных размеров ключевое слово,
        # если строка соответствует шаблону.
        # Диметры.
        for m in METRES['DI']:
            dimeter = m[1]
            dimeter_name = m[0]
            dimeter_scheme = dimeter * dimeter_count
            if dimeter_remainder:
                r = DIMETER_R[dimeter_name]
                dimeter_scheme += r
            if truth(re.match(dimeter_scheme, str_scheme)):
                possible_metres.append(dimeter_name)
        # Триметры.
        for m in METRES['TRI']:
            trimeter = m[1]
            trimeter_name = m[0]
            trimeter_scheme = trimeter * trimeter_count
            if trimeter_remainder:
                r = TRIMETER_R[trimeter_remainder][trimeter_name]
                trimeter_scheme += r
            if truth(re.match(trimeter_scheme, str_scheme)):
                possible_metres.append(trimeter_name)

        return possible_metres

    def stress_scheme(self):
        # Возвращает схему ударений в строке.
        # 0 — неударный слог.
        # 1 — ударный слог.

        metre_scheme = []
        
        # Ищем акцент в строке и заменяем его и предшествующий гласный единицей.
        # Остальное заменяем нулём.
        for vowel in self.line_as_vowels:
            if vowel == ACUTUS:
                i = 1
                metre_scheme.pop()
            else:
                i = 0
            metre_scheme.append(i)
        stress_sheme = ''.join(str(elem) for elem in metre_scheme)

        return stress_sheme

    def _remove_symbols(self, line, symbols_list=[]):
        # Удаление ненужных символов из строки.
        line_without = ''.join(filter(
                               lambda c: c not in symbols_list, line))
        return line_without


def poemline(line):
    '''
    Конвертирует строку с расставленными ударениями в объект _PoemLine
    и возвращает его.
    '''
    pl = _PoemLine(line)
    return pl


if __name__ == "__main__":
    s1 = 'Мои́ боги́ни! что́ вы? где́ вы?'
    s2 = 'Выхожу́ оди́н я на доро́гу...'
    s3 = 'Ту́чки небе́сные, ве́чные стра́нники…'
    s4 = 'Не с го́р побежа́ли ручьи́'
    s5 = 'О, весна́ без конца́ и без кра́ю —'
    sl = [s1, s2, s3, s4, s5]
    for s in sl:
        print('СТРОКА: %s' % s)
        spl = poemline(s)
        print('КЛАУЗУЛА: %s' % spl.clause())
        print('КЛАУЗУЛА(слова): %s' % spl.clause_as_words())
        print('АНАКРУСА: %s' % spl.anacrusis())
        print('РАЗМЕР: %s' % spl.metre())
        print('СХЕМА: %s' % spl.stress_scheme())

