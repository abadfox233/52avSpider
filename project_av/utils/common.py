import hashlib
import re

def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    # 从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def pass_url(cursor, md5):
    sql_1 = 'select 1 from video_url where video_object_id = \'{}\' limit 1;'.format(md5)
    sql_2 = 'select 1 from movie where movie_object_id = \'{}\' limit 1;'.format(md5)
    sql_3 = 'select 1 from video_images where video_object_id = \'{}\' limit 1;'.format(md5)
    sql_list = [sql_1, sql_2, sql_3]
    result = 0
    for sql in sql_list:
        result += cursor.execute(sql)
    if result >= 3:
        return False
    else:
        return True


def get_time(time_str):
    pattern = re.compile('.*(\d{4}\-\d+\-\d+.\d+:\d+:\d+).*')
    result = pattern.findall(time_str)
    if len(result) >= 1 and isinstance(result[0], str):
        return result[0]


def get_page_num(url):
    pattern = re.compile('.*&page=(\d+).*')
    result = pattern.findall(url)
    if len(result) >= 1 and isinstance(result[0], str):
        if result[0].isalnum():
            return int(result[0])
    return None


if __name__ == "__main__":
    print(pass_url('4264eb3ffb1be3444ebb9929d17dafaf'))