# redis key
REDIS_PROBLEM_TOPIC = 'vcode-spider-problem'  # 将爬取的题目保存至此队列
REDIS_TARGET_TOPIC = 'vcode-spider-target'  # web将指定爬去的任务保存至此队列，爬虫从此队列获取任务
REDIS_TARGET_RESULT_TOPIC = 'vcode-spider-target-result'  # 爬虫将任务结果（非题目信息）保存至此队列
REDIS_NAMESPACE_TOPIC = 'vcode-spider-namespace'  # 爬虫在启动时将支持的oj发送至此key
REDIS_LOCK_KEY = 'vcode-spider-task-lock'  # 爬虫的分布式锁，防止重复生产任务
REDIS_TASK_LIST = 'vcode-spider-task-list'  # 爬虫的自身生成的任务队列
