"""
    @Author: Patrick Peters
    @Date: 04.02.2025
    @Main: Ziel dieses Skipts ist es den Ablauf des OTC und die anderen Prozessschritte gebündelt und übersichtlich darzustellen.
    @Version: 1.0
"""
from tqdm import tqdm
import os
import subprocess
import rename as rn

# Get the path from the environment variable
config_path = os.getenv("OT_PATH") # Abfrage nicht notwendig, da CMD bereits abfragt

def main():
    # Hauptablaufplan
    # target, isRename, isRescale, isDetect, isTrack, newTarget, isTest = rn.abfragen()
    types = ['yolo11m', 'yolov8s', 'yolov8m', 'yolo11s']
    tests = [(0.25, 0.45), (0.1, 0.6), (0.75, 0.2)]
    target = []
    path = config_path+r"\TestVideo"
    for root, dirs, files in os.walk(path):
        for name in files:
            target.append(os.path.join(root, name))

# Vorlauf % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
    for t in tqdm(types, position=0):
        for i in tqdm(tests, position=1): 
            # OTC % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
            for target_file in tqdm(target,position=2):
                duration = round(rn.get_video_len_ffprobe(target_file))
            
            # Detect V_11 % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
                command = f'python detect.py -p "{target_file}" --expected_duration "{duration}" -w {t}.pt --conf {i[0]} --iou {i[1]} '
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")

            # Track % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
                old, file_extension = os.path.splitext(target_file)
                command = f'python track.py -p "{old}.otdet"'
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")

            # rename.otdet/.ottrk
                new = target_file+f"_{t}-{i[0]}-{i[1]}"

                # try: 
                os.rename(old+".otdet", new+".otdet") 
                os.rename(old+".ottrk", new+".ottrk")
                # except Exception as e:
                    # print(f"Ein Fehler (File) ist aufgetreten: {e}")

                # print(old, new, duration)

    subprocess.run(f'msg * "Py-Programm abgeschlossen."', text=True)
        
if __name__ == "__main__":
    main()