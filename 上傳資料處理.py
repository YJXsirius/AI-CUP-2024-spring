import os
import cv2
import shutil
import subprocess
from PIL import Image
import zipfile


#----------------------------------------------------------------------------------#
#獲取生成圖片
#----------------------------------------------------------------------------------#

#獲得河流圖片
command_1 = [
    'python', 'pytorch-CycleGAN-and-pix2pix-master/test.py', 
    '--dataroot', 'pytorch-CycleGAN-and-pix2pix-master/datasets/label_img', 
    '--name', 'ROAD_pix2pix_RI', 
    '--model', 'pix2pix', 
    '--direction', 'AtoB', 
    '--netG', 'resnet_12blocks', 
    '--checkpoints_dir', 'checkpoints',
]
subprocess.run(command_1)
#獲得道路圖片
command_2 = [
    'python', 'pytorch-CycleGAN-and-pix2pix-master/test.py', 
    '--dataroot', 'pytorch-CycleGAN-and-pix2pix-master/datasets/label_img', 
    '--name', 'ROAD_pix2pix_RO', 
    '--model', 'pix2pix', 
    '--direction', 'AtoB', 
    '--netG', 'resnet_9blocks', 
    '--netD', 'n_layers', 
    '--n_layers_D', '6',
    '--checkpoints_dir', 'checkpoints',
]
subprocess.run(command_2)


#----------------------------------------------------------------------------------#
#提取生成圖片並合併
#----------------------------------------------------------------------------------#
def convert_and_delete(start_dir, target_dir, keyword1, keyword2):
    for filename in os.listdir(start_dir):
        # 檢查文件名是否符合條件，包含 keyword1 或 keyword2
        if (keyword1 in filename or keyword2 in filename) and '_fake_B' in filename and filename.endswith('.png'):
            new_name = filename.replace('_fake_B', '').replace('.png', '.jpg')
            start_file_path = os.path.join(start_dir, filename)
            target_file_path = os.path.join(target_dir, new_name)

            # 讀取圖像
            img = cv2.imread(start_file_path)

            # 如果目標文件夾不存在，則創建它
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # 保存圖像為 JPG 格式
            cv2.imwrite(target_file_path, img)

            # 刪除原始 PNG 文件
            #os.remove(start_file_path)

            print(f"Processed: {filename} -> {new_name}")
keyword_RI1 = "PUB_RI"
keyword_RI2 = "PRI_RI"
keyword_RO1 = "PUB_RO" 
keyword_RO2 = "PRI_RO"
if not os.path.exists('results/images'):
    os.makedirs('results/images')
convert_and_delete('results/ROAD_pix2pix_RI/test_latest/images', 'results/images',keyword_RI1,keyword_RI2)
convert_and_delete('results/ROAD_pix2pix_RO/test_latest/images', 'results/images',keyword_RO1,keyword_RO2)

#----------------------------------------------------------------------------------#
#改變圖片大小
#----------------------------------------------------------------------------------#
target_width = 428
target_height = 240
start_dir = 'results/images'
for filename in os.listdir(start_dir):
    # 检查文件是否为.jpg格式
    if filename.endswith('.jpg'):
        start_file_path = os.path.join(start_dir, filename)
        target_file_path = os.path.join(start_dir, filename)
        # 使用PIL库读取图片
        img = Image.open(start_file_path)
        # 改变图片大小
        resized_img = img.resize((target_width, target_height))
        # 保存更改大小后的图片
        resized_img.save(target_file_path)
        print(f"Processed: {filename} -> {filename}")




#----------------------------------------------------------------------------------#
#製造zip上傳檔案
#----------------------------------------------------------------------------------#
def zip_images(directory, zip_filename):
    # 创建一个ZipFile对象
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    
    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 只压缩.jpg和.png文件
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # 获取文件的全路径
                full_path = os.path.join(root, filename)
                # 将文件添加到zip，只保留文件名，不包含路径
                zipf.write(full_path, arcname=filename)

    # 关闭ZipFile对象
    zipf.close()
    print(f"Finished zipping {zip_filename}")
zip_images('results/images', '00001.zip')
