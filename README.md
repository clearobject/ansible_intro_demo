# Ansible Introduction

This project introduces Ansible to new or inexperienced developers. It was prepared for the Indianapolis Ansible meetup.

# Prerequisites

1. Ansible, git and python must be installed on the Control machine.

    **Mac**  
    1. Install homebrew and use it to install the required packages.  
    ```bash  
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"  
    brew install git python ansible  
    ```  

    **Linux**  
    1. Install required packages.  
    ```bash  
    yum install python-pip git ansible  
    # For Debian systems, replace yum with apt  
    ```  
    2. Install some system packages that pip will need.  
    ```bash  
    yum install epel-release libffi-devel python-devel openssl-devel gcc  
    # For Debian systems, use:  
    # apt install libffi-dev python-dev libssl-dev gcc  
    ```

2. Create virtual environment to work in.
    ```bash  
    pip install virtualenv  
    # virtualenv will make a folder for you  
    virtualenv ~/path/to/project  
    cd ~/path/to/project  
    ```

3. Clone the automation repo into the project folder.
    ```bash  
    git clone https://github.com/clearobject/ansible_intro_demo.git  
    ```

You should be ready to go!

# Inventory

The inventory directory contains files that are used to determine what machines or groups of machines will be targeted in the automation run.

Groups are named inside square brackets: `[webservers]`  
All domain names or IP addresses under that heading will belong to that group.  
Inventories are included using the `-i` option when running **playbooks** or Ad-Hoc Ansible commands.

# Library

This directory holds Custom Modules. Ansible will look here for any module that is not built-in.
There is no special command line option needed to include Custom Modules. Ansible includes them automatically as long as they are in the directory specified in ansible.cfg.

# Playbooks

Playbooks are lists of **tasks** or included **roles** that will use Ansible modules to run automated operations.  
**Tasks** are direct calls to Ansible modules in a playbook.  
Longer playbooks that do multiple operations can import **Roles**. An imported role will be run in its entirety unless otherwise specified using **tags**.  
**Tags** can be used to label similar tasks in a playbook or role. They can the be specifically selected when running a playbook.  
Tags can be specified when importing roles in a playbook, or from the command line using the `--tags` option.  

# Roles

Roles are a way to reuse code that would otherwise have to be copy and pasted into multiple playbooks.  
Roles are basically just a long list of tasks that will be executed.

# Templates

Templates are Jinja files that can be formatted to be html files, parts of html files, json objects, etc.  
Templates pull information from **registered variables** and set **facts**.  
This information is inserted using either Ansible variable calls: `{{ variable_name }}` or Jinja includes: `{% include anotherTemplate.j2 %}`

# Variables

Variables are used to store output from various module runs. These outputs are json objects that may contain strings, booleans, lists, etc.  
**Facts** can be set as a playbook runs using the `set_fact` module. They can also be set under the **group_vars** and **host_vars** folders.  
Output from modules that have been run can be put into variables using the `register` module.  
The **group_vars** and **host_vars** folders contain files that list default values for different variables. These variables may be empty, then updated as the playbook or role runs.
