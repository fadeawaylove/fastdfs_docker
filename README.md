# 镜像构建以及使用
## 1.构建
```bash
# your_image为自定义的镜像名
docker build -t your_image .
```
## 2.使用
### 2.1 tracker运行
```bash
# 默认运行，端口为22122
docker run -itd --name tracker --net=host your_image tracker
# 指定tracker服务的端口
docker run -itd --name tracker --net=host -e FDFS_PORT=3333 your_image tracker
# 挂载tracker的数据目录,tracker在容器中的数据目录为/fdfs/fdfs_data
docker run -itd --name tracker --net=host -e FDFS_PORT=3333 -v ~/data/your_dir:/fdfs/fdfs_data your_image tracker
```
### 2.2 storage运行
```bash
# 必须指定tracker服务的地址，如果有多个tracker服务，则地址之间用逗号","隔开，如:TRACKER_SERVERS=192.168.209.128:22122,192.168.209.129:22122
# GROUP_NAME,指定这个storage所属的组名，默认为group1
# STORE_PORT,指定storage服务运行的端口，默认为23000
# HTTP_PORT，指定storage提供的http服务的端口，默认为8888，注意这个要与nginx中的配置一致
docker run -itd --name storage1 -e TRACKER_SERVERS=192.168.209.128:22122,192.168.209.129:22122 -e GROUP_NAME=group22 -e STORE_PORT=23001 -e HTTP_PORT=8889 -v ~/data/your_dir:/fdfs/fdfs_data --net=host your_image storage
```







