import os
import time
import shutil


# 功能点
# 1. 输入指定的文件路径
# 2. 展示路径下的文件详情, 如果没有文件就退出
# 3. 输入指定的输出路径（如果不指定，就在指定的路径默认建一个output文件夹）
# 4. 简单的替换规则：
#   4.1 指定替换的字符串
#   4.2 指定替换的开始位置，
#   4.3 指定序列号开始数字，用于拼接在重命名的文件名末尾
# 5. 在指定文件路径下，建一个日志文件夹，日志记录：输出txt文件，记录源文件 --> 新文件 的对应关系。
# 6. 增加一个选项问用户是否需要保存原来的文件
# 7. 尝试对正则替换的支持 TODO

# 日志记录功能
def gen_my_log(msg, path):
    # file = r'C:\Users\zhanggs\Desktop\test\log-remane20180830.txt'
    log_path = path + '\\log\\'
    if not (os.path.exists(log_path)):
        make_dir(log_path)
    file = log_path + "log" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".txt"
    with open(file, 'a+', encoding='utf-8') as f:
        f.write(msg)


def user_input_dir():
    while True:
        try:
            input_dir = input()
            if os.path.exists(input_dir):
                return input_dir
            else:
                print("x  请输入需要批量重命名文件所在的路径（请用斜杠/）:")
        except Exception:
            print("x  请输入需要批量重命名文件所在的路径（请用斜杠/）:")


def user_output_dir():
    while True:
        try:
            output_dir = input()
            if os.path.exists(output_dir):
                return output_dir
            else:
                print("###  路径不存在，创建中……")
                make_dir(output_dir)
                print("###  路径创建成功")
                return output_dir
        except Exception:
            print("x  请输入文件路径（请用斜杠/）:")


def user_yes_or_no():
    yes_words = ['Y', 'YES']
    no_words = ['N', 'NO']
    while True:
        try:
            user_yes_no = input()
            if user_yes_no.upper() in yes_words:
                return "Y"
            elif user_yes_no.upper() in no_words:
                return "N"
            else:
                print("x  请输入：Y 或者 N")
        except Exception:
            print("x  请输入：Y 或者 N")


def user_input_notnull():
    while True:
        try:
            input_str = input()
            if input_str.strip() != '':
                return input_str
            else:
                print("x  输入不能为空")
        except Exception:
            print("x  输入不能为空")


def make_dir(t_path):
    folder = os.path.exists(t_path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(t_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("###  创建新文件:" + t_path)
        print("###  OK")
    else:
        print("###  路径已存在，不用新建: "+ t_path)


def show_files_in_dir(files_dir):
    print("###   路径下的文件如下：")
    temp_index = 0
    file_list = os.listdir(files_dir)
    for files in file_list:  # 遍历所有文件
        show_dir = os.path.join(files_dir, files)  # 原来的文件路径
        if os.path.isdir(show_dir):  # 如果是文件夹则跳过
            continue
        else:
            temp_index += 1
            print(show_dir)
    if temp_index == 0:
        # print("--没有文件，退出程序--")
        exit("###  没有文件，退出程序")
    print("###  ------------")


def user_num_input():
    while True:
        try:
            user_num = int(input())
            if 0 < user_num < 1000:
                return user_num
            else:
                print("x  请输入1000以内的整数数字: ")
        except Exception:
            print("x  请输入1000以内的整数数字: ")


def rename(new_str, old_path, new_path, start_index=1, start_seq=1, save_old_file=1):
    print("###  重命名进行中: ")
    if start_index <= 1:
        start_index = 1

    file_list = os.listdir(old_path)  # 该文件夹下所有的文件（包括文件夹）

    i = start_seq
    for files in file_list:  # 遍历所有文件

        old_dir = os.path.join(old_path, files)  # 原来的文件路径
        if os.path.isdir(old_dir):  # 如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0]  # 文件名
        new_name1 = filename[:start_index-1]
        new_name2 = new_str
        new_name3 = gen_end_index(str(i))
        file_type = os.path.splitext(files)[1]  # 文件扩展名
        new_name = new_name1 + new_name2 + new_name3
        new_dir = os.path.join(new_path, new_name + file_type)
        if save_old_file == 1:
            # 保留源文件
            shutil.copyfile(old_dir, new_dir)  # 复制重命名
        else:
            os.rename(old_dir, new_dir)  # 重命名
        i += 1
        msg = old_dir + '重命名完成：' + new_dir
        print(msg)
        gen_my_log(msg + '\n', old_path)


# 返回6位左补零点数字字符串
def gen_end_index(index):
    return index.zfill(6)


if __name__ == '__main__':
    print("\n>>>  请输入需要重命名的文件所在的路径: ")
    path = user_input_dir()
    show_files_in_dir(path)  # 展示路径下的文件详情
    print("\n>>>  是否需要保留源文件, Y/N ")
    save_flag = user_yes_or_no()
    if save_flag == 'Y':
        is_save = 1
    else:
        is_save = 0
    print("\n>>>  是否需要指定重命名后的文件保存的路径, Y/N ")
    flag = user_yes_or_no()
    if flag == 'Y':
        new_path = user_output_dir()
    else:
        new_path = path + '/output/'
        make_dir(new_path)
    print("\n>>>  请输入文件名需要替换成的字符串: ")
    replace_str = user_input_notnull()
    print("\n>>>  是否需要指定文件后缀的序列号开始数字（默认从1开始）, Y/N ")
    num_flag = user_yes_or_no()
    if num_flag == 'Y':
        print("x  请输入整数： ")
        start_seq = user_num_input()
    else:
        start_seq = 1
    print("\n>>>  是否需要指定从源文件名的第几位开始替换（默认从开始位置进行替换）, Y/N ")
    index_flag = user_yes_or_no()
    if index_flag == 'Y':
        print("x  请输入整数： ")
        start_i = user_num_input() + 1
    else:
        start_i = 0
    rename(replace_str, path, new_path, start_i, start_seq, is_save)
    print("\n>>>  重命名后的文件保存在："+new_path)
