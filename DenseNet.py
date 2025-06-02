import torch.nn as nn
import torch
import math
class SingleLayer(nn.Module):
    def __init__(self, num_channels, growth_rate):
        super(SingleLayer,self).__init__()
        self.conv = nn.Conv2d(num_channels,growth_rate,3,padding = 1, bias=False)
        self.norm = nn.BatchNorm2d(num_channels)
        self.relu = nn.LeakyReLU()
    def forward(self,x):
        x1 = self.relu(self.norm(x))
        x2 = self.conv(x1)
        return torch.cat((x,x2),1)#skip connection
#Bottle nexk basically the same as single layer but with a 1x1 conv and 3x3 conv with larger channels in between the two
class Bottlenet(nn.Module):
    def __init__(self,in_channels, growth_rate):
        super(Bottlenet,self).__init__()
        channel_1 = growth_rate * 4
        self.conv_1 = nn.Conv2d(in_channels, channel_1,1, bias=False)
        self.norm_1 = nn.BatchNorm2d(in_channels)
        self.conv_2 = nn.Conv2d(channel_1,growth_rate,3,padding=1, bias=False)
        self.norm_2 = nn.BatchNorm2d(channel_1)
        self.relu = nn.LeakyReLU()
    def forward(self,x):
        x1 = self.relu(self.norm_1(x))
        x2 = self.conv_1(x1)
        x3 = self.relu(self.norm_2(x2))
        x4 = self.conv_2(x3)
        return torch.cat((x,x4),1)#skip connection
#an avg pool layer to transistion between sizes
class TransLayer(nn.Module):
    def __init__(self,in_channels, out_channels):
        super(TransLayer,self).__init__()
        self.conv = nn.Conv2d(in_channels,out_channels,3,padding = 1, bias=False)
        self.norm = nn.BatchNorm2d(in_channels)
        self.relu = nn.LeakyReLU()
        self.avg_pool = nn.AvgPool2d(2)
    def forward(self,x):
        x1 = self.relu(self.norm(x))
        x2 = self.conv(x1)
        return self.avg_pool(x2)
class DenseNet(nn.Module):
    def __init__(self, growth_rate, depth, reduction, num_classes, bottleneck):
        super(DenseNet,self).__init__()
        #first convolutions/norm
        num_dense_blocks = (depth-4) //3
        if(bottleneck):
            num_dense_blocks = num_dense_blocks//2
        num_channels = growth_rate * 2
        self.conv_1 = nn.Conv2d(3,num_channels, 3, padding=1, bias=False)
        #first dense block
        self.dense_1 = self._make_dense(num_channels,growth_rate,num_dense_blocks=num_dense_blocks,bottleneck=bottleneck)
        num_channels += num_dense_blocks * growth_rate#scale input channels
        out_channel = int(math.floor(num_channels*reduction))#scale output channels
        self.tran_1 = TransLayer(num_channels,out_channel)
        num_channels = out_channel#update input channels for next block
        #second dense block
        self.dense_2 = self._make_dense(num_channels,growth_rate,num_dense_blocks=num_dense_blocks,bottleneck=bottleneck)
        num_channels += num_dense_blocks * growth_rate#scale input channels
        out_channel = int(math.floor(num_channels*reduction))#scale output channels
        self.tran_2 = TransLayer(num_channels,out_channel)
        num_channels = out_channel#update input channels for next block
        #third dense block
        self.dense_3 = self._make_dense(num_channels,growth_rate,num_dense_blocks=num_dense_blocks,bottleneck=bottleneck)
        num_channels += num_dense_blocks * growth_rate#scale input channels
        out_channel = int(math.floor(num_channels*reduction))#scale output channels
        self.tran_3 = TransLayer(num_channels,out_channel)
        num_channels = out_channel#update input channels for next block

        #fourth Dense Block
        self.dense_4 = self._make_dense(num_channels,growth_rate,num_dense_blocks=num_dense_blocks,bottleneck=bottleneck)
        num_channels += num_dense_blocks * growth_rate#scale input channels
        #Final Layer
        self.norm = nn.BatchNorm2d(num_channels)
        self.fc = nn.Linear(num_channels, num_classes)
        self.relu = nn.LeakyReLU()
        self.avg_pool = nn.AvgPool2d(8)
        self.log_softmax = nn.LogSoftmax()
        self.flatten = torch.flatten()
        #intialize wieghts
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.bias.data.zero_()
    def forward(self, x):
        x1 = self.conv_1(x)
        
        x2 = self.dense_1(x1)
        x3 = self.tran_1(x2)

        x4 = self.dense_2(x3)
        x5 = self.tran_2(x4)

        x6 = self.dense_3(x5)
        x7 = self.tran_3(x6)

        x8 = self.dense_4(x7)
        x9 = self.avg_pool(self.relu(self.norm(x8)))
        
        #return self.log_softmax(self.fc(self.flatten(x7)))
        return self.fc(self.flatten(x9))

    #function that makes an nn.Sequential base on the parameters I give it
    def _make_dense(self, num_channels, growth_rate, num_dense_blocks, bottleneck):
        layers = []
        for i in range(num_dense_blocks):
            if(bottleneck):#if we want a bottleneck block
                layers.append(Bottlenet(num_channels,growth_rate))
            else:
                layers.append(SingleLayer(num_channels=num_channels, growth_rate=growth_rate))
            num_channels+= growth_rate#grow as we iterate thru layers
        return nn.Sequential(*layers)#convert our list of layers into a sequential NN for ease