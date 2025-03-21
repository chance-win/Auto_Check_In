'''
new Env('夸克自动签到')
cron: 0 9 * * *

V2版-目前有效
使用移动端接口修复每日自动签到，移除原有的“登录验证”，参数有效期未知

V1版-已失效
受大佬 @Cp0204 的仓库项目启发改编
源码来自 GitHub 仓库：https://github.com/Cp0204/quark-auto-save
提取“登录验证”“签到”“领取”方法封装到下文中的“Quark”类中

Author: BNDou
Date: 2024-03-15 21:43:06
LastEditTime: 2024-08-03 21:07:27
FilePath: \Auto_Check_In\checkIn_Quark.py
Description: 
抓包流程：
    【手机端】
    ①打开抓包，手机端访问签到页
    ②找到url为 https://drive-m.quark.cn/1/clouddrive/capacity/growth/info 的请求信息
    ③复制url后面的参数: kps sign vcode 粘贴到环境变量
    环境变量名为 COOKIE_QUARK 多账户用 回车 或 && 分开
    user字段是用户名 (可是随意填写，多账户方便区分)
    例如: user=张三; kps=abcdefg; sign=hijklmn; vcode=111111111;
'''
#import os
import re
import sys

import requests

# 测试用环境变量
# os.environ['COOKIE_QUARK'] = ''

try:  # 异常捕捉
    from utils.notify import send  # 导入消息通知模块
except Exception as err:  # 异常捕捉
    print('%s\n❌加载通知服务失败~' % err)


# 获取环境变量
def get_env():
    # 判断 COOKIE_QUARK是否存在于环境变量
    # `user=张三; kps=abcdefg; sign=hijklmn; vcode=111111111`
    # if "COOKIE_QUARK" in os.environ:
    #     # 读取系统变量以 \n 或 && 分割变量
    #     cookie_list = re.split('\n|&&', os.environ.get('COOKIE_QUARK'))
    # else:
    #     # 标准日志输出
    #     print('❌未添加COOKIE_QUARK变量')
    #     send('夸克自动签到', '❌未添加COOKIE_QUARK变量')
    #     # 脚本退出
    #     sys.exit(0)
    cookie_list = [handle_cookie()]
    return cookie_list

def handle_cookie():
    #original_string = "kps=AAQTVJeN1xwqSXc0YyjfUyIhsX+9wfWF5g1S4HhQJBLzf1jnyfprx5WaCth+vS+A0CJZb63iBH+N9Cr5tqxX98A0F6btcdotWeYcmtI+InhR5A==&sign=AATga5OMpRt8/1OYapev7ESgd41RJi4eO4UkkPUDGaWKIvcpTsXwrZcu8xVUUZu9VWE=&vcode=1726371680722"
    #original_string = "kps=AAR/GVHmrsd+yl5hmq3lmhhFIUgMMuKWV69URRmdhCf1RDPqv12FX2QrbY2xH449RiEnQaKP0OreKYYX3q6KcerHbEQvZ/6YJhdKt0EiuVaQcw==&kps_wg=AAR/GVHmrsd+yl5hmq3lmhhFIUgMMuKWV69URRmdhCf1RDPqv12FX2QrbY2xH449RiEnQaKP0OreKYYX3q6KcerHbEQvZ/6YJhdKt0EiuVaQcw==&sign_wg=AAT9AuAgyOIGzwAm068GPjSdOu/3x7WIa+iuQR1WSGIdd623j1dk+9otd918ICgYoco=&vcode=1730450866099&sign=AAT9AuAgyOIGzwAm068GPjSdOu/3x7WIa+iuQR1WSGIdd623j1dk+9otd918ICgYoco=&uc_param_str=mtdsdnfrpfbivesscpgimibtbmnijblauputogpintnwktprsvwiod&mt=CLUBDtZLPLw6/QKS5pwr23dArysyShRb&ds=AAPK+nmkWFEon/JCIglHTIoNen2FwTAyZWdd78fsJg4UsQ==&dn=62579636126-b22471b8&fr=android&pf=3300&bi=35825&ve=7.4.5.680&ss=411x864&pc=AAQRAtQtd9XY54gmHPf775eHIN6swUKF%2B1NzFjXzGOz0ke756TDJUc5m5Xx3UdNOjwbIFKahG8dFeDdpojTZFfx0&gi=bTkwBNZ6etXwhZIA9j6Hkb2to%2Fy4&mi=23113RKC6C&ni=bTkwBCzQpdTADiEAMW0kyEh633MzTvnxIXn3c4iU5veg8Dw=&la=zh&ut=AAPK+nmkWFEon/JCIglHTIoNen2FwTAyZWdd78fsJg4UsQ==&nt=6&nw=0&kt=4&pr=ucpro&sv=release&od=AARh2cvxNL%2FHHSZgKijBS2sN6xKMTxSU3QIPm6o%2BPuvgPQ%3D%3D"
    #original_string = "kps=AAQi+sJbRSBq2Gw+j8zO61K8QQHwfhCBHISk4tZspkiIiOy8yLXz+PRXbwlQTaQ8VUmo0VmzHHqMAUL/PwvBmz3WeW61biIQIDYOdYZtVplD1Q==&sign=AASfUkl5DDWPRoLEauktBvqJWeIqoXu2jM/b9lDp6zEu5Ur5rnIeoIIEdlLtn5J21BU=&vcode=1739874869460"
    #parts = original_string.split('&')

    #processed_string = 'user=wx; ' + '; '.join(parts)
    original_string = "sign_cyclic=true&kps=AAROFd31muoSdHHVbV6iZW9bOX3ihMlD6Nt5WXkZDxkRl4uh63inNThtqHloH19eVnLQY0UjgRSezS8+yYzkXHN3mnwK6GCdR3L0JkAymuFC/Q==&sign=AATUKL4ET3YCw5kwJHA4MjFTxEXLMI0j3+dH7cWMGfeTeG4po2rIGbnNZcYT/rnZjDo=&vcode=1742554136978&..."


    # 使用正则表达式提取需要的值
    kps_match = re.search(r'kps=([^&]+)', original_string)
    sign_match = re.search(r'sign=([^&]+)', original_string)
    vcode_match = re.search(r'vcode=([^&]+)', original_string)

    kps_value = kps_match.group(1) if kps_match else ''
    sign_value = sign_match.group(1) if sign_match else ''
    vcode_value = vcode_match.group(1) if vcode_match else ''

    # 拼接字符串
    processed_string = f'user=wx; kps={kps_value}; sign={sign_value}; vcode={vcode_value}'
    print(processed_string)
    return processed_string

class Quark:
    '''
    Quark类封装了签到、领取签到奖励的方法
    '''
    def __init__(self, user_data):
        '''
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        '''
        self.param = user_data

    def convert_bytes(self, b):
        '''
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回 MB GB TB
        '''
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024
            i += 1
        return f"{b:.2f} {units[i]}"

    def get_growth_info(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        response = requests.get(url=url, params=querystring).json()
        #print(response)
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        data = {"sign_cyclic": True}
        response = requests.post(url=url, json=data, params=querystring).json()
        #print(response)
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def queryBalance(self):
        '''
        查询抽奖余额
        '''
        url = "https://coral2.quark.cn/currency/v1/queryBalance"
        querystring = {
            "moduleCode": "1f3563d38896438db994f118d4ff53cb",
            "kps": self.param.get('kps'),
        }
        response = requests.get(url=url, params=querystring).json()
        print(response)
        if response.get("data"):
            return response["data"]["balance"]
        else:
            return response["msg"]

    def do_sign(self):
        '''
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        '''
        msg, log = "", ""
        # 每日领空间
        growth_info = self.get_growth_info()
        if growth_info:
            log += (
                f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
                f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
                f"签到累计容量：")
            if "sign_reward" in growth_info['cap_composition']:
                log += f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
            else:
                log += "0 MB\n"
            if growth_info["cap_sign"]["sign_daily"]:
                log += (
                    f"✅ 签到日志: 今日已签到+{self.convert_bytes(growth_info['cap_sign']['sign_daily_reward'])}，"
                    f"连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})\n"
                )
            else:
                sign, sign_return = self.get_growth_sign()
                if sign:
                    log += (
                        f"✅ 执行签到: 今日签到+{self.convert_bytes(sign_return)}，"
                        f"连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})\n"
                    )
                else:
                    log += f"❌ 签到异常: {sign_return}\n"
        else:
            log += f"❌ 签到异常: 获取成长信息失败\n"
        print(log)
        # 查询抽奖余额
        balance = self.queryBalance()
        if isinstance(balance,int):
            if balance > 0:
                log += f"还剩{balance}次抽奖"
            else:
                log += f"暂无抽奖次数"
            msg += log + ", 抽奖功能暂未开发\n"
        else:
            msg += log + balance + "\n"

        return msg


def main():
    '''
    主函数
    :return: 返回一个字符串，包含签到结果
    '''
    msg = ""
    global cookie_quark
    cookie_quark = get_env()

    print("✅ 检测到共", len(cookie_quark), "个夸克账号\n")

    i = 0
    while i < len(cookie_quark):
        # 获取user_data参数
        user_data = {}  # 用户信息
        for a in cookie_quark[i].replace(" ", "").split(';'):
            if not a == '':
                user_data.update({a[0:a.index('=')]: a[a.index('=') + 1:]})
        # print(user_data)
        # 开始任务
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        # 登录
        log = Quark(user_data).do_sign()
        msg += log + "\n"

        i += 1

    # print(msg)

    try:
        send('夸克自动签到', msg)
    except Exception as err:
        print('%s\n❌ 错误，请查看运行日志！' % err)

    return msg[:-1]


if __name__ == "__main__":
    print("----------夸克网盘开始签到----------")
    main()
    print("----------夸克网盘签到完毕----------")
