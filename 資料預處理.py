import os
from PIL import Image,ImageOps
import shutil
import zipfile

#----------------------------------------------------------------------------------#
#解壓縮AI-CUP-2024-spring\datasets下圖片
#----------------------------------------------------------------------------------#
def unzip_files_in_folder(folder_path):
    # 通過os.listdir獲取文件夾下所有的文件名稱
    files = os.listdir(folder_path)
    # 遍歷文件夾下的每一個文件
    for file in files:
        # 如果這個文件是.zip壓縮格式
        if file.endswith('.zip'):
            # 獲取文件的全路徑
            file_path = os.path.join(folder_path, file)
            # 創建ZipFile對象並使用extractall方法解壓
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
folder_path = 'datasets'
unzip_files_in_folder(folder_path)
print('完成解壓縮AI-CUP-2024-spring\datasets下圖片')

#----------------------------------------------------------------------------------#
#合併舉辦方提供的訓練原始圖片與線路圖
#----------------------------------------------------------------------------------#
img_folder_path = "datasets/Training dataset/img"
label_img_folder_path = "datasets/Training dataset/label_img"
folder_path = 'datasets/ALL'

img_files = os.listdir(img_folder_path)
label_img_files = os.listdir(label_img_folder_path)
# 確認兩個目錄下的圖片名稱一一對應
assert set(i.split('.')[0] for i in img_files) == set(i.split('.')[0] for i in label_img_files)

# 遍历所有圖片
for img_file in img_files:
    # 找到對應的 label_img
    label_img_file = img_file.split('.')[0] + '.png'
    
    # 打开这两张圖片
    img_path = os.path.join(img_folder_path, img_file)
    img = Image.open(img_path)

    label_img_path = os.path.join(label_img_folder_path, label_img_file)
    label_img = Image.open(label_img_path)
    
    # 確認圖片大小
    width, height = max(img.size[0], label_img.size[0]), max(img.size[1], label_img.size[1])
    new_img = Image.new('RGB', (2 * width, height))
    
    # 反轉label_img的黑白
    inverted_label_img = ImageOps.invert(label_img.convert('L'))

    # 将这两张圖片左右拼接为一张圖片
    new_img.paste(inverted_label_img, (0, 0))
    new_img.paste(img, (width, 0))
    
    # 保存圖片至指定路徑，文件格式为.jpg
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    new_img_path = os.path.join(folder_path, img_file)
    new_img.save(new_img_path)
print('完成合併舉辦方提供的訓練原始圖片與線路圖')

#----------------------------------------------------------------------------------#
#分開河流与道路訓練圖片
#----------------------------------------------------------------------------------#
def extract_specific_images(src_folder, dst_folder, keyword):
    # 獲取源文件夾下所有文件名
    file_list = os.listdir(src_folder)

    for file_name in file_list:
        # 如果文件名包含 keyword 且為 .jpg 格式，則复制到目标文件夾
        if keyword in file_name and file_name.endswith(".jpg"):
            # 完整的源文件路徑
            src_file_path = os.path.join(src_folder, file_name)
            # 完整的目标文件路徑
            dst_file_path = os.path.join(dst_folder, file_name)
            # 如果目标文件夹不存在，则创建它
            if not os.path.exists(os.path.join(dst_folder)):
                os.makedirs(os.path.join(dst_folder))
            # 移動文件
            shutil.move(src_file_path, dst_file_path)

src_folder = "datasets/ALL" 

# 提取的關鍵字
keyword1 = "TRA_RI"
keyword2 = "TRA_RO"

# 目標文件夾
dst_folder_RI = "pytorch-CycleGAN-and-pix2pix-master/datasets/ROAD_pix2pix_RI/train"
dst_folder_RO = "pytorch-CycleGAN-and-pix2pix-master/datasets/ROAD_pix2pix_RO/train"

# 在兩個源文件夾中分別提取符合關鍵詞的圖片
extract_specific_images(src_folder, dst_folder_RI, keyword1)
extract_specific_images(src_folder, dst_folder_RO, keyword2)
if os.path.exists(src_folder):
    shutil.rmtree(src_folder)
print('完成分開河流与道路訓練圖片')

#----------------------------------------------------------------------------------#
#合併擴充道路訓練圖片（程式自帶訓練集）
#----------------------------------------------------------------------------------#
dst_folder_RO = "pytorch-CycleGAN-and-pix2pix-master/datasets/ROAD_pix2pix_RO/train"
folder1 = 'datasets/ROAD_pix2pix/test'
folder2 = 'datasets/ROAD_pix2pix/train'

def copy_images(src_folder, dst_folder):
    # 獲取源文件夾下所有文件名
    file_list = os.listdir(src_folder)

    for file_name in file_list:
        # 如果文件為 .jpg 格式，則複製到目標文件夾
        if file_name.endswith(".jpg"):
            # 完整的源文件路徑
            src_file_path = os.path.join(src_folder, file_name)
            # 完整的目標文件路徑
            dst_file_path = os.path.join(dst_folder, file_name)
            # 如果目標文件夾不存在，則創建它
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)
            # 複製文件
            shutil.copy(src_file_path, dst_file_path)
# 移動兩個源文件夾的所有.jpg圖片到目標文件夾
copy_images(folder1, dst_folder_RO)
copy_images(folder2, dst_folder_RO)
print('完成合併擴充道路訓練圖片（程式自帶訓練集）')


#----------------------------------------------------------------------------------#
#驗證圖片處理
#----------------------------------------------------------------------------------#
label_img_folder_path = "datasets/label_img"
folder_path ='pytorch-CycleGAN-and-pix2pix-master/datasets/label_img/test'

label_img_files = os.listdir(label_img_folder_path)
for img_file in label_img_files:
    label_img_file = img_file.split('.')[0] + '.png'
    label_img_path = os.path.join(label_img_folder_path, label_img_file)
    label_img = Image.open(label_img_path)
    width, height = label_img.size[0], label_img.size[1]
    new_img = Image.new('RGB', (2 * width, height))
    # 反轉label_img的黑白
    inverted_label_img = ImageOps.invert(label_img.convert('L'))
    # 将这两张圖片左右拼接为一张圖片
    new_img.paste(inverted_label_img, (0, 0))
    new_img.paste(inverted_label_img, (width, 0))
    # 保存圖片至指定路徑，文件格式为.jpg
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    new_img_path = os.path.join(folder_path, img_file)
    new_img.save(new_img_path)
print('完成驗證圖片處理')
print('資料預處理完成')

