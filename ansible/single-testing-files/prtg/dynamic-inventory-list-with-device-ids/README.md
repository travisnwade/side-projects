# Ansible PRTG Device ID Fetcher

## Overview

This Ansible project contains a playbook designed to retrieve PRTG device IDs for a list of hostnames. The playbook interacts with the PRTG API using an API token, retrieves device IDs for the specified hostnames, and stores them in a `device_ids.yml` file located in the `vars` directory.

## Directory Structure

```
ansible_project/
├── ansible.cfg
├── inventories/
│   ├── hosts.ini
├── playbooks/
│   ├── get_prtg_device_ids.yml
├── vars/
│   ├── device_ids.yml
```

## Prerequisites

1. **Ansible**: Ensure Ansible is installed on your control machine.
2. **PRTG API Access**: Obtain your PRTG API URL and API token.
3. **Hostnames**: List of hostnames you want to retrieve device IDs for.

## Setup

1. **Configure Ansible**: Ensure your `ansible.cfg` is set up correctly.
2. **Inventory**: List your target hosts in the inventory file `hosts.ini`.
3. **PRTG Credentials**: Replace the placeholder values for `prtg_api_url` and `prtg_api_token` in the playbook with your actual PRTG API details.

## Files

### `ansible.cfg`

This configuration file ensures Ansible recognizes the inventory file.

```ini
[defaults]
inventory = inventories/hosts.ini
```

### `inventories/hosts.ini`

List your target hosts in this inventory file.

```ini
[all]
localhost
```

### `playbooks/get_prtg_device_ids.yml`

This playbook retrieves PRTG device IDs for the specified hostnames and saves them to `vars/device_ids.yml`.

```yaml
---
- name: Get PRTG Device IDs
  hosts: localhost
  gather_facts: no
  vars:
    prtg_api_url: "https://prtg.example.com/api"
    prtg_api_token: "your_prtg_api_token"
    hostnames:
      - hostname1
      - hostname2
      - hostname3
  tasks:
    - name: Ensure vars directory exists
      ansible.builtin.file:
        path: vars
        state: directory

    - name: Initialize device_ids dictionary
      set_fact:
        device_ids: {}

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

    - name: Parse and store device IDs
      set_fact:
        device_ids: "{{ device_ids | combine({ item: (prtg_response.json.devices | selectattr('host', 'equalto', item) | first).objid }) }}"
      loop: "{{ hostnames }}"
      when: prtg_response.json.devices is defined and (prtg_response.json.devices | selectattr('host', 'equalto', item) | list) | length > 0

    - name: Save device IDs to vars file
      copy:
        content: "{{ device_ids | to_nice_yaml }}"
        dest: vars/device_ids.yml
```

## Usage

To run the playbook and populate the `device_ids.yml` file with PRTG device IDs, execute the following command:

```sh
ansible-playbook playbooks/get_prtg_device_ids.yml
```