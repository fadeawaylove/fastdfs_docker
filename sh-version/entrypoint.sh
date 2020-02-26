#!/bin/bash
type_tracker="tracker"
type_storage="storage"
orgin_base_path="/fdfs/fdfs_data"
transfer_base_path="\/fdfs\/fdfs_data"

server_type=$1
echo $server_type
mkdir -p $orgin_base_path
if [ $server_type == $type_tracker ];then
    echo "start building ${server_type}..."
    # 复制配置文件
    cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf;
    # 替换配置文件中的参数
    sed -i "s/^port.*$/port=${FDFS_PORT}/g" /etc/fdfs/tracker.conf;
    sed -i "s/^base_path.*$/base_path=${transfer_base_path}/g" /etc/fdfs/tracker.conf;
    # 启动tracker
    /etc/init.d/fdfs_trackerd start;
elif [ $server_type == $type_storage ];then
    echo "start building ${server_type}...";
    # 复制配置文件
    cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf;
    # 替换文件中的配置
    sed -i "s/^base_path.*$/base_path=${transfer_base_path}/g" /etc/fdfs/storage.conf;
    sed -i "s/^store_path0.*$/store_path0=${transfer_base_path}/g" /etc/fdfs/storage.conf;
    tracker_str="";
    array=(${TRACKER_SERVERS//,/ });
    for var in ${array[@]}
    do
       tracker_str="${tracker_str}tracker_server=${var}\n"
    done
    echo $tracker_str
    sed -i "s/^tracker_server.*$/${tracker_str}/g" /etc/fdfs/storage.conf;
    sed -i "s/^port.*$/port=${STORE_PORT}/g" /etc/fdfs/storage.conf;
    sed -i "s/^http.server_port.*$/http.server_port=${HTTP_PORT}/g" /etc/fdfs/storage.conf;
    sed -i "s/^group_name.*$/group_name=${GROUP_NAME}/g" /etc/fdfs/storage.conf;
    # 启动storage
    /etc/init.d/fdfs_storaged start
else
    echo "wrong server type! [${server_type}]"
fi

tail -f  /dev/null
