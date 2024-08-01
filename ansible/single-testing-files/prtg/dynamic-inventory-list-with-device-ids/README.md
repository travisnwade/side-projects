# Ansible PRTG Device ID Fetcher

## Overview

This Ansible project contains a playbook designed to retrieve PRTG device IDs for a list of hostnames. The playbook interacts with the PRTG API using an API token, retrieves device IDs for the specified hostnames, and stores them in a dynamic inventory file named `dynamic_inventory.yml`.

## Directory Structure

```
ansible_project/
├── ansible.cfg
├── inventories/
│   ├── dynamic_inventory.yml
├── playbooks/
│   ├── populate_dynamic_inventory.yml
├── vars/
│   ├── hostnames.yml
```

## Prerequisites

1. **Ansible**: Ensure Ansible is installed on your control machine.
2. **PRTG API Access**: Obtain your PRTG API URL and API token.
3. **Hostnames**: List of hostnames you want to retrieve device IDs for.

## Setup

1. **Configure Ansible**: Ensure your `ansible.cfg` is set up correctly.
2. **Inventory**: Create a `hostnames.yml` file under the `vars` directory with the list of hostnames.
3. **PRTG Credentials**: Replace the placeholder values for `prtg_api_url` and `prtg_api_token` in the playbook with your actual PRTG API details.

## Files

### `ansible.cfg`

This configuration file ensures Ansible recognizes the inventory file.

```ini
[defaults]
inventory = inventories/dynamic_inventory.yml
```

### `vars/hostnames.yml`

List your target hostnames in this file.

```yaml
---
hostnames:
  - hostname1
  - hostname2
  - hostname3
```

### `playbooks/populate_dynamic_inventory.yml`

This playbook retrieves PRTG device IDs for the specified hostnames and saves them to `inventories/dynamic_inventory.yml`.

```yaml
---
- name: Populate Dynamic Inventory with PRTG Device IDs
  hosts: localhost
  gather_facts: no
  vars_files:
    - ../vars/hostnames.yml
  vars:
    prtg_api_url: "https://prtg.example.com/api"
    prtg_api_token: "your_prtg_api_token"
  tasks:
    - name: Ensure inventories directory exists
      ansible.builtin.file:
        path: inventories
        state: directory

    - name: Initialize inventory dictionary
      set_fact:
        inventory: {
          "_meta": {
            "hostvars": {}
          },
          "all": {
            "hosts": []
          }
        }

    - name: Get PRTG device ID for each hostname
      vars:
        hostname: "{{ item }}"
      ansible.builtin.uri:
        url: "{{ prtg_api_url }}/table.json?content=devices&output=json&columns=device,host&id=0&username=api&passhash={{ prtg_api_token }}"
        method: GET
        return_content: yes
      register: prtg_response
      loop: "{{ hostnames }}"
      changed_when: false

    - name: Parse and store device IDs in inventory
      set_fact:
        inventory: "{{ inventory | combine({ 'all': { 'hosts': inventory['all']['hosts'] + [item] }, '_meta': { 'hostvars': inventory['_meta']['hostvars'] | combine({ item: { 'device_id': (prtg_response.json.devices | selectattr('host', 'equalto', item) | first).objid } }) } }) }}"
      loop: "{{ hostnames }}"
      when: prtg_response.json.devices is defined and (prtg_response.json.devices | selectattr('host', 'equalto', item) | list) | length > 0

    - name: Save inventory to dynamic_inventory.yml
      copy:
        content: "{{ inventory | to_nice_yaml }}"
        dest: inventories/dynamic_inventory.yml
```

## Usage

To run the playbook and populate the `dynamic_inventory.yml` file with PRTG device IDs, execute the following command:

```sh
ansible-playbook playbooks/populate_dynamic_inventory.yml
```

## Notes

- Ensure you have replaced the placeholder values for `prtg_api_url` and `prtg_api_token` with your actual PRTG API details.
- This playbook queries the PRTG API for each hostname listed in `hostnames.yml`, retrieves the corresponding device IDs using the API token, and saves them in `inventories/dynamic_inventory.yml`.