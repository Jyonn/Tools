from typing import Optional

from SmartDjango import Excp, ErrorCenter, E

Syllables = [
    'a', 'ba', 'ca', 'cha', 'chua', 'da', 'dia', 'fa', 'ga', 'gua', 'ha', 'hua', 'jia', 'ka', 'kua',
    'la', 'lia', 'ma', 'na', 'pa', 'qia', 'sa', 'sha', 'shua', 'ta', 'wa', 'xia', 'ya', 'za', 'zha',
    'zhua', 'ai', 'bai', 'cai', 'chai', 'chuai', 'dai', 'gai', 'guai', 'hai', 'huai', 'kai', 'kuai',
    'lai', 'mai', 'nai', 'pai', 'sai', 'shai', 'shuai', 'tai', 'wai', 'zai', 'zhai', 'zhuai', 'an',
    'ban', 'bian', 'can', 'chan', 'chuan', 'cuan', 'dan', 'dian', 'duan', 'fan', 'gan', 'guan',
    'han', 'huan', 'jian', 'juan', 'kan', 'kuan', 'lan', 'lian', 'luan', 'man', 'mian', 'nan',
    'nian', 'nuan', 'pan', 'pian', 'qian', 'quan', 'ran', 'ruan', 'san', 'shan', 'shuan', 'suan',
    'tan', 'tian', 'tuan', 'wan', 'xian', 'xuan', 'yan', 'yuan', 'zan', 'zhan', 'zhuan', 'zuan',
    'ang', 'bang', 'cang', 'chang', 'chuang', 'dang', 'fang', 'gang', 'guang', 'hang', 'huang',
    'jiang', 'kang', 'kuang', 'lang', 'liang', 'mang', 'nang', 'niang', 'pang', 'qiang', 'rang',
    'sang', 'shang', 'shuang', 'tang', 'wang', 'xiang', 'yang', 'zang', 'zhang', 'zhuang', 'ao',
    'bao', 'biao', 'cao', 'chao', 'dao', 'diao', 'gao', 'hao', 'jiao', 'kao', 'lao', 'liao', 'mao',
    'miao', 'nao', 'niao', 'pao', 'piao', 'qiao', 'rao', 'sao', 'shao', 'tao', 'tiao', 'xiao',
    'yao', 'zao', 'zhao', 'bei', 'dei', 'ei', 'fei', 'gei', 'hei', 'lei', 'mei', 'nei', 'pei',
    'rui', 'shei', 'tei', 'wei', 'zei', 'zhei', 'ben', 'cen', 'chen', 'den', 'en', 'fen', 'gen',
    'hen', 'ken', 'men', 'nen', 'pen', 'ren', 'sen', 'shen', 'wen', 'zen', 'zhen', 'beng', 'ceng',
    'cheng', 'deng', 'eng', 'feng', 'geng', 'heng', 'keng', 'leng', 'meng', 'neng', 'peng', 'reng',
    'seng', 'sheng', 'teng', 'weng', 'zeng', 'zheng', 'bi', 'di', 'ji', 'ju', 'li', 'lü', 'mi',
    'ni', 'nü', 'pi', 'qi', 'qu', 'ti', 'xi', 'xu', 'yi', 'yu', 'bie', 'die', 'jie', 'jue', 'lie',
    'lüe', 'mie', 'nie', 'nüe', 'pie', 'qie', 'que', 'tie', 'xie', 'xue', 'ye', 'yue', 'bin', 'jin',
    'jun', 'lin', 'min', 'nin', 'pin', 'qin', 'xin', 'xun', 'yin', 'yun', 'bing', 'ding', 'jing',
    'ling', 'ming', 'ning', 'ping', 'qing', 'ting', 'xing', 'ying', 'bo', 'chuo', 'cuo', 'duo',
    'fo', 'guo', 'huo', 'kuo', 'lo', 'luo', 'mo', 'nuo', 'o', 'po', 'ruo', 'shuo', 'suo', 'tuo',
    'wo', 'yo', 'zhuo', 'zuo', 'bu', 'chu', 'cu', 'du', 'fu', 'gu', 'hu', 'ku', 'lu', 'mu', 'nu',
    'pu', 'ru', 'shu', 'su', 'tu', 'wu', 'zhu', 'zu', 'ce', 'che', 'de', 'e', 'ge', 'he', 'ke',
    'le', 'me', 'ne', 're', 'se', 'she', 'te', 'ze', 'zhe', 'chi', 'ci', 'ri', 'shi', 'si', 'zhi',
    'zi', 'chong', 'cong', 'dong', 'gong', 'hong', 'jiong', 'kong', 'long', 'nong', 'qiong', 'rong',
    'song', 'tong', 'xiong', 'yong', 'zhong', 'zong', 'chou', 'cou', 'dou', 'fou', 'gou', 'hou',
    'kou', 'lou', 'mou', 'nou', 'ou', 'pou', 'rou', 'shou', 'sou', 'tou', 'zhou', 'zou', 'chui',
    'cui', 'dui', 'gui', 'hui', 'kui', 'shui', 'sui', 'tui', 'zhui', 'zui', 'chun', 'cun', 'dun',
    'gun', 'hun', 'kun', 'lun', 'qun', 'run', 'shun', 'sun', 'tun', 'zhun', 'zun', 'diu', 'jiu',
    'liu', 'miu', 'niu', 'qiu', 'xiu', 'you', 'er'
]

ToneJar = {
    'a': 'aāáǎà', 'o': 'oōóǒò', 'e': 'eēéěè', 'i': 'iīíǐì', 'u': 'uūúǔù', 'ü': 'üǖǘǚǜ',
}

ToneList = ['āōēīūǖ', 'áóéíúǘ', 'ǎǒěǐǔǚ', 'àòèìùǜ']


class PhraseServiceError(ErrorCenter):
    SYLLABLE_NOT_FOUND = E("找不到音节[{0}]", ph=E.PH_FORMAT)
    SYLLABLE_MULTIPLE_TONE = E("[{0}]音节存在多个声调", ph=E.PH_FORMAT)
    SYLLABLE_FORMAT = E("[{0}]音节格式错误{1}", ph=E.PH_FORMAT)


PhraseServiceError.register()


class PhraseService:
    @Excp.pack
    def toner(self, syllable: str, tone: Optional[int]) -> str:
        """将不带声调的音节和声调合并为带声调的音节"""
        syllable = syllable.replace('v', 'ü')
        syllable = syllable.replace('lue', 'lüe')
        syllable = syllable.replace('nue', 'nüe')
        if syllable not in Syllables:
            return PhraseServiceError.SYLLABLE_NOT_FOUND(syllable)

        if not tone:
            return syllable
        if 'a' in syllable:
            replaced = 'a'
        elif 'e' in syllable:
            replaced = 'e'
        elif 'i' in syllable:
            if 'u' not in syllable:
                replaced = 'i'
            else:
                replaced = 'iu'[syllable.find('i') < syllable.find('u')]
        elif 'o' in syllable:
            replaced = 'o'
        elif 'u' in syllable:
            replaced = 'u'
        else:
            replaced = 'ü'
        replacer = ToneJar[replaced][tone]

        syllable = syllable.replace(replaced, replacer)
        return syllable

    @staticmethod
    def _get_intersection(syllable_set: set, s: str):
        return syllable_set & set(s)

    @Excp.pack
    def format_syllable(self, syllable: str) -> str:
        """格式化不标准的音节"""
        syllable = syllable.lower()
        if not isinstance(syllable, str):
            return PhraseServiceError.SYLLABLE_FORMAT((syllable, ''))

        tone = None
        syllable_set = set(syllable)
        for index, tones in enumerate(ToneList):
            if self._get_intersection(syllable_set, tones):
                if tone:
                    return PhraseServiceError.SYLLABLE_MULTIPLE_TONE(syllable)
                tone = index + 1

        for replacer in ToneJar:  # ü居然不用在此处替换为v，ü.is_lower()也是True
            intersection = self._get_intersection(syllable_set, ToneJar[replacer][1:])
            for e in intersection:
                syllable = syllable.replace(e, replacer)

        formatted_syllable = ''.join(list(filter(lambda c_: c_.islower(), syllable)))
        for c in syllable:
            if c.islower():
                continue
            if c in '01234':
                if tone:
                    return PhraseServiceError.SYLLABLE_MULTIPLE_TONE(syllable)
                tone = int(c)
            else:
                return PhraseServiceError.SYLLABLE_FORMAT((syllable, '（存在非法字符）'))

        formatted_syllable = self.toner(formatted_syllable, tone)
        return formatted_syllable


phraseService = PhraseService()
