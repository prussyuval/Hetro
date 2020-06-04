<h1>Heterogeneous Cluster</h1>

Heterogeneous Cluster is an extensible multi-core server manager to consume various tasks 
and mimic the human digestive system.

**Producer**

Produce variety of tasks to be consumed by the Heterogeneous Cluster.

```
usage: main.py [-h] -f FILE_NAME

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file FILE_NAME, --file_name FILE_NAME
                        File name to consume tasks from
```

**Consumer**

Consume tasks from TASK_TYPE and remove them from the queue.

```
usage: consumer/main.py [-h] -t TASK_TYPE -f FILE_NAME

optional arguments:
  -h, --help            show this help message and exit
  -t TASK_TYPE, --type TASK_TYPE, --task_type TASK_TYPE
                        Task type to consume
  -f FILE_NAME, --file FILE_NAME, --file_name FILE_NAME
                        File name to consume tasks from
```

**License**

@ HIT Biomimicry Course @

Or Moradian and Yuval Pruss
