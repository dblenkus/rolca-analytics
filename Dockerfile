FROM centos

MAINTAINER Domen Blenkuš <domen@blenkus.com>

RUN yum -y update && \
    yum install -y opencv opencv-python numpy && \
    yum clean all

ENV PATH="/scripts:${PATH}"

CMD ["/bin/bash"]
