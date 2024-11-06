import concurrent.futures
import time


class ThreadPoolManager:
    def __init__(self, max_workers):
        # 初始化线程池
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []  # 用于存储提交的 Future 对象

    def submit_task(self, func, *args, **kwargs):
        # 提交任务到线程池，并存储返回的 Future 对象
        future = self.pool.submit(func, *args, **kwargs)
        self.futures.append(future)
        return future

    def wait_for_all_tasks(self):
        # 等待所有任务完成
        concurrent.futures.wait(self.futures)

    def get_task_results(self):
        # 获取所有任务的结果
        results = [future.result() for future in self.futures]
        self.shutdown_pool()
        return results

    def shutdown_pool(self, wait=True):
        # 关闭线程池
        self.pool.shutdown(wait=wait)


# 这是一个示例函数，它将接受一些参数并模拟一些工作
def worker_function(arg1, arg2):
    print(f"Worker started with args: {arg1}, {arg2}")
    time.sleep(2)  # 模拟耗时操作
    return f"Result of {arg1} and {arg2}"


# 主函数
# if __name__ == "__main__":
#     # 创建一个 ThreadPoolManager 实例，并设置最大工作线程数
#     thread_pool_manager = ThreadPoolManager(max_workers=3)
#
#     # 提交任务到线程池
#     future1 = thread_pool_manager.submit_task(worker_function, 1, "A")
#     future2 = thread_pool_manager.submit_task(worker_function, 2, "B")
#     future3 = thread_pool_manager.submit_task(worker_function, 3, "C")
#
#     # 等待所有任务完成
#     thread_pool_manager.wait_for_all_tasks()
#
#     # 获取任务的结果
#     results = thread_pool_manager.get_task_results()
#     print(f"Results: {results}")