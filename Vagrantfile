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
      python-minimal python-dev virtualenv
    SHELL

    stachoutils.vm.provision "create-virtualenv-py2", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      virtualenv venv_py2
    SHELL

    stachoutils.vm.provision "pip2-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py2/bin/activate
      pip install coverage django==1.11
    SHELL

    stachoutils.vm.provision "bashrc", type: :shell, privileged: false, inline: <<-SHELL
      echo "cd /vagrant" >> ~/.bashrc
      echo "source ~/venv_py2/bin/activate" >> ~/.bashrc
    SHELL
  end
end

