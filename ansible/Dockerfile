FROM tianon/debian:latest

RUN apt-get update &&\
    apt-get -y dist-upgrade

#ansible installation dependencies
RUN apt-get install python-pip python-dev git -y 
RUN apt-get clean
RUN pip install PyYAML jinja2 paramiko

#ansible installation
RUN cd /root &&\
    git clone https://github.com/ansible/ansible.git &&\
    cd ansible &&\
    git submodule update --init --recursive &&\
    make install

ADD . /tmp/ansible

#running playbook
RUN cd /tmp/ansible &&\
    ansible-playbook -i TESTHOST test.playbook

#Perform some checks
ADD expected /tmp/expected

RUN for f in $(find /tmp/expected -type f); do diff $f $(echo $f | sed -e 's:^.*expected::') || break 0; done;
RUN test -d /opt/risno 
