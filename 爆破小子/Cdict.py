#!/usr/bin/env python3

import argparse
import textwrap
import sys
import threading
import string
import random
import secrets


class PasswordGenerator:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog='PassWord Generator',
            description='The production company Wuyue',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(
                '''Example:
                Cdict.py -n 姓:名 -l 10                              #姓名信息为必须参数,密码默认长度为8
                Cdict.py -n 姓:名 -b 1999.01.01 -l 10                #姓名和生日信息,设置长度10
                Cdict.py -n 姓:名 -b 1999.01.01 -p 18999999999       #手机号
                Cdict.py -n 姓:名 -b 1999.01.01 -q 123456            #qq号码
                Cdict.py -n 姓:名 -b 1999.01.01 -e 123456@163.com    #邮箱信息 
                Cdict.py -n 姓:名 -s true                            #启用特殊字符
                '''
            ))
        self.parser.add_argument('-n', '--name', required=True, help='小写字母姓名')
        self.parser.add_argument('-b', '--birthday', help='生日格式为:1990.01.01')
        self.parser.add_argument('-p', '--phone', help='手机号', type=str)
        self.parser.add_argument('-q', '--qq', help='完整qq号')
        self.parser.add_argument('-e', '--email', help='完整邮箱地址')
        self.parser.add_argument(
            '-s', '--special', default=False, type=bool, help='特殊字符默认不启用, 设置为true将启用')
        self.parser.add_argument('-l', '--length', default=8,
                                 type=int, help='默认是密码长度是8')
        self.parser.add_argument(
            '-c', '--count', default=1000, type=int, help='生成密码个数,默认1000')
        self.args = self.parser.parse_args()

        # 定义处理函数
        self.handler_name = self.handler_name(self.args.name)
        self.handler_birthday = self.handler_birthday(self.args.birthday)
        self.handler_phone = self.handler_phone(self.args.phone)
        self.handler_qq = self.handler_qq(self.args.qq)
        self.handler_email = self.handler_email(self.args.email)
        self.handler_special = self.handler_special(self.args.special)

        # 定义处理函数与参数的映射关系
        self.handlers = {
            'name': self.handler_name,
            'birthday': self.handler_birthday,
            'phone': self.handler_phone,
            'qq': self.handler_qq,
            'email': self.handler_email,
            'special': self.handler_special
        }

    # 根据用户输入参数获取wordlist，然后调用生成密码函数返回密码
    def generate_password(self, count):
        wordlist = []
        passwords = []
        for arg_name in self.handlers.keys():
            if getattr(self.args, arg_name):
                wordlist += self.handlers[arg_name]
        for _ in range(count):
            passwords.append(self.generate_password_from_wordlist(
                wordlist, self.args.length, self.handler_special))
        print(passwords)
        return passwords

    # 从wordlist中生成密码
    def generate_password_from_wordlist(self, wordlist, length, special):
        password = ''.join(secrets.choice(wordlist + special)
                           for _ in range(length))
        return password[:length+1]

    # 处理用户输入的姓名信息
    def handler_name(self, name):
        name = name.split(':')
        return name

    # 处理手机信息
    def handler_phone(self, phone):
        if not phone:
            return []
        phone = list(phone)
        return phone[-4:]

    # 处理生日信息
    def handler_birthday(self, birthday):
        if not birthday:
            return []
        return birthday.split('.')

    # 处理qq信息
    def handler_qq(self, qq):
        if not qq:
            return []
        return list(qq)

    # 处理email信息
    def handler_email(self, email):
        if not email:
            return []
        emails = email.split('@')
        return list(emails[0])

    # 处理特殊字符
    def handler_special(self, special):
        if special:
            specials = ['.', '@', '&']
            return specials
        return []

    # 多线程
    def threads(self):
        for _ in range(20):
            thread = threading.Thread(
                target=self.generate_password, args=(int(self.args.count/20),))
            thread.start()

    # 主函数
    def main(self):
        self.threads()


if __name__ == '__main__':
    passwordgenertor = PasswordGenerator()
    passwordgenertor.main()
