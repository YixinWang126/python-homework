from pathlib import Path
from functions import *
import json
import matplotlib.pyplot as plt

#读取分行
path = Path('Modified_Data.txt')
contents = path.read_text()
lines = contents.splitlines()

list=[]

#将提取的信息赋值给列表
for line in lines:
    list.append(extract_data_from_line(line))

print(list[-1],list[0])
#A处理时间列表
Alist = []
#B处理时间列表
Blist = []
#总列表
final_list = []


for index, i in enumerate(list):
    if 'Astart' in i.keys():
        for a in list[index:]:
            if i['id'] == a['id'] and 'Aend' in a.keys():
                dic = {'id':i['id'], 'Atime':a['Aend']-i['Astart']}
                Alist.append(dic)
                final_list.append(dic)
    if 'Bstart' in i.keys():
        for b in list[index:]:
            if i['id'] == b['id'] and 'Bend' in b.keys():
                dic = {'id':i['id'], 'Btime':b['Bend']-i['Bstart']}
                Blist.append(dic)
                final_list.append(dic)


#计算ProcessA,B平均耗时
print(f'ProcessA的平均耗时为{calculate_average_time(Alist)}')
print(f'ProcessB的平均耗时为{calculate_average_time(Blist)}')

#给列表排序
sortedA = sorted(Alist, key=lambda item: item['Atime'])
sortedB = sorted(Blist, key=lambda item: item['Btime'])

#求P90及P99
ka = len(Alist)
ka99 = int(0.99 * ka)
ka90 = int(0.90 * ka)
kb = len(Blist)
kb99 = int(0.99 * kb)
kb90 = int(0.90 * kb)
m = sortedA[ka99]['Atime']
n = sortedA[ka90]['Atime']
x = sortedB[kb99]['Btime']
y = sortedB[kb90]['Btime']
print(f' ProcessA的P99耗时为:{m},P90耗时为{n}')
print(f' ProcessB的P99耗时为:{x},P90耗时为{y}')

#计算吞吐量
time = (list[-1]['Bend']-list[0]['Astart'])/1000 #second
count = 0
#构建两个列表存放A和B的id
id_A = []
id_B = []
for i in Alist:
    if i['id'] not in id_A:
        id_A.append(i['id'])
for i in Blist:
    if i['id'] not in id_B:
        id_B.append(i['id'])

id_list = []
for i in list:
    if i['id'] not in id_list:
        if i['id'] in id_A and i['id'] in id_B:
            id_list.append(i['id'])
            count += 1
p = count/time
print(f'系统平均吞吐量为{count/time}')

sum = 0
count = 0
for i in list:
    for j in list:
        if i['id'] == j['id'] and 'Astart' in i.keys() and 'Bend' in j.keys():
            sum += j['Bend'] - i['Astart']
            count += 1
average_time = sum/count
print(f'平均帧延迟为{sum/count}')


processA = []
processB = []

for entry in list:
    id = int(entry['id'])
    for key, value in entry.items():
        if key == 'Astart':
            processA.append((id, value, 'start'))
        elif key == 'Aend':
            processA.append((id, value, 'end'))
        elif key == 'Bstart':
            processB.append((id, value, 'start'))
        elif key == 'Bend':
            processB.append((id, value, 'end'))

# 对数据进行排序
processA.sort(key=lambda x: x[1])
processB.sort(key=lambda x: x[1])

# 定义绘图函数
def plot_timeline(process_data, label, ax, linewidth=2):
    prev_time = None
    for i, (id, time, action) in enumerate(process_data):
        if action == 'start':
            ax.plot([time, time], [id - 0.4, id + 0.4], label=label if i == 0 else "", color='C0' if label == 'ProcessA' else 'C1', linewidth=linewidth)
        elif action == 'end':
            ax.plot([time, time], [id - 0.4, id + 0.4], label=label if i == 0 else "", color='C0' if label == 'ProcessA' else 'C1', linewidth=linewidth)
            ax.plot([prev_time, time], [id, id], color='C0' if label == 'ProcessA' else 'C1', linewidth=linewidth)
        prev_time = time

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 ProcessA 和 ProcessB 的时序图
plot_timeline(processA, 'ProcessA', ax)
plot_timeline(processB, 'ProcessB', ax)

# 设置 x 轴格式
ax.set_xlabel('Time (timestamp)')
ax.set_ylabel('Process ID')
ax.set_title('Process Scheduling Timeline')
ax.legend()

# 显示图形
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#保存结果
result1 = {'ProcessA的平均耗时':calculate_average_time(Alist),
           'ProcessB的平均耗时':calculate_average_time(Blist),
           'ProcessA的P99耗时':m,
           'ProcessA的P90耗时':n,
           'ProcessB的P99耗时':x,
           'ProcessB的P99耗时':y
}
result2 = {'系统平均吞吐量':p}
result3 = {'平均帧延迟':average_time}
result = [result1, result2, result3]
result = json.dumps(result, indent=2)
result_path = Path('result.json')
result_path.write_text(result)