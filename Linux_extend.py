# -*- coding: utf-8 -*-
import os

def run_command(command):
    """Run the command and return the output."""
    print(f"Running command: {command}")
    result = os.system(command)
    return result == 0  # Check if the command was successful

def ask_confirmation(prompt):
    """Ask for user confirmation (yes/no)."""
    while True:
        choice = input(f"{prompt} (yes/no): ").lower()
        if choice == 'yes':
            return True
        elif choice == 'no':
            return False
        else:
            print("Please enter yes or no.")

def extend_lvm():
    disk = "/dev/sdc"
    partition = "/dev/sdc1"
    vg_name = "sdc_group"  # Updated VG name
    lv_name = "sdclogical"  # Updated LV name
    filesystem = "ext4"  # File system type (ext4, xfs, etc.)

    # 1. Create and extend the partition
    if ask_confirmation(f"You are about to make changes on the {disk} disk. Do you want to continue?"):
        # Use parted for partitioning
        if not run_command(f"echo -e 'mklabel gpt\nmkpart primary ext4 0% 100%\nquit' | sudo parted {disk}"):
            print(f"Partitioning failed for disk: {disk}")
            return

        # Reload the partition table
        if not run_command(f"sudo partprobe {disk}"):
            print(f"Failed to reload partition table for disk: {disk}")
            return

        if ask_confirmation("Partition successfully created. Do you want to continue?"):
            # 2. Create a new physical volume
            if not run_command(f"sudo pvcreate -ff {partition}"):
                print(f"Failed to create physical volume: {partition}")
                return

            # 3. Check if the volume group exists, if not, create it
            if not run_command(f"sudo vgdisplay {vg_name}"):
                print(f"Volume group {vg_name} not found. Creating volume group.")
                if not run_command(f"sudo vgcreate {vg_name} {partition}"):
                    print(f"Failed to create volume group: {vg_name}")
                    return
            else:
                # Add the new physical volume to the volume group
                if not run_command(f"sudo vgextend {vg_name} {partition}"):
                    print(f"Failed to extend volume group: {vg_name}")
                    return

            # 4. Extend the logical volume
            if not run_command(f"sudo lvextend -l +100%FREE /dev/{vg_name}/{lv_name}"):
                print(f"Failed to extend logical volume: {lv_name}")
                return

            # 5. Extend the file system
            if ask_confirmation("Logical volume extended. Do you want to extend the file system?"):
                if filesystem == "ext4":
                    if not run_command(f"sudo resize2fs /dev/{vg_name}/{lv_name}"):
                        print(f"Failed to extend file system: {filesystem}")
                        return
                elif filesystem == "xfs":
                    if not run_command(f"sudo xfs_growfs /dev/{vg_name}/{lv_name}"):
                        print(f"Failed to extend file system: {filesystem}")
                        return
                else:
                    print(f"Unsupported file system type: {filesystem}")
                    return

            print("Operation completed successfully.")
        else:
            print("Operation cancelled.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    extend_lvm()
