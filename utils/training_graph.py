"""
@author : Hyunwoong
@when : 2020-03-11
@homepage : https://github.com/gusdnd852
"""
from configuration import *
import re
import matplotlib.pyplot as plt


class GraphDrawer:

    def read_file(self, file_name):
        f = open(file_name, 'r')
        file = f.read()
        file = re.sub('\\[', '', file)
        file = re.sub('\\]', '', file)
        f.close()

        return [float(i) for idx, i in enumerate(file.split(','))]

    def draw_accuracy(self, step):
        train = self.read_file(root_path + '\\log\\train_accuracy_{}.txt'.format(step))
        test = self.read_file(root_path + '\\log\\test_accuracy_{}.txt'.format(step))
        plt.plot(train, 'b', label='train acc')
        plt.plot(test, 'r', label='test acc')
        plt.xlabel('step ({} times)'.format(record_per_step))
        plt.ylabel('acc')
        plt.title('training result - trial : {}'.format(step))
        plt.legend(loc='lower left')
        plt.grid(True, which='both', axis='both')
        plt.show()

    def draw_error(self, step):
        train = self.read_file(root_path + '\\log\\train_error_{}.txt'.format(step))
        test = self.read_file(root_path + '\\log\\test_error_{}.txt'.format(step))
        plt.plot(train, 'y', label='train error')
        plt.plot(test, 'g', label='test error')
        plt.xlabel('step ({} times)'.format(record_per_step))
        plt.ylabel('error')
        plt.title('training result - trial : {}'.format(step))
        plt.legend(loc='lower left')
        plt.grid(True, which='both', axis='both')
        plt.show()

    def draw_both(self, step):
        self.draw_error(step)
        self.draw_accuracy(step)


if __name__ == '__main__':
    drawer = GraphDrawer()
    drawer.draw_both(0)
