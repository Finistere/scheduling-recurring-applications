from master import generator
from master.resource_manager import DummyRM
from master.stat_collector import DummyStatCollector, Server
from master.yarn_workloader import Experiment
from master.scheduler import RoundRobin
from master.complementarity import EpsilonGreedy
import os.path
from pathlib import Path

DUMMIES_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / 'dummies'


class TestGenerators:

    def test_cluster(self):
        with open(DUMMIES_DIR / 'config.yaml') as config:
            cluster = generator.cluster(config)
        rm = cluster.resource_manager

        assert isinstance(cluster.stat_collector, DummyStatCollector)
        assert isinstance(rm, DummyRM)
        assert rm.n_nodes == 5
        assert rm.n_containers == 7
        assert rm.node_pattern == "NN{}"
        assert rm.app_pattern == "AA{}"
        assert rm.apps_running == {
            'test': True
        }
        assert rm.apps_submitted == 2
        assert rm.apps_finished == {
            'test': True
        }
        assert cluster.nodes["NN0"].n_containers == 7

        assert Server.disk_max == 500
        assert Server.net_max == 450
        assert Server.disk_name == "disk"
        assert Server.net_interface == "net"

    def test_experiment(self):
        with open(DUMMIES_DIR / 'jobs.xml') as jobs_xml:
            exp = generator.experiment(jobs_xml.read(), 4)

        assert len(exp.applications) == 4

    def test_scheduler(self):
        with open(DUMMIES_DIR / 'config.yaml') as config, \
                open(DUMMIES_DIR / 'jobs.xml') as jobs_file, \
                open(DUMMIES_DIR / 'experiment.xml') as exp_file:
            scheduler = generator.scheduler(
                scheduler_class=RoundRobin,
                estimation_class=EpsilonGreedy,
                exp_xml_str=exp_file.read(),
                jobs_xml_str=jobs_file.read(),
                config_yaml=config,
                estimation_kwargs={
                    'epsilon': 10
                }
            )
            exp_file.seek(0)
            jobs_file.seek(0)
            exp = Experiment(exp_file, jobs_xml=jobs_file)

        assert isinstance(scheduler, RoundRobin)

        estimation = scheduler.estimation
        assert isinstance(estimation, EpsilonGreedy)
        assert estimation.epsilon == 10

        assert len(scheduler.queue) == len(exp.applications)
        for i in range(len(scheduler.queue)):
            assert scheduler.queue[i].is_a_copy_of(exp.applications[i])
