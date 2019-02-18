# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "stachoutils", primary: true do |stachoutils|
    stachoutils.vm.box = "bento/ubuntu-16.04"
    stachoutils.vm.hostname = "stachoutils"

    stachoutils.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
    end

    stachoutils.vm.provision "shell", inline: <<-SHELL
      apt-get update
      DEBIAN_FRONTEND="noninteractive" apt-get install -y build-essential \
      python-minimal python-dev python3-dev virtualenv python3-venv
    SHELL

    stachoutils.vm.provision "create-virtualenv-py2", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      virtualenv venv_py2
    SHELL

    stachoutils.vm.provision "create-virtualenv-py3", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      python3 -m venv venv_py3
    SHELL

    stachoutils.vm.provision "pip2-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py2/bin/activate
      pip install coverage django==1.11 future Pillow sorl-thumbnail django_thumbor
    SHELL

    stachoutils.vm.provision "pip3-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py3/bin/activate
      pip3 install coverage django==2.0.10 future Pillow sorl-thumbnail django_thumbor
    SHELL

    stachoutils.vm.provision "bashrc", type: :shell, privileged: false, inline: <<-SHELL
      echo "cd /vagrant" >> ~/.bashrc
      echo "source ~/venv_py2/bin/activate" >> ~/.bashrc
    SHELL
  end
end

