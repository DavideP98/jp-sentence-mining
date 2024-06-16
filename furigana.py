#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import unicodedata
import pykakasi


def is_kanji(ch):
    try:
        return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(ch)
    except:
        return False


def is_hiragana(ch):
    try:
        return 'HIRAGANA' in unicodedata.name(ch)
    except:
        return False


def split_okurigana_reverse(text, hiragana):
    """ 
      tested:
        お茶(おちゃ)
        ご無沙汰(ごぶさた)
        お子(こ)さん
    """
    yield (text[0],)
    yield from split_okurigana(text[1:], hiragana[1:])


def split_okurigana(text, hiragana):
    """ 送り仮名 processing
      tested: 
         * 出会(であ)う
         * 明(あか)るい
         * 駆(か)け抜(ぬ)け
    """
    if is_hiragana(text[0]):
        yield from split_okurigana_reverse(text, hiragana)
    if all(is_kanji(_) for _ in text):
        yield text, hiragana
        return
    text = list(text)
    ret = (text[0], [hiragana[0]])
    for hira in hiragana[1:]:
        for char in text:
            if hira == char:
                text.pop(0)
                if ret[0]:
                    if is_kanji(ret[0]):
                        yield ret[0], ''.join(ret[1][:-1])
                        yield (ret[1][-1],)
                    else:
                        yield (ret[0],)
                else:
                    yield (hira,)
                ret = ('', [])
                if text and text[0] == hira:
                    text.pop(0)
                break
            else:
                if is_kanji(char):
                    if ret[1] and hira == ret[1][-1] and len(text) > 1:
                        text.pop(0)
                        yield ret[0], ''.join(ret[1][:-1])
                        yield char, hira
                        ret = ('', [])
                        try:
                            text.pop(0)
                        except e:
                            print("Problem: {} with {}".format(e,text))
                    else:
                        ret = (char, ret[1]+[hira])
                else:
                    # char is also hiragana
                    if hira != char:
                        break
                    else:
                        break


def split_furigana(text):
    """ Change from MeCab to pykakasi
    """
    ret = []
    kks = pykakasi.kakasi()
    result = kks.convert(text + '人')
    for item in result:
        if any(is_kanji(_) for _ in item['orig']):
            for pair in split_okurigana(item['orig'], item['hira']):
                ret += [pair]
        else:
            ret += [(item['orig'],)]
    ret.pop()
    return ret


def to_html(text):
    text2 = ""
    for pair in split_furigana(text):
        if len(pair)==2:
            kanji,hira = pair
            text2 += "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(kanji, hira)
        else:
            text2 += pair[0]
    return text2


def to_plaintext(text):
    text2 = ""
    for pair in split_furigana(text):
        if len(pair)==2:
            kanji,hira = pair
            text2 += "%s(%s)" % (kanja,hira)
        else:
            text2 += pair[0]
    return text2

def print_plaintext(text):
    print(to_plaintext(text))
 
def print_html(text):
    print(to_html(text))

def main():
    text = sys.argv[1]
    print_html(text)


if __name__ == '__main__':
    main()

