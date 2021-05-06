from os import pipe
from pathlib import Path
import subprocess, time,re



        
# countdown timer
def time_countdown(timer):
    while timer != 0:
        print('等待' + str(timer), end='\r')
        time.sleep(1)
        timer -= 1


# initial stage - create needed folders
print('初始化中')
needed_files = ['result.log', 'channel.text', '']
needed_folders = ['data', 'channel', 'source_files']
folder_path = Path(__file__)

number = -1
for needed_folder in needed_folders:
    folder_check = Path(__file__).parents[0].joinpath(f'{needed_folder}')
    if not folder_check.exists():
        folder_check.mkdir()
        number += 1
    folder_check.joinpath(needed_files[number]).touch(exist_ok=True)

channel_txt_path = Path(__file__).parent.joinpath('channel','channel.txt')
source_files_path = Path(__file__).parent.joinpath('source_files')
result_log = folder_path.parent.joinpath('data','result.log')

print('初始化结束')


# instructions
def input_figure(choice):
    if choice == 1:
        single_file_path = input('输入需要查看包的绝对地址 ')
        raw_info = subprocess.run(['java', '-jar', 'walle-cli-all.jar', 'show', single_file_path],capture_output=True)
        # print(str(raw_info))
        patten = '(?<=\{channel=).*(?=})'
        patten2= re.compile(patten)
        channel_info = patten2.findall(str(raw_info))[0]
        print(f'''
======================================
| 渠道名称:{channel_info}
======================================
''')
        with open(result_log,'a') as f:
            f.write(f'\n{str(raw_info)}')
            
        raise ValueError
    elif choice == 2:
        single_file_path = input('输入包的绝对地址 ')
        ex_channel = input('请输入市场名称')
        subprocess.run(['java', '-jar', 'walle-cli-all.jar', 'put', '-c', ex_channel, single_file_path])
        print('更改中')
    # 测试文件是否
        for i in Path(single_file_path).parent.glob(f'*_{ex_channel}.*'):
            raw_info = subprocess.run(['java', '-jar', 'walle-cli-all.jar', 'show', i],capture_output=True)
            patten = '(?<=\{channel=).*(?=})'
            patten2= re.compile(patten)
            channel_info = patten2.findall(str(raw_info))[0]
            # print(i.stat().st_mtime_ns) todo
            print(f'''
======================================
| 添加完成
======================================
| 源文件      ：{single_file_path}
| 市场来源    :{channel_info}
| 生成文件地址 ：{i} 
| 
======================================
''')
        with open(result_log,'a') as f:
            f.write(f'\n{raw_info})')
        raise ValueError
    elif choice == 3:
        Path(__file__).parent.joinpath('output_files').mkdir(exist_ok=True)
        output_file_path = Path(__file__).parent.joinpath('output_files')

        with open(channel_txt_path,'rb') as files:
            file_count = 0
            lines = []
            for line in files:
                lines.append(line)
            for i in source_files_path.glob('*.apk'):
                for line in lines:
                    cc = subprocess.run(['java','-jar','walle-cli-all.jar','batch','-f ',channel_txt_path,i,output_file_path],check=True,capture_output=True,text=True)
                    file_count +=1
                    print(f'已完成：{file_count}')
                    with open(result_log,'a') as f:
                        f.write(f'\n{cc}')
        print(f'查看 {output_file_path} 验证生成文件')
    elif choice == 4:
        print('拜拜')
        time_countdown(1)
        raise exit()
    else:
        print('你的输入有问题')
        raise ValueError


for files in Path.iterdir(Path(__file__).parent):
    while True:
        try:
            user_choose = input_figure(int(input(
                '''
===============================================================
| ------------v0.1--------------------------------------------
|
| 
| 
| 请选择功能
| 1. 查看指定包内容
| 2. 为特定包，写入渠道名称
| 3. 使用channel的信息内容为source_folder里的包打包
| 4. 退出                                                     
===============================================================
>>>'''
            )))
            # print(user_choose)
        except ValueError:
            print('请重新选择')
            time_countdown(2)



