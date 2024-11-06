#文件操作
import os
from datetime import datetime

dir_base = os.path.dirname(os.path.abspath(__file__))
def input_SQL(params_list,table_name="install",print_div ="../print"):
    sql_file_name = f"{print_div}/{table_name}.sql"
    file_exists = os.path.isfile(sql_file_name)
    # 如果文件不存在，创建新文件并写入创建表的语句
    # insert_template = f"INSERT INTO {table_name} (ncode, Introduction, author, key, type) VALUES ({', '.join(['%s'] * 5)});\n"
    with open(sql_file_name, 'a') as f:
        if not file_exists:
            f.write(f"CREATE TABLE {table_name} (\n")
            f.write("    ncode char PRIMARY KEY,\n")
            f.write("    Introduction TEXT,\n")
            f.write("    author TEXT,\n")
            f.write("    key TEXT,\n")
            f.write("    type TEXT,\n")
            f.write("    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n")
            f.write(");\n")
        insert_statement = f'INSERT INTO {table_name} (ncode, Introduction, author, key, type) VALUES ({params_list[0]} {params_list[1]} {params_list[2]} {params_list[3]} {params_list[4]});\n'
        f.write(insert_statement)
def get_dir(ncode, print_div ="../print"):
    try:
        novel_dir =  os.path.normpath( f'{print_div}/{ncode}')
        if not os.path.exists(novel_dir):
            os.mkdir(novel_dir)
        return novel_dir
    except Exception as e:
        print(f"{e}")

def write_log(filename, content,print_div ="../log"):
    # 如果文件不存在，则创建它（可选：你也可以选择不创建文件并在文件不存在时抛出错误）
    log_file = f"{print_div}/{filename}.log"
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            # 这里其实不需要写入任何内容，因为我们只是要创建文件
            pass
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 写入内容到文件，并附加时间戳
    with open(filename, 'a') as f:
        f.write(f"{current_time} - {content}\n")
