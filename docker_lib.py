import subprocess
import json

def get_container_list() -> list:
    command = ["docker", "ps"]
    responce = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    containers = responce.stdout.read().decode().splitlines()[1:]
    container_data = []
    for i in range(len(containers)):
        # for debug
        # print(str(i) + ': ' + containers[i])
        containers[i] = list(filter(None, containers[i].split()))
        container_data.append({
            'id': containers[i][0],
            'image': containers[i][1],
            'command': containers[i][2],
            # X <XXX> ago
            'created': containers[i][3] + ' ' + containers[i][4] + ' ' + containers[i][5],
            # Up X <XXX>
            'status': containers[i][6] + ' ' + containers[i][7] + ' ' + containers[i][8] + ' ' + containers[i][9],
            'ports': containers[i][10] + ' ' + containers[i][11],
            'names': containers[i][12]
        })

    # for debug
    # for i in range(len(container_data)):
    #    print(str(i) + ': ' + str(container_data[i]))
    return container_data


def create_container(image: str, opts: str, cmds: str, args: list):
    command = ["docker", "create"]
    if opts != '':
        command.append(opts)
    command.append(image)
    if cmds != '':
        command.append(cmds)
    if args or args is None or len(args) != 0:
        command.append(args)
    responce = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outs = responce.stdout.read().decode().splitlines()

    # for debug
    # print(outs)


def run_container(container_id: str) -> bool:
    command = ["docker", "start", container_id]
    responce = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outs = responce.stdout.read().decode().splitlines()
    return outs[0] == container_id
    # for debug
    # print(outs)


def stop_container(container_id: str) -> bool:
    command = ["docker", "stop", container_id]
    responce = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outs = responce.stdout.read().decode().splitlines()
    return outs[0] == container_id
    # for debug
    # print(outs)


def is_container_running(container_id: str) -> bool:
    command = ["docker", "inspect", container_id]
    responce = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outs = json.loads(responce.stdout.read().decode())
    return outs[0]['State']['Running']
    # for debug
    # print(outs)
