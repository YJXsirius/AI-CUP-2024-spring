克隆github程式:
    github網址：https://github.com/YJXsirius/AI-CUP-2024-spring.git


安裝環境:
    1. 安裝[Anaconda]:（https://www.anaconda.com/download）
    2. 进入主目錄下:D:
                   cd D:\AI-CUP-2024-spring
    3. 創建虛擬環境:conda create -n AI-CUP-2024-spring python=3.10
    4. 進入虛擬環境:conda activate AI-CUP-2024-spring
    5. 安裝Pytorch :pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116
    6. 安裝github基本套件:pip install -r requirements.txt


下載訓練與驗證資料:（請分別下載並且直接移動到AI-CUP-2024-spring/datasets下）
    Google雲端硬碟網址：https://drive.google.com/drive/folders/1MRxT6C3Ub8FMBtniSotfoHlMUbsXdvWu?usp=sharing


資料處理:(運行以下程式將完成資料處理)
    1.資料預處理.py


開始訓練:
    1.河流:python pytorch-CycleGAN-and-pix2pix-master/train.py --dataroot ./pytorch-CycleGAN-and-pix2pix-master/datasets/ROAD_pix2pix_RI --name ROAD_pix2pix_RI --model pix2pix --direction AtoB --netG resnet_12blocks
    2.道路:python pytorch-CycleGAN-and-pix2pix-master/train.py --dataroot ./pytorch-CycleGAN-and-pix2pix-master/datasets/ROAD_pix2pix_RO --name ROAD_pix2pix_RO --model pix2pix --direction AtoB --netG resnet_9blocks --netD n_layers --n_layers_D 6


上傳資料處理:(運行以下程式將在主目錄生成zip上傳檔案)
    1.上傳資料處理.py










*-----------------------------------------------------------------------------------------------------------------------------------*
比賽最終訓練權重：
    Google雲端硬碟網址：https://drive.google.com/drive/folders/1TGF4QNO0dQ_MQgGqblX3NNQfwpPL7hJg?usp=sharing
