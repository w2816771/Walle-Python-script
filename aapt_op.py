import subprocess,platform,re,pathlib
os = platform.system()
print(f'你的系统为 {os}')

apk_location = pathlib.Path(input("填入要分析的APK的路径"))
content = subprocess.run('./aapt' + ' dump badging ' + str(apk_location), capture_output=True)
nameplate_list = ['package: ','VersionCode: ','VersionName: ','MinsdkVersion: ','targetSDKversion: ']
check_list = ["name='","versionCode='","versionName='","nsdkVersion:'","ntargetSdkVersion:'"]
figure_list=[]
for check_name in check_list:
    patten_string = fr'(?<={check_name}).*?(?=\')' ## 查找到相关的字符
    pattens = re.compile(patten_string,flags=re.M) 
    package_name = pattens.findall(str(content))[0]
    figure_list.append(package_name)

print(f'''
===================================================
|            Package  :  {figure_list[0]}
|        VersionCode  :  {figure_list[1]}
|        VersionName  :  {figure_list[2]}
|      MinSdkVersion  :  {figure_list[3]}
|   targetSDKversion  :  {figure_list[4]}
==================================================
'''
)


