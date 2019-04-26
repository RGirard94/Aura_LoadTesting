# Aura_LoadTesting

Ansible role to automate data loading test to evaluate Aura infrastructure's data storage capacity. 
Data are randomly generated and injected in influxdb database.

## Aura Infrastructure

At first, you need to install Aura Infrastructure (https://github.com/Aura-healthcare/Aura_infrastructure)

## Playbook's details

This Ansible playbook consists of three roles:
  - prerequisite : installs tools used to perform well the different python scripts.
  - copy_directories : copies a directory containing the python scripts to randomly generate data and an other directory
                       containing the python scripts to inject the generated data in influxdb database. These directories are
                       copied from your local machin to the virtual machin containing the Aura Infrastructure.
  - load_testing : generates random data, injects them into influxdb database and recover some informations as injection time,
                   number of inserted data per field etc...

## Usage

At first you need to launch the playbook to install prerequisite and copy_directories roles. It allows to set the work environment to perform well the loading tests.

`ansible-playbook -i inventories/dev.yml install.yml -t prerequisite -t copy_directories`

Next you can perform your loading test with the following command.

`ansible-playbook -i inventories/dev.yml install.yml -t load_testing --extra-vars "nb_Rr_data= nb_Ma_data= nb_Mg_data= directory_to_inject=aura_data_test"`

You need to precise the amount of nb_Xx_data variable you want to generate.
Example : `nb_Rr_data=1000000`

Once the tests are performed, you can vizualise graph using kibana UI implemented with the Aura infrastructure
