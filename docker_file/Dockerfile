FROM centos:centos6.8

RUN yum -y install gcc gcc-c++ git zlib zlib-deve vim make openssl-devel bzip2-devel readline-devel bzip2 sqlite-devel sqlite python-setuptools python-setuptools-devel python-devel
RUN git clone https://github.com/yyuu/pyenv.git ~/.pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
RUN echo 'export PYENV_ROOT=$HOME/.pyenv' >> ~/.bash_profile
RUN echo 'export PATH=$PYENV_ROOT/bin:$PATH' >> ~/.bash_profile
RUN echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
RUN source ~/.bash_profile
RUN easy_install pip
RUN rpm -ivh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
RUN yum install -y nginx

ENV HOME=/root
ENV PYENV_ROOT=$HOME/.pyenv
ENV PATH=$PYENV_ROOT/bin:$PATH
ENV PYVERSION=3.6.1
ENV WORK_DIR=/home/lambda
ENV VIRTUALNAME=lambda

RUN pyenv install ${PYVERSION}
RUN pyenv global ${PYVERSION}
RUN pyenv virtualenv ${VIRTUALNAME}
RUN mkdir ${WORK_DIR}; cd ${WORK_DIR}; pyenv local ${VIRTUALNAME};
WORKDIR ${WORK_DIR}
RUN bash -lc 'pip install --upgrade pip && pip install awscli'
RUN bash -lc 'pip install uwsgi &&  pip install python-lambda-local'

VOLUME [${WORK_DIR}]

ADD default.conf   /etc/nginx/conf.d/
ADD uwsgi ${WORK_DIR}/uwsgi
ADD run.sh /tmp/

ENTRYPOINT sh /tmp/run.sh
