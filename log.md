# 20200224
目前进度与想法：
目前计划用Inception架构训练，然后再尝试在网络中加入正则化的层
还在调整输入张量input_tensor

遇到的问题：
构建的one-hot张量 shape=8006*1259197*5=50,405,655,910，服务器上运行说用了300多GiB的内存，
所以需要改一下这个输入张量input_tensor的结构。
目前的想法是，这个1259197（可能）是最长序列的长度（因为可能测量长度的过程也可能有问题）
而有的序列很短，可能就几百。考虑过采样，首先统一每种病毒的数量，然后给每个病毒样本采用大致相同的长度。
并且最终实现更小的shape从而占用少一些内存。
数据预处理方法正在参考阅读A systematic study of the class imbalance problem in convolutional neural networks中

# 20200225
从论文中可以得出  
(i) 不均衡数据会给分类性能带来损害；
(ii) 解决不均衡数据问题的方法中，占主导地位的是过采样，它几乎存在于所有的分析场景中；
(iii) 过采样应该被用在那些需要完全消除不均衡的情况中，而下采样在只需要从一定程度消除不均衡的情况中的效果可能更好；
(iv) 与一些传统的机器学习模型不同的是，过采样也不一定会造成卷积神经网络的过拟合；
(v) 当对被正确分类的例子的总数感兴趣的时候，为了补偿先验类别概率，就应该使用阈值化方法。

class imbalance拟采用过采样，下采样和阈值化方法结合

方案一：
将每个物种的序列的数量控制在100
每个序列的长度控制在10000

# 20200226
碱基只设置ATCGU不行，运行程序出错显示有简并碱基Y，所以我把所有简并碱基都加上了
之后数据one-hot化成功，训练后的训练集形状如下x_train shape: (13700, 10000, 16) 13700*10000*16=2,192,000,000
训练最终accuracy大约93%的时候，val_accuracy大约80%

# 20200227
验证集是用validation_split=0.2，直接在train_data取的后20%的数据。随机的可能不准确
今天的测试在epoch在170-180左右accuracy在0.87左右的时候val_accuracy不再涨了，就在0.78-0.80之间波动。
这个测试的网络是
input_tensor = Input(shape=(max_length, token_index_len))

branch_a = layers.Conv1D(32, 1, activation='relu')(input_tensor)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(64, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(128, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(128, 3, activation='relu')(branch_a)
# branch_a = layers.Flatten()(branch_a)
branch_a = layers.GlobalMaxPooling1D()(branch_a)

branch_b = layers.Conv1D(128, 1, activation='relu')(input_tensor)
branch_b = layers.GlobalMaxPooling1D()(branch_b)

merged = layers.concatenate([branch_a, branch_b], axis=-1)
merged = layers.Dense(512, activation='relu')(merged)
output_tensor = layers.Dense(137, activation='softmax')(merged)

把网络改一下试试。

# 20200228
今天改了这个网络
input_tensor = Input(shape=(max_length, token_index_len))
branch_a = layers.Conv1D(32, 1, activation='relu')(input_tensor)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(64, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(128, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(128, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(256, 3, activation='relu')(branch_a)
# branch_a = layers.Flatten()(branch_a)
branch_a = layers.GlobalMaxPooling1D()(branch_a)

branch_b = layers.Conv1D(256, 1, activation='relu')(input_tensor)
branch_b = layers.GlobalMaxPooling1D()(branch_b)

branch_c = layers.Conv1D(64, 3, activation='relu')(input_tensor)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.Conv1D(128, 3, activation='relu')(branch_c)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.Conv1D(256, 3, activation='relu')(branch_c)
branch_c = layers.GlobalMaxPooling1D()(branch_c)

merged = layers.concatenate([branch_a, branch_b, branch_c], axis=-1)
merged = layers.Dense(512, activation='relu')(merged)
output_tensor = layers.Dense(137, activation='softmax')(merged)

在epoch80的时候accuracy=0.96，val_accuracy=0.84.
又在网上查了下，网络越深效果越好，而且加深度比加宽度效果更好（没有实际验证，而且我觉得宽度也是要适当增加的）。
既然现在验证精度还是这么多，najiu加深宽度试试

branch_a = layers.Conv1D(128, 1, activation='relu')(input_tensor)
branch_a = layers.Conv1D(256, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(256, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(512, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(512, 3, activation='relu')(branch_a)
# branch_a = layers.Flatten()(branch_a)
branch_a = layers.GlobalMaxPooling1D()(branch_a)

branch_b = layers.Conv1D(512, 1, activation='relu', strides=2)(input_tensor)
branch_b = layers.GlobalMaxPooling1D()(branch_b)

branch_c = layers.Conv1D(128, 3, activation='relu')(input_tensor)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.Conv1D(256, 3, activation='relu')(branch_c)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.Conv1D(512, 3, activation='relu')(branch_c)
branch_c = layers.GlobalMaxPooling1D()(branch_c)

branch_d = layers.Conv1D(256, 3, activation='relu')(input_tensor)
branch_d = layers.MaxPooling1D(2)(branch_d)
branch_d = layers.Conv1D(512, 3, activation='relu')(branch_d)
branch_d = layers.GlobalMaxPooling1D()(branch_d)

merged = layers.concatenate([branch_a, branch_b, branch_c, branch_d], axis=-1)
merged = layers.Dense(512, activation='relu')(merged)
output_tensor = layers.Dense(137, activation='softmax')(merged)

# 20200229
加宽度弄得运行的很慢，每个epoch要1100多秒，而且在65epoch的时候accuracy约95-97的时候，val_accuracy约为85-87.5
今天减少宽度，然后加层数。如果效果还不好试试修改kernel_size

branch_a = layers.Conv1D(32, 1, activation='relu')(input_tensor)
branch_a = layers.Conv1D(32, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(64, 3, activation='relu')(branch_a)
branch_a = layers.Conv1D(64, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(128, 3, activation='relu')(branch_a)
branch_a = layers.Conv1D(128, 3, activation='relu')(branch_a)
branch_a = layers.MaxPooling1D(2)(branch_a)
branch_a = layers.Conv1D(256, 3, activation='relu')(branch_a)
branch_a = layers.Conv1D(256, 3, activation='relu')(branch_a)
# branch_a = layers.Flatten()(branch_a)
branch_a = layers.GlobalMaxPooling1D()(branch_a)

branch_b = layers.Conv1D(256, 1, activation='relu', strides=2)(input_tensor)
branch_b = layers.GlobalMaxPooling1D()(branch_b)

branch_c = layers.Conv1D(64, 3, activation='relu')(input_tensor)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.Conv1D(128, 3, activation='relu')(branch_c)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.Conv1D(256, 3, activation='relu')(branch_c)
branch_c = layers.GlobalMaxPooling1D()(branch_c)

branch_d = layers.Conv1D(128, 3, activation='relu')(input_tensor)
branch_d = layers.MaxPooling1D(2)(branch_d)
branch_d = layers.Conv1D(256, 3, activation='relu')(branch_d)
branch_d = layers.GlobalMaxPooling1D()(branch_d)

merged = layers.concatenate([branch_a, branch_b, branch_c, branch_d], axis=-1)
merged = layers.Dense(512, activation='relu')(merged)
output_tensor = layers.Dense(137, activation='softmax')(merged)

用这个模型，深度加了，宽度少了，但是val_accuracy依然也就84-88波动。
试一下增加kernel size

# 20200301
目前在保证运行时间不太长的情况下，val_accuracy

# 20200304
三月1号试了kernel_size为5的，三种情况，分别layers.concatenate包含1，2，4个。结果是4个的最好。
三月2号试了kernel_size为1，2，3的三种情况，3的最好
三月3号试了kernel_size为1，3，4的三种情况，其中1的epoch200次，3月2号的是100次，4的是100次，3的是加深度的（分支strides=2）的100次。
加了深度但是分支strides=2反而val_accuracy低了。所以去掉strides=2，然后再加深度。

# 20200305
VirusDetect是用small RNAs来virus discovery

# 20200308
137个科，每个科取10000次，每次10000长度。每个科就是一共取了一亿长度。
但是种最多的科是1146个种，假设每个种长度5万，那总长度就是5千万。
这里可能存在每个科取了很多重复数据的情况。

在sequences_integrated.xlsx的sheet4中，一共有865个属。考虑在属的级别上进行分类。

同时今天在训练中，在epoch=1中，1/9563到806/9563，loss下降，accuracy上升到0.0117；
在之后812/9563到目前已经训练到的2141/8563过程中，loss依然在下降，但是accuracy也下降0.0088。
这个现象在知乎<https://www.jianshu.com/p/ab539e9a7955>中找了个解释如下:
```
loss下降的同时accuracy下降表示进入overfitting的领域，可以想象成你的模型在训练中依然进步，但是在validation set上测出的accuracy已经开始下降了。  
接下来，accuracy反升，这表示你的模型中的regularization开始起作用，在成功遏制overfitting，于是你的accuracy开始回升，但是作为代价你的loss会退步，因为你的模型在阻止自己过度拟合训练数据。
简单来说，双降表示你的模型在训练数据中一头扎得太深，双升表示你的模型意识到这个问题，开始回过头来补救。
```

# 20200309
还是有在第二个epoch就loss和accuracy都是nan的问题。
cy说可能数据有问题。在网上查的时候发现这个<https://www.jianshu.com/p/c969ae433932>

```
1）注意到函数中使用yield返回数据

2）注意到函数使用while True 来进行循环，目前可以认为这是一个必要的部分，这个函数不停的在while中进行循环

3）由于是在while中进行循环，我们需要在while中进行设置初始化，而不要在while循环外进行初始化；我刚开始在load_validate函数中没有初始化 images = []和labels = []，导致程序出错。因为我在while循环中最后将这两个数据都变成了numpy的数据格式，当进行第二轮数据产生时，numpy的数据格式是没有append的函数的，所以会出错。

4）程序中具体的数据运算不需要太多了解，不过这里给出一个简单的说明，以助于理解：在train数据中，我试图从一个很大的图片数据库中随机选择batch_size个图片，然后进行resize变换。这是一张图片的过程。为了读取多张图片，我是先将每一个图片都读入一个列表中，这是为了使用列表的append这个追加数据的功能（我觉得这个功能其实挺好用的），最后，把要训练的一个batch数据转成numpy的array格式。

5）除了while True 和 yield，大家留意一下这里的循环和初始化，比较容易出错。
```

第三条，我的generator里i在while外面初始化了。所以我觉得可能是从epoch=2开始，i的数值超过train_data的长度了，所以训练数据都是空的。导致nan。

## 20200310

在改好了generator之后发现原本用batch_size=128训练的时候，到epoch=6-8的时候，loss和accuracy都不变了。
网上查有下面的几种说法：

```
（1）loss不变，判断为梯度消失情况，改用relu激活，或者添加batchnormal
（2）实际使用中，增大batch_size,调小learning rate 也可以继续让loss降低（在训练过程中动态调节某些参数值：比如优化器的学习率，用ReduceLROnPlateau函数）
（3）问题解决了，是激活函数的问题，relu激活函数的激活率太低，很多神经元死掉了
```
