# 基于 alpine
FROM python:3.6-alpine
# 作者信息
MAINTAINER daigua<1032939141@qq.com>
# 环境变量
# 存储日志和数据的根目录
ENV BASE_PATH /fdfs/fdfs_data
# 默认fastdfs端口
ENV FDFS_PORT 22122
# tracker服务列表
ENV TRACKER_SERVERS 127.0.0.1:22122
# storage服务的端口
ENV STORE_PORT 23000
# http服务的端口
ENV HTTP_PORT 8888
# storage服务所属的组
ENV GROUP_NAME group1

# 安装依赖
RUN apk update \
    && apk add --no-cache  git gcc libc-dev make automake autoconf libtool pcre pcre-dev zlib zlib-dev openssl-dev wget vim

# 安装libfastcommon
WORKDIR /fdfs/packages
RUN git clone https://github.com/happyfish100/libfastcommon.git --depth 1 \
    && cd libfastcommon/ \
    && ./make.sh \
    && ./make.sh install

# 安装FastDFS
WORKDIR /fdfs/packages
RUN git clone https://github.com/happyfish100/fastdfs.git --depth 1 \
    && cd fastdfs/ \
    && ./make.sh \
    && ./make.sh install \
    && cd /fdfs/ \
    && rm -rf /fdfs/packages

# 复制运行脚本
WORKDIR /fdfs
COPY entrypoint.py ./

ENTRYPOINT ["python", "entrypoint.py"]
