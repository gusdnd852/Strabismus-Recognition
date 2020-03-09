"""
@author : Hyunwoong
@when : 2020-03-02
@homepage : https://github.com/gusdnd852
"""
import torch
from torch import nn


class Stem(nn.Module):

    def __init__(self, ):
        super(Stem, self).__init__()

    def forward(self, x):
        b, c, l = x.size()
        criteria = c // 4

        LX = x[:, criteria * 0: criteria * 1, :]
        LY = x[:, criteria * 1: criteria * 2, :]
        RX = x[:, criteria * 2: criteria * 3, :]
        RY = x[:, criteria * 3: criteria * 4, :]

        horizontal = (RX - LX).pow(2)
        vertical = (RY - LY).pow(2)
        return torch.cat([horizontal, vertical, x], dim=1)


class Conv1D(nn.Module):

    def __init__(self, _in, _out, kernel_size):
        super(Conv1D, self).__init__()
        self.conv = nn.Conv1d(_in, _out, kernel_size=kernel_size, padding=kernel_size // 2, groups=1)
        self.batch_norm = nn.BatchNorm1d(_out)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.batch_norm(x)
        return self.relu(x)


class Inception(nn.Module):

    def __init__(self, _in, _out):
        super(Inception, self).__init__()
        self.conv1 = Conv1D(_in, _out // 3, kernel_size=1)
        self.conv3 = Conv1D(_in, (_out // 3) + 1, kernel_size=3)
        self.conv5 = Conv1D(_in, (_out // 3), kernel_size=5)

    def forward(self, x):
        c1 = self.conv1(x)
        c3 = self.conv3(x)
        c5 = self.conv5(x)
        return torch.cat([c1, c3, c5], dim=1)


class Model(nn.Module):

    def __init__(self):
        super(Model, self).__init__()
        self.stem = Stem()

        self.conv1 = Inception(6, 64)
        self.conv2 = Inception(64, 64)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv3 = Inception(64, 256)
        self.conv4 = Inception(256, 256)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv5 = Inception(256, 1024)
        self.conv6 = Inception(1024, 1024)
        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv7 = Inception(1024, 2048)
        self.conv8 = Inception(2047, 2048)
        self.pool4 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.output_layer = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(4094, 1),
            nn.Sigmoid())

    def forward(self, x):
        b, c, l = x.shape
        x = self.stem(x)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.pool1(x)

        x = self.conv3(x)
        x = self.conv4(x)
        x = self.pool2(x)

        x = self.conv5(x)
        x = self.conv6(x)
        x = self.pool3(x)

        x = self.conv7(x)
        x = self.conv8(x)
        x = self.pool4(x)

        x = x.view(b, -1)
        x = self.output_layer(x)
        return x
