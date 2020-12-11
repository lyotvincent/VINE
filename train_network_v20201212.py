import os
from math import ceil
import numpy as np
import keras
from keras.models import Model
from keras import layers
from keras import Input
from keras import regularizers
from keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
# from keras.optimizers import RMSprop
import keras.optimizers as optimizers

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# def load_data():
#     accession_file = open('./accession_family_labels_v2.txt', 'r')
#     lines = accession_file.readlines()
#     accession_file.close()

#     for line in lines:
#         splitted_line = line.strip().split(',')
#         fna_file = open('./train_data/'+splitted_line[0]+'.fna', 'r')
#         fna_lines = fna_file.readlines()
#         fna_file.close()
        
#         for i in range(len(fna_lines)):
#             if i == 0:
#                 fna_lines[i] = ''
#             fna_lines[i] = fna_lines[i].strip()

#         train_data.append(''.join(fna_lines).strip())
#         train_labels.append(splitted_line[2])

def load_data():
    train_data_file = open('./train_data_1000.fasta', 'r')
    lines = train_data_file.readlines()
    train_data_file.close()

    for line in lines:
        if line.startswith('>'):
            train_labels.append(line.split('_')[1])
        else:
            train_data.append(line.strip())



print('Loading data...')
# 训练集，其中一部分取出作为验证集
# train_data = ['ATATCTGAATGTAGTAGTAGTAGTCAGTCGTAGCTGCTAGCTGTGCTAGCTGTCGTAGCTAGCTCGTAGCTCGATCGTAGTAGTCAGTCGTAGCTGCTAGCTGTGCTAGCTGTCGTATAGTAGTCAGTCGTAGCTGCTAGCTGTGCTAGCTGTCGTATAGTAGTCAGTCGTAGCTGCTAGCTGTGCTAGCTGTCGTA', 'TTGAACGTTGAATGTAGTAGTAGTAGTCAGTCGTAGCTGCTAGCTGTGCTAGCTGTCGTAGCTAGCTCGTAG']
train_data = []
# 训练集标签，与训练集一一对应，表示每个输入训练集的预期分类结果
# >>> train_labels[10]
# 3
# 3是一个物种的种类的代号，代表train_data[10]属于3这个物种的分类
# TODO 给下载的数据物种分类生成标签号后然后读取到这
train_labels = []
# 测试集，在用训练集和验证集训练完后使用测试集测试
# test_data = 
# 测试集标签，与测试集一一对应
# test_labels =  

load_data()
print('train_data_length=', len(train_data))
print('train_labels_length=', len(train_labels))
print('Finish loading data!!!')
if len(train_data) != len(train_labels):
    print('len(train_data) != len(train_labels)')
    exit()

max_length = len(max(train_data, key=len))
print('max_length: ', max_length)

# 先均匀从训练集中抽取一部分作为验证集，取20%
print('Extracting validation data...')
validation_data = []
validation_labels = []
for i in range(137):
    # validation_data += train_data[8000*i+4000:8000*i+6000]
    # train_data = train_data[:8000*i+4000]+train_data[8000*i+6000:]
    # validation_labels += train_labels[8000*i+4000:8000*i+6000]
    # train_labels = train_labels[:8000*i+4000]+train_labels[8000*i+6000:]
    for j in range(10):
        validation_data += train_data[800*i+j*100+40:800*i+j*100+60]
        validation_labels += train_labels[800*i+j*100+40:800*i+j*100+60]
    train_data = train_data[:800*i+40]+train_data[800*i+60:800*i+140]+train_data[800*i+160:800*i+240]+train_data[800*i+260:800*i+340]+train_data[800*i+360:800*i+440]+train_data[800*i+460:800*i+540]+train_data[800*i+560:800*i+640]+train_data[800*i+660:800*i+740]+train_data[800*i+760:800*i+840]+train_data[800*i+860:800*i+940]+train_data[800*i+960:]
    train_labels = train_labels[:800*i+40]+train_labels[800*i+60:800*i+140]+train_labels[800*i+160:800*i+240]+train_labels[800*i+260:800*i+340]+train_labels[800*i+360:800*i+440]+train_labels[800*i+460:800*i+540]+train_labels[800*i+560:800*i+640]+train_labels[800*i+660:800*i+740]+train_labels[800*i+760:800*i+840]+train_labels[800*i+860:800*i+940]+train_labels[800*i+960:]


print('train_data_length=', len(train_data))
print('train_labels_length=', len(train_labels))
print('train_labels_number=', len(set(train_labels)))
print('validation_data_length=', len(validation_data))
print('validation_labels_length=', len(validation_labels))
print('validation_labels_number=', len(set(train_labels)))
print('Finish extracting validation data...')

train_data = np.array(train_data)
train_labels = np.array(train_labels)
validation_data = np.array(validation_data)
validation_labels = np.array(validation_labels)



# 打乱数据，否则validation_split会只取相同类的样本，自己取
print('Shuffling data...')
index_in_shuffle = np.arange(len(train_data))
np.random.shuffle(index_in_shuffle)
train_data = train_data[index_in_shuffle]
train_labels = train_labels[index_in_shuffle]

index_in_shuffle = np.arange(len(validation_data))
np.random.shuffle(index_in_shuffle)
validation_data = validation_data[index_in_shuffle]
validation_labels = validation_labels[index_in_shuffle]
print('Finish shuffling data!!!')

# for i in train_data:
#     print(len(i))

# token_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'N': 4}
# token_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'U': 4, 'W': 5, 'S': 6, 'K': 7, 'M': 8, 'Y': 9, 'R': 10, 'B': 11, 'D': 12, 'H': 13, 'V': 14, 'N': 15}
token_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'W': 4, 'S': 5, 'K': 6, 'M': 7, 'Y': 8, 'R': 9, 'B': 10, 'D': 11, 'H': 12, 'V': 13, 'N': 14}
token_index_len = len(token_index)

def vectorize_sequences(sequences, dimension):
#     print('Vectorizing data...')
    results = np.zeros(shape=(len(sequences), dimension, token_index_len))

    for i, sample in enumerate(sequences):
        for j, character in enumerate(sample):
            index = token_index.get(character)
            if index is None:
                print('index is none: ', i, j, character)
                exit()
            results[i, j, index] = 1.
#     print('Finish vectorizing data...')
    return results

batch_size = 256

def generator(input_data, input_labels, batch_size=batch_size):
    i = -1
    input_data_len = len(input_data)
    while True:
        i += 1
        if i * batch_size > input_data_len:
            i = 0
        samples = input_data[batch_size*i:batch_size*(i+1)]
        labels = input_labels[batch_size*i:batch_size*(i+1)]
        # print('labels_number=', len(set(labels)))
        samples = vectorize_sequences(samples, max_length)
        labels = to_categorical(labels, num_classes=137)
        # print(labels)
        yield samples, labels



# print('Vectorizing train data...')
# # x_train就是向量化的训练集train_data
# x_train = vectorize_sequences(train_data, max_length)
# print(x_train)
# print('x_train shape:', x_train.shape)
# print('Finish vectorizing train data...')

# print('Vectorizing validation data...')
# # x_validation就是向量化的训练集validation_data
# x_validation = vectorize_sequences(validation_data, max_length)
# print(x_validation)
# print('x_validation shape:', x_validation.shape)
# print('Finish vectorizing validation data...')

# # python深度学习p61，one_hot_train_labels就是向量化后的训练集标签
# # TODO 给下载的数据物种分类生成标签号后，在上面读取后，在这向量化
# # one_hot_train_labels = to_categorical(train_labels)
# y_train = to_categorical(train_labels)
# y_validation = to_categorical(validation_labels)
# # one_hot_test_labels = to_categorical(test_labels)

train_generator = generator(train_data, train_labels)
validation_generator = generator(validation_data, validation_labels)


# 一维卷积神经网络的架构与第 5 章的二维卷积神经网络相同，它是 SeparableConv1D 层和 MaxPooling1D
# 层的堆叠，最后是一个全局池化层或 Flatten 层，将三维输出转换为二维输出，让你可以向模
# 型中添加一个或多个 Dense 层，用于分类或回归。

# Sequential 模型
# model = models.Sequential()

# model.add(layers.SeparableConv1D(32, 5, activation='relu', input_shape=(max_length, token_index_len)))
# model.add(layers.MaxPooling1D(2))
# model.add(layers.SeparableConv1D(64, 5, activation='relu'))
# model.add(layers.MaxPooling1D(3))
# model.add(layers.SeparableConv1D(128, 5, activation='relu'))
# model.add(layers.MaxPooling1D(3))
# model.add(layers.SeparableConv1D(128, 5, activation='relu'))
# model.add(layers.GlobalMaxPooling1D())
# # model.add(layers.Flatten())
# model.add(layers.Dense(512, activation='relu'))
# model.add(layers.Dense(46, activation='softmax'))

# 函数式API
input_tensor = Input(shape=(max_length, token_index_len))
# 每个分支都有相同的步幅值strides(默认=(1, 1))，这对于保持所有分支输出具有相同的尺寸是很有必要的，这样你才能将它们连接在一起
branch_a1 = layers.SeparableConv1D(128, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(input_tensor)
branch_a1 = layers.BatchNormalization()(branch_a1)
branch_a1 = layers.SeparableConv1D(128, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a1)
branch_a1 = layers.BatchNormalization()(branch_a1)

branch_a2 = layers.SeparableConv1D(128, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a1)
branch_a2 = layers.BatchNormalization()(branch_a2)
branch_a2 = layers.SeparableConv1D(128, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a2)
branch_a2 = layers.MaxPooling1D(2)(branch_a2)
residual1 = layers.SeparableConv1D(128, 1, strides=2, padding='same')(branch_a1)
branch_a2 = layers.add([branch_a2, residual1])
branch_a2 = layers.BatchNormalization()(branch_a2)
branch_a2 = layers.SeparableConv1D(128, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a2)
branch_a2 = layers.BatchNormalization()(branch_a2)
branch_a2 = layers.SeparableConv1D(128, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a2)
branch_a2 = layers.BatchNormalization()(branch_a2)

branch_a3 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a2)
branch_a3 = layers.BatchNormalization()(branch_a3)
branch_a3 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a3 = layers.MaxPooling1D(2)(branch_a3)
residual2 = layers.SeparableConv1D(256, 1, strides=2, padding='same')(branch_a2)
branch_a3 = layers.add([branch_a3, residual2])
branch_a3 = layers.BatchNormalization()(branch_a3)
branch_a3 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a3 = layers.BatchNormalization()(branch_a3)
branch_a3 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a3 = layers.BatchNormalization()(branch_a3)

branch_a4 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a4 = layers.BatchNormalization()(branch_a4)
branch_a4 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a4)
branch_a4 = layers.MaxPooling1D(2)(branch_a4)
residual3 = layers.SeparableConv1D(256, 1, strides=2, padding='same')(branch_a3)
branch_a4 = layers.add([branch_a4, residual3])
branch_a4 = layers.BatchNormalization()(branch_a4)
branch_a4 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a4 = layers.BatchNormalization()(branch_a4)
branch_a4 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a4 = layers.BatchNormalization()(branch_a4)
branch_a4 = layers.SeparableConv1D(256, 3, activation='relu', padding='same', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_a3)
branch_a4 = layers.BatchNormalization()(branch_a4)

# branch_a = layers.Flatten()(branch_a)
branch_a4 = layers.GlobalMaxPooling1D()(branch_a4)

branch_b = layers.SeparableConv1D(256, 3, activation='relu', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(input_tensor)
branch_b = layers.GlobalMaxPooling1D()(branch_b)

branch_c = layers.SeparableConv1D(64, 3, activation='relu', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(input_tensor)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.BatchNormalization()(branch_c)
branch_c = layers.SeparableConv1D(128, 3, activation='relu', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_c)
branch_c = layers.MaxPooling1D(2)(branch_c)
branch_c = layers.BatchNormalization()(branch_c)
branch_c = layers.SeparableConv1D(256, 3, activation='relu', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_c)
branch_c = layers.GlobalMaxPooling1D()(branch_c)

branch_d = layers.SeparableConv1D(128, 3, activation='relu', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(input_tensor)
branch_d = layers.MaxPooling1D(2)(branch_d)
branch_d = layers.BatchNormalization()(branch_d)
branch_d = layers.SeparableConv1D(256, 3, activation='relu', depthwise_regularizer=regularizers.l1_l2(0.001), pointwise_regularizer=regularizers.l1_l2(0.001))(branch_d)
branch_d = layers.GlobalMaxPooling1D()(branch_d)

merged = layers.concatenate([branch_a4, branch_b, branch_c, branch_d], axis=-1)
merged = layers.Dense(512, activation='relu')(merged)
merged = layers.BatchNormalization()(merged)
output_tensor = layers.Dense(137, activation='softmax')(merged)

model = Model(input_tensor, output_tensor)

model.summary()

model.compile(optimizer=optimizers.Nadam(lr=1e-6), loss='categorical_crossentropy', metrics=['accuracy'])

callbacks_list = [ 
    keras.callbacks.EarlyStopping( # 如果不再改善，就中断训练
        monitor='accuracy', # 监控模型的验证精度
        patience=6, # 如果精度在多于2轮的时间（即3轮）内不再改善，中断训练
    ),
    keras.callbacks.ModelCheckpoint( # 在每轮过后保存当前权重
        filepath='virus_categorical_cnn_model.h5', # 目标模型文件的保存路径
        # 这两个参数的含义是，如果 val_loss 没有改善，那么不需要覆盖模型文件。这就可以始终保存在训练过程中见到的最佳模型
        monitor='val_loss',
        save_best_only=True,
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', # 监控模型的验证损失
        factor=0.5, # 触发时将学习率除以 2
        patience=4, # 如果验证损失在 10 轮内都没有改善，那么就触发这个回调函数
    )
]

# batch_size是每次梯度下降输入的数据数量，epochs是用整个train_data训练的轮数，具体解释ctrl点fit看参数
# history = model.fit(x_train, y_train, epochs=250, batch_size=128, validation_split=0.2)
# history = model.fit(x_train, y_train, epochs=200, batch_size=128, validation_data=(x_validation, y_validation))
history = model.fit_generator(train_generator, steps_per_epoch=ceil(109600/batch_size), epochs=1000, validation_data=validation_generator, validation_steps=ceil(27400/batch_size), callbacks=callbacks_list)

out_file = open('train_history.txt', 'w')
out_file.write(str(history.history))
out_file.close()
