from pathlib import Path

path = Path('trace_analysis.log')
#载入日志并分行存储
log_data = path.read_text()
lines = log_data.splitlines()

#保留有用内容
lines_copy = lines[:]
for line in lines_copy:
    if 'static_multistream' not in line:
        lines.remove(line)
        print(f'"{line}" removed')

#转换为字符串
text = ''
for line in lines:
    print(line)
    text += f'{line}\n'
#写入
path = Path('Modified_Data.txt')
path.write_text(text)