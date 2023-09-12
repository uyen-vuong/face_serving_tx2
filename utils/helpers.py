import os 
import signal
import shutil
LOG_PATH = "./logs/pid"
LOG_FILE = "./logs"
import torch 
import cv2 

def kill_all_old_process():

    for item in os.listdir(LOG_FILE):
        if item.endswith(".log"):
            os.remove(os.path.join(LOG_FILE, item))

    if not os.path.exists(LOG_PATH):
        print("Not exist old process")
        return 
    for filename in os.listdir(LOG_PATH):
        file_path = os.path.join(LOG_PATH, filename)
        try:
            f = open(file_path, "r")
            pid = int(f.readline())
            os.kill(pid, signal.SIGKILL)
            print("Finish remove process: ", pid)
        except Exception as e:
            print(e)

def save_pid_is_running(list_proc):
    print(list_proc)
    try:
        shutil.rmtree(LOG_PATH) 
    except:
        pass 
    try:
        os.makedirs(LOG_PATH)
    except:
        pass
    for i, proc in enumerate(list_proc):
        with open(os.path.join(LOG_PATH, f"proc_{i}.txt"), 'w') as f:
            f.write(f"{list_proc[i].pid}")

dict_emotion = {0:'neutral', 1:'happiness', 2:'surprise', 3:'sadness', 4: 'anger', 5: 'disgust', 6: 'fear', 7: 'contempt'}
dict_color = {0:(255, 255, 255), 
              1:(0, 255, 255), 
              2:(255, 200, 0), 
              3:(255, 128, 0), 
              4: (0, 0, 255), 
              5: (255, 0, 150), 
              6: (0, 255, 0), 
              7: (116, 185, 252)}


def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [0, 0, 0], thickness=tf, lineType=cv2.LINE_AA)

def check_keys(model, pretrained_state_dict):
    ckpt_keys = set(pretrained_state_dict.keys())
    model_keys = set(model.state_dict().keys())
    used_pretrained_keys = model_keys & ckpt_keys
    unused_pretrained_keys = ckpt_keys - model_keys
    missing_keys = model_keys - ckpt_keys
    print('Missing keys:{}'.format(len(missing_keys)))
    print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
    print('Used keys:{}'.format(len(used_pretrained_keys)))
    assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
    return True


def remove_prefix(state_dict, prefix):
    ''' Old style model is stored with all names of parameters sharing common prefix 'module.' '''
    print('remove prefix \'{}\''.format(prefix))
    f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
    return {f(key): value for key, value in state_dict.items()}


def load_model(model, pretrained_path, load_to_cpu):
    print('Loading pretrained model from {}'.format(pretrained_path))
    if load_to_cpu:
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
    else:
        device = torch.cuda.current_device()
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage.cuda(device))
    if "state_dict" in pretrained_dict.keys():
        pretrained_dict = remove_prefix(pretrained_dict['state_dict'], 'module.')
    else:
        pretrained_dict = remove_prefix(pretrained_dict, 'module.')
    check_keys(model, pretrained_dict)
    model.load_state_dict(pretrained_dict, strict=False)
    return model