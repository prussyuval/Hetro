***Heterogeneous Cluster***

**Producer**

Produce variety of tasks to be consumed by the Heterogeneous Cluster. 

```
usage: producer/main.py
```

**Consumer**

Consume tasks from TASK_TYPE and remove them from the queue

```usage: consumer/main.py [-h] -t TASK_TYPE -f FILE_NAME

optional arguments:
  -h, --help            show this help message and exit
  -t TASK_TYPE, --type TASK_TYPE, --task_type TASK_TYPE
                        Task type to consume
  -f FILE_NAME, --file FILE_NAME, --file_name FILE_NAME
                        File name to consume tasks from
```
