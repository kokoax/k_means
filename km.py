#! coding: utf-8
import sys
import random
import math
import numpy as np
# import matplotlib.pyplot as plt
import re
from sklearn import datasets

class KMeans:
    def __init__(self, K):
        self.K = K
        self.nrow = 0
        self.ncol = 0
        self.data_flg = 0
        self.all_data_sets = None
        self.data_sets = self.getDataSets()
        self.CoGs = self.getFirstCoG(self.K) # plural of Center of Gravity.

        while(True):
            self.clustering()

            beforeCoGs = self.CoGs[:]
            self.updateCoGs()
            if np.array_equal(beforeCoGs, self.CoGs):
                break

    def data_load(filename):
        f = open("input/".join(filename))

        line = f.readline()
        ret = []
        while line:
            ret.append(map(lambda val:float(val), re.split(r'[,:]',line)))
            line = f.readline()
        self.ncol = ret.size()
        self.nrow = ret[0].size()

    def getDataSets(self):
        if self.data_flg == 0:
            data_sets = datasets.load_iris()
        elif self.data_flg == 1:
            data_sets = datasets.load_digits()
        elif self.data_flg == 2:
            return data_load("haberman.data")

        self.all_data_sets = data_sets
        self.nrow, self.ncol = data_sets.data.shape
        return [
                {
                    'name':data_sets.target[i],
                    'data':data_sets.data[i],
                    'cluster':-1
                } for i in range(self.nrow)
        ]

    def getFirstCoG(self, K):
        return [self.data_sets[rand_i]['data']
                    for rand_i in [random.randint(0,self.nrow-1)
                        for i in range(self.K)]]

    def clustering(self):
        for feature in self.data_sets:
            i = 0
            min_i = 0;
            # python3からは,整数に上限がなくなったそうで、とりあえずでかい数値で解決
            min_distance = 100000000000000000;
            for CoG in self.CoGs:
                distance = 0
                for point in [
                        {
                            'CoG':CoG[j],
                            'feature':feature['data'][j]
                        } for j in range(self.ncol)
                ]:
                    distance += (point['CoG']-point['feature']) ** 2

                if( math.sqrt(distance) < min_distance ):
                    min_i = i
                    min_distance = math.sqrt(distance)
                i += 1

            feature['cluster'] = min_i

    def updateCoGs(self):
        classes = [
                {'sum_point':[0 for i in range(self.ncol)], 'count':1}
                        for i in range(self.K)
        ]

        for feature in self.data_sets:
            for i in range(self.ncol):
                classes[feature['cluster']]['sum_point'][i] += feature['data'][i]
            classes[feature['cluster']]['count'] += 1

        for i in range(self.K):
            self.CoGs[i] = np.array([classes[i]['sum_point'][j]/classes[i]['count']
                for j in range(self.ncol)])

    def allClusterSumOfDistance(self):
        all_distance = 0
        for feature in self.data_sets:
            for CoG in self.CoGs:
                distance = 0
                for point in [{'CoG':CoG[i], 'feature':feature['data'][i]}
                        for i in range(self.ncol)]:
                    distance += (point['CoG']-point['feature'])**2
                all_distance += math.sqrt(distance)

        return all_distance

    # この値が小さいほどいい評価
    def intraClusterSumOfDistance(self):
        cluster_sum_distance = [0 for i in range(self.K)]
        for feature in self.data_sets:
            cluster = feature['cluster']
            for CoG in self.CoGs:
                distance = 0
                for point in[{'CoG':CoG[i], 'feature':feature['data'][i]}
                        for i in range(self.ncol)]:
                    distance += (point['CoG']-point['feature'])**2
                cluster_sum_distance[cluster] += math.sqrt(distance)

        return cluster_sum_distance

    def pseudoCalc(self, distance):
        sum_distance = self.allClusterSumOfDistance()
        return (((sum_distance-distance)/(self.K-1)) /
                (distance+1/(self.nrow-self.K)))

    def pseudo(self):
        class_pseudo = []
        for distance in self.intraClusterSumOfDistance():
            class_pseudo.append(self.pseudoCalc(distance))
        return class_pseudo

    def clusterCount(self):
        count = [0 for i in range(self.K)]
        for fueature in self.data_sets:
            count[fueature['cluster']] += 1
        return count

    def classCountInCluster(self, cluster):
        # クラス名を数値(0~K)にして管理
        count = [0 for i in range(len(self.all_data_sets.target_names))]
        c = 0
        for data in self.data_sets:
            # print("%d: %d == %d" % (c, data['name'], cluster))
            if data['cluster'] == cluster:
                if count[data['name']] == {}:
                    count[data['name']] = 0
                else:
                    count[data['name']] += 1
            c += 1
        return count

    def correctCount(self):
        count = 0
        for data in self.data_sets:
            data.name

    def entropy(self):
        ret = 0
        cluster = 0
        # TODO: (nが0のときがある)クラスタに何も割り振られない可能性があり ZeroDivisionになるときがある
        # ただし、K-meansでは一般にクラスの数がわかっているときに使用されるので無視できる
        i = 0
        for n in self.clusterCount():
            j = 0
            print("|Cluster_%d|: %d" % (j, n))
            tmp = 0
            for count in self.classCountInCluster(cluster):
                print("|Cluster_%d & Class_%d|: %d" % (j, i, count))
                # countが0のときは無視する
                if count != 0:
                    print("P(%d,%d) = %lf" % (i, j, (count/n)*(math.log(count/n))))
                    tmp += (count/n)*(math.log(count/n))
                j += 1
            print("∑P(i,j)logP(i,j) = ", tmp)
            ret += (n/self.nrow)*tmp # N 総データ数
            print("n/n_j * ∑P(i,j)logP(i,j) = ", ret)
            cluster += 1
            i += 1
        # return ret
        # print(self.K)
        return -1*math.log(self.K) * ret

    # def plotCluster(self):
    #     plt.plot(1,0)

args = sys.argv

K = int(args[1])
km = KMeans(K)
# for i in range(km.nrow):
#     print(km.data_sets[i])
# print("K:", K)
# print("二乗和")
# print(km.intraClusterSumOfDistance())
# print(sum(km.intraClusterSumOfDistance()))
# print("Pseudo")
# print(km.pseudo())
# print(sum(km.pseudo()))

# print("Entropy: ", km.entropy())
print(km.entropy())

