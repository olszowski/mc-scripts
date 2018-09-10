from unittest import TestCase

stdout = """HOSTNAMES PARTITION NODES CPU_LOAD STATE CPUS(A/I/O/T)
p0615 plgrid* 3.92 mixed 16/8/0/24
p0620 plgrid* 0.41 idle 0/24/0/24
p0627 plgrid* 4.00 mixed 16/8/0/24"""


class ClusterLoadTest(TestCase):

    def test(self):
        from scripts.cluster_load import cluster_status_from_stdout
        cluster = cluster_status_from_stdout(stdout)
        self.assertEquals(cluster.current_load().total_capacity, 72)
        print(cluster.current_load())
