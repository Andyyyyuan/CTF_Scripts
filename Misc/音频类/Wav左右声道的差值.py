import scipy.io.wavfile as wavfile

sample_rate, data = wavfile.read("1.wav") # 读取音频文件的采样率和数据
# print(sample_rate, data)
# 创建两个列表来存储左右两声道的数据
left = []
right = []

for item in data:
    # 第一列的数据是左声道，第二列是右声道
    left.append(item[0])
    right.append(item[1])

diff = [str(left-right) for left, right in zip(left, right)]
res = ''
for item in diff:
    if item == '2':
        res += '1'
    elif item == '1':
        res += '0'
    else:
        continue
with open('res.txt', 'w') as f:
    f.write(res)