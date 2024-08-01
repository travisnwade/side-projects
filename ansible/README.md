# Ansible Windows Update Project

## Overview

Welcome to the Ansible Windows Update Project! This repository contains Ansible playbooks, inventory files, and roles to manage and update Windows servers from 2012 through 2022. The playbook provided here installs all available security, critical, and update rollups regardless of the status of any existing updates.

## Folder Structure

```
ansible_project/
├── ansible.cfg
├── inventories/
│   ├── development/
│   │   ├── hosts.ini
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── windows_servers.yml
│   ├── staging/
│   │   ├── hosts.ini
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── windows_servers.yml
│   └── production/
│       ├── hosts.ini
│       └── group_vars/
│           ├── all.yml
│           └── windows_servers.yml
├── playbooks/
│   ├── windows_update_playbook.yml
│   └── roles/
│       ├── common/
│       │   ├── tasks/
│       │   │   └── main.yml
│       │   ├── handlers/
│       │   │   └── main.yml
│       │   ├── templates/
│       │   │   └── some_template.j2
│       │   ├── files/
│       │   │   └── some_file.txt
│       │   └── vars/
│       │       └── main.yml
│       └── windows_updates/
│           ├── tasks/
│           │   └── main.yml
│           └── vars/
│               └── main.yml
└── vars/
    ├── development.yml
    ├── staging.yml
    └── production.yml
```

## Explanation of the Folder Structure

- **ansible.cfg**: The Ansible configuration file where you can define your Ansible configuration settings.

- **inventories/**: Directory containing different inventory configurations for various environments.
  - **development/**, **staging/**, **production/**: Subdirectories for different environments.
    - **hosts.ini**: Inventory file listing the hosts and groups for the environment.
    - **group_vars/**: Directory for variables that are specific to groups of hosts.
      - **all.yml**: Variables that apply to all hosts in the inventory.
      - **windows_servers.yml**: Variables specific to the `windows_servers` group.

- **playbooks/**: Directory containing your playbooks and related roles.
  - **windows_update_playbook.yml**: The main playbook for updating Windows servers.
  - **roles/**: Directory for organizing roles.
    - **common/**: A common role that can be shared across multiple playbooks.
      - **tasks/**: Directory containing the main tasks file (`main.yml`).
      - **handlers/**: Directory containing handlers (`main.yml`).
      - **templates/**: Directory for Jinja2 templates.
      - **files/**: Directory for static files.
      - **vars/**: Directory for role-specific variables (`main.yml`).
    - **windows_updates/**: A specific role for handling Windows updates.
      - **tasks/**: Directory containing the main tasks file (`main.yml`).
      - **vars/**: Directory for role-specific variables (`main.yml`).

- **vars/**: Directory containing variables that apply across different environments.
  - **development.yml**, **staging.yml**, **production.yml**: Variables specific to each environment.

## Sample File Contents

### ansible.cfg

```ini
[defaults]
inventory = inventories/development/hosts.ini
roles_path = playbooks/roles
host_key_checking = False
```

### inventories/development/hosts.ini

```ini
[windows_servers]
winserver1 ansible_host=192.168.1.101 ansible_user=Administrator ansible_password=your_password ansible_port=5986 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore
winserver2 ansible_host=192.168.1.102 ansible_user=Administrator ansible_password=your_password ansible_port=5986 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore
```

### inventories/development/group_vars/windows_servers.yml

```yaml
ansible_user: Administrator
ansible_password: your_password
ansible_port: 5986
ansible_connection: winrm
ansible_winrm_server_cert_validation: ignore
```

### playbooks/windows_update_playbook.yml

```yaml
---
- name: Install all security, critical, and update rollups on Windows Servers
  hosts: windows_servers
  gather_facts: no
  roles:
    - role: windows_updates
```

### playbooks/roles/windows_updates/tasks/main.yml

```yaml
---
- name: Install all available updates
  ansible.windows.win_updates:
    category_names:
      - SecurityUpdates
      - CriticalUpdates
      - UpdateRollups
    state: installed
  register: update_result

- name: Reboot if updates were installed and require a reboot
  ansible.windows.win_reboot:
  when: update_result.reboot_required
```

## How to Use

1. **Clone the Repository**: `git clone https://github.com/yourusername/ansible_project.git`
2. **Navigate to the Project Directory**: `cd ansible_project`
3. **Set Up Your Inventory**: Edit the `hosts.ini` files in the `inventories/` directory to match your environment.
4. **Run the Playbook**:
   ```sh
   ansible-playbook -i inventories/development/hosts.ini playbooks/windows_update_playbook.yml
   ```