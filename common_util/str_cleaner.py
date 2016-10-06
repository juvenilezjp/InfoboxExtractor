# coding=utf-8
import re


class StrCleaner:
    def __init__(self, string):
        self.str = string

    def baidu_words_clean(self):
        return re.sub('\n|编辑|\n|锁定|\xa0', '', self.str)


if __name__ == "__main__":
    str = StrCleaner("['\n张子君\n（哈尔滨演员）\n编辑\n锁定\n'] ['\n男\n', '\n演员\n', '\n娱乐人物\n', '\n大陆演员\n', '\n人物\n'] (['中文名', '国\xa0\xa0\xa0\xa0籍', '民\xa0\xa0\xa0\xa0族', '星\xa0\xa0\xa0\xa0座', '血\xa0\xa0\xa0\xa0型', '身\xa0\xa0\xa0\xa0高', '体\xa0\xa0\xa0\xa0重', '出生地', '出生日期', '职\xa0\xa0\xa0\xa0业', '毕业院校', '代表作品', '特\xa0\xa0\xa0\xa0长'], ['\n张子君\n', '\n中国\n', '\n汉\n', '\n水瓶座\n', '\nO型\n', '\n184cm\n', '\n70kg\n', '\n黑龙江哈尔滨\n', '\n2月14日\n', '\n演员\n', '\n北京电影学院\n', '\n《鲜花开满村庄》《星光都市》《政委》\n', '\n篮球、游泳、足球、驾驶\n'])")
    print(str.baidu_words_clean())