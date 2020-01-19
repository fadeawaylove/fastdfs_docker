import os
import sys

# 读取命令行参数，来判断是tracker还是storage
server_type = sys.argv[-1]

# storage需要设置：
# base_path: 存储storage数据和日志的目录，默认设置的/fdfs
# tracker_server：追踪服务器的地址，是一个用逗号隔开的字符串
if server_type == "storage":
    # 读取storage的环境变量
    base_path = os.getenv("BASE_PATH")
    tracker_servers = os.getenv("TRACKER_SERVERS").split(",")
    store_port = os.getenv("STORE_PORT")
    http_server_port = os.getenv("HTTP_PORT")
    group_name = os.getenv("GROUP_NAME")
    # 生成配置文件
    with open("/etc/fdfs/storage.conf.sample", "r") as fr, open("/etc/fdfs/storage.conf", "w") as fw:
        for line in fr:
            # 替换base_path
            if line.startswith("base_path"):
                line = "base_path=" + base_path + "\n"
            # 替换第一个存储目录，就设置为base_path
            if line.startswith("store_path0"):
                line = "base_path=" + base_path + "\n"
            # 替换track_server
            if line.startswith("tracker_server"):
                temp_line = ""
                for t in tracker_servers:
                    temp_line += "tracker_server=" + t + "\n"
                line = temp_line
            # 替换storage服务的port
            if line.startswith("port"):
                line = "port=" + store_port + "\n"
            # 替换http服务的port
            if line.startswith("http.server_port"):
                line = "http.server_port=" + http_server_port + "\n"
            # 替换storage所属的group
            if line.startswith("group_name"):
                line = "group_name=" + group_name + "\n"
            fw.write(line)
    # 开启服务
    os.system("/etc/init.d/fdfs_storaged start")

# tracker的设置：
# port：默认是22122
# base_path：存储tracker数据和日志的目录，默认设置的/fdfs
elif server_type == "tracker":
    # 读取tracker的环境变量
    base_path = os.getenv("BASE_PATH")
    fdfs_port = os.getenv("FDFS_PORT")
    # 替换配置
    with open("/etc/fdfs/tracker.conf.sample", "r") as fr, open("/etc/fdfs/tracker.conf", "w") as fw:
        for line in fr:
            # 替换base_path
            if line.startswith("base_path"):
                line = "base_path=" + base_path + "\n"
            # tracker的port
            if line.startswith("port"):
                line = "port=" + fdfs_port + "\n"
            fw.write(line)
    # 开启服务
    os.system("/etc/init.d/fdfs_trackerd start")
else:
    raise Exception("Please input storage or tracker")

# 避免容器运行就退出
os.system("/bin/bash")
