# !/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
from gensim import corpora, models


class Parser:

    def __init__(self, stopWordsPath, text):
        #加载停用词
        self.stopWords = self.getStopWords(stopWordsPath)
        self.text_cutted = ''#分词后文本
        self.text_cutted_clean = []#分词后文本，去除停用词和特殊字符
        self.text_clean = ''
        cutted = self.splitWords(text)
        cutted_clean = list(filter(lambda i: i not in self.stopWords, cutted))
        cutted_clean = list(filter(lambda i: i.isalnum(), cutted_clean))
        self.text_cutted = cutted
        self.text_clean = ''.join(cutted_clean)

    def getTopCountwords(self, news_text):
        cutted = self.splitWords(news_text)
        cutted_clean = list(filter(lambda i: i not in self.stopWords, cutted))
        cutted_clean = list(filter(lambda i: i.isalnum(), cutted_clean))
        uniqueWords = list(set(cutted_clean))
        keywords = [{'word': word, 'count': cutted_clean.count(word)} for word in uniqueWords]

        keywords = sorted(keywords, key=lambda x: -x['count'])
        print(str(keywords))
        return (keywords, len(cutted))


    def getSentenceLengthScore(self, sentence, ideal):
        return 1 - min(abs(ideal - len(sentence)), ideal) / ideal

    # Jagadeesh, J., Pingali, P., & Varma, V. (2005). Sentence Extraction Based Single Document Summarization. International Institute of Information Technology, Hyderabad, India, 5.
    def getSentencePositionScore(self, i, sentenceCount):
        normalized = i / (sentenceCount * 1.0)

        if normalized >= 0 and normalized <= 0.1:
            return 0.17
        elif normalized > 0.1 and normalized <= 0.2:
            return 0.23
        elif normalized > 0.2 and normalized <= 0.3:
            return 0.14
        elif normalized > 0.3 and normalized <= 0.4:
            return 0.08
        elif normalized > 0.4 and normalized <= 0.5:
            return 0.05
        elif normalized > 0.5 and normalized <= 0.6:
            return 0.04
        elif normalized > 0.6 and normalized <= 0.7:
            return 0.06
        elif normalized > 0.7 and normalized <= 0.8:
            return 0.04
        elif normalized > 0.8 and normalized <= 0.9:
            return 0.04
        elif normalized > 0.9 and normalized <= 1.0:
            return 0.15
        else:
            return 0

    def getTitleScore(self, title, sentence):
        titleWords = self.removeStopWords(title)
        sentenceWords = self.removeStopWords(sentence)
        matchedWords = [word for word in sentenceWords if word in titleWords]
        matchedWords = list(matchedWords)
        return (len(matchedWords) + 1) / (len(matchedWords) + 2) / len(title)  # 拉普拉斯平滑

    """
    分句，还可以将分词后的单词又还原成句子
    """

    def splitSentences(self, sentence):
        delimiters = frozenset(u'。！？')
        buf = []
        for ch in sentence:
            buf.append(ch)
            if delimiters.__contains__(ch):
                yield ''.join(buf)
                buf = []
        if buf:
            yield ''.join(buf)

    #用结巴分词分词
    def splitWords(self, sentence):
        return list(jieba.cut(sentence))


    def removePunctations(self, text):
        return ''.join(t for t in text if t.isalnum() or t == ' ')

    def removeStopWords(self, words):
        return [word for word in words if word not in self.stopWords]

    def getStopWords(self, stopPath):
        with open(stopPath, encoding="UTF-8") as file:
            words = file.readlines()

        return [word.replace('\n', '') for word in words]