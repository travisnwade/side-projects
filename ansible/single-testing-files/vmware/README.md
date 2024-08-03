# Ansible Playbook for Querying vCenter Servers and Generating VM Information

This Ansible playbook queries four different vCenter servers to generate a list of virtual machines in JSON format. The list is split into two groups based on whether the virtual machines are running or not. The information includes the virtual machine's name, IP address (if available), VMware tools status, the ESX host the VM is running on, and the datastore location of the VM's disk or disks.

## Prerequisites

1. Ensure the `community.vmware` collection is installed:
   ```bash
   ansible-galaxy collection install community.vmware
   ```
2. Ensure you have the necessary credentials and permissions to access the vCenter servers.

## Playbook

### Variables

- `vcenter_servers`: A list of dictionaries containing the vCenter server details.
- `running_vms`: A list to store information about running VMs.
- `stopped_vms`: A list to store information about stopped VMs.

### Tasks

1. **Gather VM information from each vCenter server**:
   - Uses the `community.vmware.vmware_vm_info` module to gather information about VMs from each vCenter server.

2. **Initialize VM lists**:
   - Initializes the lists for running and stopped VMs.

3. **Process VM information**:
   - Loops through the VM information and splits the VMs into running and stopped groups based on their power state.
   - Collects necessary details like the name, IP address, VMware tools status, ESX host, and datastore locations.

4. **Append to stopped VMs**:
   - Appends the VM data to the stopped VMs list if the VM is powered off.

5. **Output to JSON file**:
   - Writes the lists of running and stopped VMs to a JSON file.

## Usage

1. Update the playbook with your vCenter server details and the correct path for the output JSON file.
2. Run the playbook:
   ```bash
   ansible-playbook query_vcenter_servers.yml
   ```

This playbook will generate a JSON file containing the details of virtual machines from the specified vCenter servers, categorized by their running state.