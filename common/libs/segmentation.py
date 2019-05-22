"""
中文分词,使用算法为
正向最大匹配法(Maximum Matching Method, 简称MM算法)
逆向最大匹配算法(Reverse Maximum Matching Method, 简称RMM算法)
最大概率分词算法
"""
import collections
import os


class Segmentation(object):
    def __init__(self):
        self.word_set = set(Segmentation.init_word_list(self.get_cwd() + "ChineseDic.txt"))
        self.word_frequency_dict = Segmentation.init_frequency_dict(self.get_cwd() + "WordFrequency.txt")
        self.sentence = ""  # 待划分句子
        self.seg_result_dict = {}  # 划分结果

    @staticmethod
    def get_cwd():
        return os.getcwd() + "/common/libs/"

    def set_sentence(self, sentence):
        if not isinstance(sentence, str):
            self.sentence = sentence.decode('utf8')
        else:
            self.sentence = sentence
        self.seg_result_dict = {}  # 初始化划分结果

    def get_result_dict(self):
        """
        获得分词结果字典
        :return:
        """
        return self.seg_result_dict

    def print_result(self):
        """
        输出分词结果
        :return:
        """
        print("分词算法  分词结果")
        for k, v in self.seg_result_dict.items():
            print('%6s:' % k, '|'.join(v))

    def mm_seg(self, max_len=6):
        """
        使用正向最大匹配法划分词语
        :param max_len: int 最大词长 默认为6
        """
        cur = 0  # 表示分词的位置
        seg_result = []
        sen_len = len(self.sentence)  # 句子的长度
        while cur < sen_len:
            length = None
            for length in range(max_len, 0, -1):
                if self.sentence[cur: cur + length] in self.word_set:
                    break
            seg_result.append(self.sentence[cur: cur + length])
            cur += length
        self.seg_result_dict['MM'] = seg_result

    def rmm_seg(self, max_len=6):
        """
        使用逆向最大匹配法划分词语
        :param max_len: int 最大词长 默认为6
        """
        sen_len = self.sentence.__len__()  # 句子的长度
        seg_result = []
        cur = sen_len  # 表示分词的位置
        while cur > 0:
            l = None
            if max_len > cur:
                max_len = cur
            for l in range(max_len, 0, -1):
                if self.sentence[cur - l: cur] in self.word_set:
                    break
            seg_result.insert(0, self.sentence[cur - l: cur])
            cur -= l
        self.seg_result_dict['RMM'] = seg_result

    def max_probability_seg(self):
        """
        使用概率最大分词算法进行分词
        """
        length = len(self.sentence)
        p = [0] * (length + 1)
        p[length] = 1
        div = [1] * (length + 1)
        t = [1] * length
        for i in range(length - 1, -1, -1):
            for k in range(1, length - i + 1):
                tmp = self.word_frequency_dict[self.sentence[i:i + k]]
                if k > 1 and tmp == 1:
                    continue
                if self.word_frequency_dict[self.sentence[i:i + k]] * p[i + k] * div[i] > p[i] * \
                        self.word_frequency_dict['_total_'] * div[i + k]:
                    p[i] = self.word_frequency_dict[self.sentence[i:i + k]] * p[i + k]
                    div[i] = self.word_frequency_dict['_total_'] * div[i + k]
                    t[i] = k
        i = 0
        seg_result = []
        while i < length:
            seg_result.append(self.sentence[i:i + t[i]])
            i += t[i]
        self.seg_result_dict['MP'] = seg_result

    @staticmethod
    def init_word_list(file_name):
        """
        读取词库txt, 返回词库列表
        :param file_name: 文件路径
        :return: 词库列表
        """
        with open(file_name, encoding='utf-8') as fd:
            lines = fd.readlines()
        word_list = []
        for line in lines:
            word_list.append(line.split(',')[0])
        return word_list

    @staticmethod
    def init_frequency_dict(file_name):
        """
        读取词库频率txt, 返回词-频率字典
        :param file_name: 文件路径
        :return: 词-频率字典
        """
        word_frequency_dict = collections.defaultdict(lambda: 1.0)
        with open(file_name, 'r', encoding='utf-8') as fd:
            total = 0
            while True:
                line = fd.readline()
                if not line:
                    break
                word = line.split(',')[0]
                freq = line.split(',')[2].strip('%\r\n')
                total += float(freq) + 1  # smooth
                try:
                    word_frequency_dict[word] = float(freq) + 1
                except UnicodeDecodeError:
                    word_frequency_dict[word] = float(freq) + 1
        word_frequency_dict['_total_'] = total
        return word_frequency_dict


if __name__ == '__main__':
    sen = '区块链在物联网的应用'
    seg = Segmentation()
    seg.set_sentence(sen)
    seg.mm_seg()  # MM
    seg.rmm_seg()  # RMM
    seg.max_probability_seg()  # 最大概率分词
    # r = seg.get_result_dict()  # 获得分词结果字典
    # print '|'.join(r['MM'])
    # print '|'.join(r['RMM'])
    # print '|'.join(r['MP'])
    # seg.print_result()  # 将分词结果输出
    print(seg.get_result_dict())
