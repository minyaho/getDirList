# 參考網頁 https://www.gushiciku.cn/pl/2LwL/zh-tw
# by HoRan
import os
import pathlib
from pathlib import Path

# Part 1: 獲取當前目錄
#print('***獲取當前目錄***')
#print(__file__)                                     # 當前檔案路徑
#print(os.getcwd())                                  # 當前的工作目錄
#print(os.path.abspath(os.path.dirname(__file__)))   # 方法1： 利用os，獲取當前檔案所放置的資料夾
#print(pathlib.Path(__file__).parent.absolute())     # 方法2： 利用pathlib，獲取當前檔案所放置的資料夾

# 補充
# abspath() 函式可以得到所需檔案的路徑，dirname() 函式從完整路徑中得到目錄。
#print('***獲取上級目錄***')
#print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
#print(os.path.abspath(os.path.dirname(os.getcwd())))
#print(os.path.abspath(os.path.join(os.getcwd(), "..")))
#print(os.path.abspath(os.path.join(os.getcwd(), "../.."))) # 上上級

# part 2: 列出當下目錄文件
print("!*請輸入資料夾位置(空白則視為當前工作資料夾):")
dir_path = input()
if dir_path == "":
    dir_path = os.getcwd()              # 指定要查詢的路徑

# 方法一: 利用 os.listdir()
#allFileList = os.listdir(dir_path)  # 列出指定路徑底下所有檔案(包含資料夾)
#for file in allFileList:            # 逐一查詢檔案清單
#   這邊也可以視情況，做檔案的操作(複製、讀取...等)
#   使用isdir檢查是否為目錄
#   使用isfile判斷是否為檔案
#   使用join的方式把路徑與檔案名稱串起來(等同filePath+fileName) ex: os.path.isdir(os.path.join(yourPath,file))
#    print(file)

# 方法2: 利用os.walk()
# 與listdir不同的是，listdir只是將指定路徑底下的目錄和檔案列出來
# walk的方式則會將指定路徑底下所有的目錄與檔案都列出來(包含子目錄以及子目錄底下的檔案)
#allList = os.walk(dir_path)
# 列出所有子目錄與子目錄底下所有的檔案
#for root, dirs, files in allList:
#   列出目前讀取到的路徑
#    print("path：", root)
#   列出在這個路徑下讀取到的資料夾(第一層讀完才會讀第二層)
#    print("directory：", dirs)
#   列出在這個路徑下讀取到的所有檔案
#    print("file：", files)

# 由於方法1、2皆無法直接列出檔案資訊，因此需要進行讀檔後解析
# 可參考此網站 https://www.learncodewithmike.com/2020/02/python-files.html

# 方法3: 利用os.scandir() (PS:在Python 3.5 中被引用，其文件為 PEP 471 。)
# with os.scandir(dir_path) as entries:
#     for entry in entries:
#         print(entry.name)

# 方法4: 使用 pathlib 模組
# entries = pathlib.Path(dir_path)
# for entry in entries.iterdir():
#     print(entry.name)
#     print(entry.absolute())

# 總結比較:
# 函式 	描述
# os.listdir() 	以列表的方式返回目錄中所有的檔案和資料夾
# os.scandir() 	返回一個迭代器包含目錄中所有的物件，物件包含檔案屬性資訊
# pathlib.Path().iterdir() 	返回一個迭代器包含目錄中所有的物件，物件包含檔案屬性資訊

# 在此利用方法4繼續
dir_list = list()   # 放置資料夾的entry list
file_list = list()  # 放置檔案的entry list
entries = Path(dir_path)

print("!*是否選擇排序方式(數字以外預設0)?")
print("(依據名稱:0, 依據修改時間:1, 依據建立時間:2, 依據檔案大小:3, 依照檔案類型:4)")
sort_type = input()
print(sort_type)
if sort_type == '1':
    entries = sorted(entries.iterdir(),key = lambda s: s.stat().st_mtime)
elif sort_type == '2':
    entries = sorted(entries.iterdir(),key = lambda s: s.stat().st_ctime)
elif sort_type == '3':
    entries = sorted(entries.iterdir(),key = lambda s: s.stat().st_size)
elif sort_type == '4':
    entries = sorted(entries.iterdir(),key = lambda s: s.suffix[1:])
else:
    entries = sorted(entries.iterdir(),key = lambda s: s.name)

for entry in entries:     # 分類資料夾與檔案
    if entry.is_file():
        file_list.append(entry)
    if entry.is_dir():
        dir_list.append(entry)

print("**資料夾內清單**")
print('文件:')
for i,dir in enumerate(dir_list,0):
    print(i,': ',dir.name)
print('--------------------------')
print('檔案:')
for i,file in enumerate(file_list,0):
    print(i,': ',file.name)

print("\n!*是否建立json(Y/N,預設N)*!")
if input() == 'Y':
    # 建立json，紀錄檔案資訊
    import json
    create_json_state = False
    try:
        print("\n**開始建立json**")
        json_list = list()
        for i,file in enumerate(entries):
            json_list.append(
                {
                "name": file.name,
                "type": file.suffix[1:],
                "size": file.stat().st_size,
                "atime": file.stat().st_atime,
                "mtime": file.stat().st_mtime,
                "ctime": file.stat().st_ctime,
                "path": str(file.absolute()),
                })
        data = json.dumps(json_list)
        #print(os.path.split(dir_path)[-1])
        json_file = Path(os.path.split(dir_path)[-1]+"_content.json")
        json_file.write_text(data)
        create_json_state = True
        print("**建立json成功**")
        print("**檔案位置: "+str(json_file.absolute())+" **")

    except:
        print("!*建立json失敗*!")

print("\n!*是否建立csv(Y/N,預設N)*!")
if input() == 'Y':
    import csv
    with open(os.path.split(dir_path)[-1]+"_content.csv", "w", newline='') as file:
        fieldnames = ["name", "type", "size","atime","mtime","ctime","path"]    # 定義欄位
        writer = csv.DictWriter(file, fieldnames=fieldnames)                    # 將 dictionary 寫入 CSV 檔
        writer.writeheader()                                                    # 寫入第一列的欄位名稱
        for file in entries:
            writer.writerow(
                {
                "name": file.name,
                "type": file.suffix[1:],
                "size": file.stat().st_size,
                "atime": file.stat().st_atime,
                "mtime": file.stat().st_mtime,
                "ctime": file.stat().st_ctime,
                "path": str(file.absolute()),
                })


    print('BYE')