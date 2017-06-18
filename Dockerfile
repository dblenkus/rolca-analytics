FROM centos

MAINTAINER Domen Blenkuš <domen@blenkus.com>

ENV OPENCV_PREFIX /opt/opencv
ENV OPENCV_SRC_DIR $OPENCV_PREFIX/src
ENV OPENCV_VERSION 3.2.0
ENV OPENCV_ARCHIVE_URL https://github.com/opencv/opencv/archive/$OPENCV_VERSION.tar.gz

RUN yum update -y && yum install -y \
    make \
    cmake \
    gcc-c++ \
    gtk2-devel \
    opencv-python \
    && yum clean all

RUN mkdir -p $OPENCV_SRC_DIR \
    && curl -sL $OPENCV_ARCHIVE_URL | tar xz -C $OPENCV_SRC_DIR \
    && cd $OPENCV_SRC_DIR/opencv-$OPENCV_VERSION \
    && cmake . \
       -DCMAKE_INSTALL_PREFIX=$OPENCV_PREFIX \
       -DBUILD_DOCS=OFF \
       -DBUILD_EXAMPLES=OFF \
       -DBUILD_TESTS=OFF \
       -DBUILD_PERF_TESTS=OFF \
       -DBUILD_WITH_DEBUG_INFO=OFF \
    && make -s \
    && make -s install \
    && rm -rf $OPENCV_SRC_DIR

RUN echo "$OPENCV_PREFIX/lib" > /etc/ld.so.conf.d/opencv.conf && ldconfig
ENV PKG_CONFIG_PATH $OPENCV_PREFIX/lib/pkgconfig/:$PKG_CONFIG_PATH

ENV PATH="/scripts:${PATH}"

CMD ["/bin/bash"] 

