from typing import List
# noinspection PyPep8Naming
from numpy import ndarray as NDArray

from src import collects, clustering
from src.clusters_info import calc_cluster_dist
from src.evolution import ChildGenerator
from src import pathways_generating as generation
from src import pathways_processing as process
import logging
import random

logger = logging.getLogger('main_logger')

SYNT_PATH_EXPECT_NUM = 750


class RunnerBuilder(object):

    def __init__(self):
        self.__idx = None
        self.__fav_idx = None
        self.__act_path_mtrx = None
        self.__cluster_centers = None
        self.__cluster_probs = None
        self.__fav_subpaths = None
        self.__act_fav_count = None

    def set_idx(self, idx: int):
        self.__idx = idx

    def set_fav_idx(self, fav_idx: int):
        self.__fav_idx = fav_idx

    def set_act_path_mtrx(self, act_path_mtrx: List[List[str]]):
        self.__act_path_mtrx = act_path_mtrx

    def set_cluster_centers(self, cluster_centers: List[str]):
        self.__cluster_centers = cluster_centers

    def set_cluster_probs(self, cluster_probs: NDArray):
        self.__cluster_probs = cluster_probs

    def set_fav_subpaths(self, fav_subpaths: List[str]):
        self.__fav_subpaths = fav_subpaths

    def set_act_fav_count(self, act_fav_count: int):
        self.__act_fav_count = act_fav_count

    class __Runner(object):

        def __init__(self, idx: int, fav_idx: int, act_path_mtrx: List[List[str]], cluster_centers: List[str],
                     cluster_probs: NDArray, fav_subpaths: List[str], act_fav_count: int):
            self.__idx = idx
            self.__fav_idx = fav_idx
            self.__act_path_mtrx = act_path_mtrx
            self.__cluster_centers = cluster_centers
            self.__cluster_probs = cluster_probs
            self.__fav_subpaths = fav_subpaths
            self.__act_fav_count = act_fav_count

        @property
        def idx(self) -> int:
            return self.__idx

        @property
        def fav_idx(self) -> int:
            return self.__fav_idx

        @property
        def act_path_mtrx(self) -> List[List[str]]:
            return self.__act_path_mtrx

        @property
        def cluster_centers(self) -> List[str]:
            return self.__cluster_centers

        @property
        def cluster_probs(self) -> NDArray:
            return self.__cluster_probs

        @property
        def fav_subpaths(self) -> List[str]:
            return self.__fav_subpaths

        @property
        def act_fav_count(self) -> int:
            return self.__act_fav_count

        def run(self):
            cluster_dist = calc_cluster_dist(self.cluster_probs, SYNT_PATH_EXPECT_NUM)
            synt_path_mtrx = generation.collect_all_pathways_by_clusters(cluster_dist)
            synt_paths = process.flatten_all_pathways_by_clusters(synt_path_mtrx)
            if self.fav_subpaths[-1] not in synt_paths:
                logger.error('Not valid for estimation')
                logger.info('Run skipped')
                return
            number_of_steps = len(self.fav_subpaths)
            intermediate_step_index = number_of_steps // 2
            last_step_index = number_of_steps - 1
            clustering.print_quality_info(synt_paths, self.cluster_centers, self.fav_idx)
            for step_idx, fav_subpath in enumerate(self.fav_subpaths):
                logger.info('Step {}/{}: {}'.format(step_idx, last_step_index, fav_subpath))
                remained_paths, deleted_paths = process.filter_pathways(synt_paths, fav_subpath, step_idx == last_step_index)
                synt_paths = generation.generate_new_pathways(remained_paths, len(synt_paths))
                clustering.print_quality_info(synt_paths, self.cluster_centers, self.fav_idx)

    def build(self) -> '__Runner':
        args = (self.__idx, self.__fav_idx, self.__act_path_mtrx, self.__cluster_centers,
                self.__cluster_probs, self.__fav_subpaths, self.__act_fav_count)
        return RunnerBuilder.__Runner(*args)
