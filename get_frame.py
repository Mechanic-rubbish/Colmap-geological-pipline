import cv2
import os

# 视频文件路径
video_path = 'mountain\dji_fly_20240625_113931_0_1719308360045_video_cache.mp4'
# 保存帧的目录
output_dir = 'mountain\input'

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print(f"Error: Cannot open video file {video_path}")
else:
    print(f"Successfully opened video file {video_path}")

frame_count = 0
saved_frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Reached the end of the video or cannot fetch the frame.")
        break
    
    # 只保存编号为n的倍数的帧
    if frame_count % 20 == 0:
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
        success = cv2.imwrite(frame_filename, frame)
        
        if success:
            saved_frame_count += 1
            print(f"Saved frame {frame_count} to {frame_filename}")
        else:
            print(f"Failed to save frame {frame_count}")
    
    frame_count += 1

cap.release()
print(f"Total frames saved: {saved_frame_count}")
