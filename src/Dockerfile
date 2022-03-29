FROM public.ecr.aws/lambda/python:3.9

#dependencias da LIB pillow-simd
RUN yum -y install zlib \
    freetype-devel \
    gcc \
    lcms2-devel \
    libimagequant-devel \
    libjpeg-devel \
    libraqm-devel \
    libtiff-devel \
    libwebp-devel \
    openjpeg2-devel \
    tcl-devel \
    tk-devel \
    zlib-devel \
#    gzip \
#    tar \
#    ghostscript \
#    libffi-devel \
#    make \
#    rh-python36 \
#    rh-python36-python-virtualenv \
#    sudo \
#    tkinter \
#    which \
#    xorg-x11-server-Xvfb \
#
#    harfbuzz-devel \
#    fribidi-devel \
#    libxcb-devel \
    && yum clean all

COPY app.py requirements.txt ./

RUN /var/lang/bin/python3.9 -m pip install --upgrade pip

RUN python3.9 -m pip install -r requirements.txt -t .


RUN CC="cc -mavx2" pip install -U --force-reinstall pillow-simd

#RUN python3.9 -c "print('PIL',PIL.__version__)"
#RUN python3.9 -c "print('PIL',PIL.PILLOW_VERSION)"
#RUN python3.9 -c "print('PIL',PIL.Image.VERSION)"
#RUN python3.9 -c "print('PIL',PIL.Image.PILLOW_VERSION)"
# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
