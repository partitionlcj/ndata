FROM xharbor.i-tetris.com:5000/public/centos7-with-tools:v1.0

# mount jdk path
VOLUME /opt/java/jdk-1.8

ENV JAVA_HOME /opt/java/jdk-1.8
ENV PATH $PATH:/opt/java/jdk-1.8/jre/bin:/opt/java/jdk-1.8/bin

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

# Install tools
RUN yum update -y && \
    yum reinstall -y glibc-common && \
    yum install -y telnet net-tools && \
    yum clean all && \
    rm -rf /tmp/* rm -rf /var/cache/yum/* && \
    localedef -c -f UTF-8 -i zh_CN zh_CN.UTF-8 && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ENV USER_DIR /data/app/mars-ops

RUN yum -y install tar
RUN yum -y install mysql
RUN yum -y install python3
RUN yum -y install python3-pip

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir pymysql boto3 wave


RUN mkdir -p /data/app/mars-ndata
WORKDIR /data/app/mars-ndata

COPY ./api/target/ndata-0.0.1-SNAPSHOT.jar ./
COPY ./api/src/main/resources/*.yml ./
COPY ./ui/dist ./static
COPY ./start.sh ./

EXPOSE 8000

ENTRYPOINT ["sh", "start.sh"]
