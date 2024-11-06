import itertools
import string

from function import getNCode
from function.futuresPool import ThreadPoolManager
from function.getFunction import getOver

def get_Ncode_list():
    data = getOver()
    print(data)
    start_number = int(data['ncodeasc'][1:5])
    start_suffix = data['ncodeasc'][5:]
    end_number = int(data['ncodedesc'][1:5])
    end_suffix = data['ncodedesc'][5:]
    letters = list(string.ascii_uppercase)
    suffixes = ["".join(suffix) for suffix in itertools.product(letters, repeat=1)] + \
               ["".join(suffix) for suffix in itertools.product(letters, repeat=2)]
    # 截取所需范围的组合
    suffixes = suffixes[suffixes.index(start_suffix):suffixes.index(end_suffix) + 1]
    ncode_list = []
    for suffix in suffixes:
        for number in range(start_number, end_number + 1):
            if suffix == start_suffix and number == start_number:
                # print(f"N{number:04d}{suffix}")
                    ncode_list.append(f"N{number:04d}{suffix}")
            elif suffix == end_suffix and number == end_number:
                # print(f"N{number:04d}{suffix}")
                ncode_list.append(f"N{number:04d}{suffix}")
            else:
                # print(f"N{number:04d}{suffix}")
                ncode_list.append(f"N{number:04d}{suffix}")
    return ncode_list
def main():
    thread_pool_manager = ThreadPoolManager(max_workers=20)

    # print(len(get_Ncode_list()))
    for i in get_Ncode_list():
        # print(i,end="")
        continue
        # thread_pool_manager.submit_task(i)
    results = thread_pool_manager.get_task_results()
main()
