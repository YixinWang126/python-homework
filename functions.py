import re

def extract_data_from_line(line):
    # 使用正则表达式匹配 frame_id 和 ProcessA:start 等值
    frame_id_pattern = re.compile(r'frame_id:(\d+)')
    process_Astart_pattern = re.compile(r'ProcessA:start:(\d+)')
    process_Aend_pattern = re.compile(r'ProcessA:end:(\d+)')
    process_Bstart_pattern = re.compile(r'ProcessB:start:(\d+)')
    process_Bend_pattern = re.compile(r'ProcessB:end:(\d+)')
    
    frame_id_match = frame_id_pattern.search(line)
    process_Astart_match = process_Astart_pattern.search(line)
    process_Aend_match = process_Aend_pattern.search(line)
    process_Bstart_match = process_Bstart_pattern.search(line)
    process_Bend_match = process_Bend_pattern.search(line)
    
    if frame_id_match:
        if process_Astart_match:
            #返回一个包含相关信息的字典
            a = {'id':frame_id_match.group(1), 'Astart':int(process_Astart_match.group(1))}
            return a
        elif process_Aend_match:
            a = {'id':frame_id_match.group(1), 'Aend':int(process_Aend_match.group(1))}
            return a
        elif process_Bstart_match:
            a = {'id':frame_id_match.group(1), 'Bstart':int(process_Bstart_match.group(1))}
            return a
        elif process_Bend_match:
            a = {'id':frame_id_match.group(1), 'Bend':int(process_Bend_match.group(1))}
            return a

#计算工序平均用时
def calculate_average_time(list):
    sum = 0
    for dic in list:
        for name in dic.keys():
            if 'time' in name:
                sum += dic[name]
    
    t = sum/len(list)
    return t
