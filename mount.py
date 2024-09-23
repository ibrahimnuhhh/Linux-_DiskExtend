import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def extend_and_mount_disk():
    disk = "/dev/sdc"
    partition = "/dev/sdc"
    mount_point = "/mnt/newdisk2"

    # 1. Create mount point if not exists
    print(f"Creating mount point {mount_point} if not exists:")
    run_command(f"sudo mkdir -p {mount_point}")

    # 2. Mount the partition
    print(f"Mounting {partition} to {mount_point}:")
    output = run_command(f"sudo mount {partition} {mount_point}")
    if output is not None:
        print(f"Mount successful: {output}")
    else:
        print(f"Failed to mount {partition} to {mount_point}")

# Run the function
extend_and_mount_disk()
