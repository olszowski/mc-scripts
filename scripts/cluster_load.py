import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NodeInfo:
    def __init__(self, line):
        logger.debug(line)
        parameters = line.split(" ")
        logger.debug(parameters)
        self.node_id = parameters[0]
        self.partition = parameters[1]
        self.load = parameters[2]
        self.state = parameters[3]

        cpu = parameters[4].split('/')
        self.cpu_available = int(cpu[0])
        self.cpu_idle = int(cpu[1])
        self.cpu_other = int(cpu[2])
        self.cpu_total = int(cpu[3])

    def is_idle(self):
        return self.state == "idle"

    def is_mixed(self):
        return self.state == "mixed"


class ClusterLoad:
    def __init__(self, cluster_state):
        self.total_nodes_count = len(cluster_state.nodes_info)
        self.idle_nodes_count = len(cluster_state.get_idle_nodes())
        self.mixed_nodes_count = len(cluster_state.get_mixed_nodes())
        self.idle_capacity = int(cluster_state.capacity_idle())
        self.mixed_capacity = int(cluster_state.capacity_mixed())
        self.total_capacity = int(cluster_state.max_total_capacity())
        self.capacity_idle_perc = round(1.0 * self.idle_capacity / self.total_capacity * 100, 1)
        self.capacity_mixed_perc = round(1.0 * self.mixed_capacity / self.total_capacity * 100, 1)

    def __str__(self) -> str:
        return f'''
Idle nodes: {self.idle_nodes_count}
Mixed nodes: {self.mixed_nodes_count}
Total nodes: {self.total_nodes_count}

Idle nodes capacity: {self.idle_capacity} ({self.capacity_idle_perc}%)
Mixed nodes capacity: {self.mixed_capacity} ({self.capacity_mixed_perc}%)
Total cluster capacity: {self.total_capacity}
        '''


class ClusterState:
    def __init__(self, nodes_info):
        """
        :type nodes_info: list of NodeInfo
        """
        self.nodes_info = nodes_info

    def get_idle_nodes(self):
        return [node for node in self.nodes_info if node.is_idle()]

    def get_mixed_nodes(self):
        return [node for node in self.nodes_info if node.is_mixed()]

    def capacity_idle(self):
        idles = [node.cpu_idle for node in self.get_idle_nodes()]
        from functools import reduce
        return reduce((lambda x, y: x + y), idles, 0)

    def capacity_mixed(self):
        idles = [node.cpu_idle for node in self.get_mixed_nodes()]
        from functools import reduce
        return reduce((lambda x, y: x + y), idles, 0)

    def max_total_capacity(self):
        idles = [node.cpu_total for node in self.nodes_info]
        from functools import reduce
        return reduce((lambda x, y: x + y), idles, 0)

    def max_available_capacity(self):
        capacities = [node.cpu_idle for node in self.get_mixed_nodes().extend(self.get_idle_nodes())]
        from functools import reduce
        return reduce((lambda x, y: x + y), capacities, 0)

    def current_load(self):
        return ClusterLoad(self)

    def __sort(self, nodes):
        from operator import attrgetter
        return sorted(nodes, key=attrgetter('state', 'load', 'cpu_idle'))


def cluster_status_from_stdout(std_out):
    splitted_output = std_out.split("\n")[1:]
    nodes = []
    for line in splitted_output:
        try:
            nodeinfo = NodeInfo(line)
            nodes.append(nodeinfo)
        except Exception:
            logger.info("Unable to parse line, skipping: " + line)
    cluster_info = ClusterState(nodes)
    return cluster_info


def get_cluster_state_from_os(partition):
    from subprocess import check_output, STDOUT
    from shlex import split
    command = "sinfo --partition={partition} --format='%n %P %O %T %C'" \
        .format(partition=partition)
    output = check_output(split(command), shell=False, stderr=STDOUT).decode("UTF-8")
    cluster_info = cluster_status_from_stdout(output)
    return cluster_info


if __name__ == '__main__':
    print(get_cluster_state_from_os("plgrid").current_load())
