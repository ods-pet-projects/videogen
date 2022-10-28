import re
import random

def similar_frames_to_query(similar_frames, max_interval_len=10):
    video_to_seconds = {}
    for frame_filename in similar_frames:
        frame_video_name = re.search('(\w.*)_\d+\.jpg', frame_filename).group(1)
        frame_second = int(re.search('\w.*_(\d+)\.jpg', frame_filename).group(1))
        if frame_video_name in video_to_seconds:
            video_to_seconds[frame_video_name].append(frame_second)
        else:
            video_to_seconds[frame_video_name] = [frame_second]
    video_to_intervals = {frame_video_name:[] for frame_video_name in video_to_seconds}
    for frame_video_name in video_to_seconds:
        video_to_seconds[frame_video_name] = sorted(video_to_seconds[frame_video_name])
        
        creating_new_interval = False
        start_interval = max(0, video_to_seconds[frame_video_name][0] - 2)
        end_interval = random.randint(start_interval+1, start_interval + max_interval_len)
        for second in video_to_seconds[frame_video_name]:
            if second - start_interval > max_interval_len:
                end_interval = random.randint(end_interval, start_interval+max_interval_len)
                video_to_intervals[frame_video_name].append(tuple((start_interval, end_interval)))
                start_interval = max(0, second - 2)
                end_interval = second + 1
            else:                
                if end_interval < second:
                    end_interval = second
                end_interval = random.randint(start_interval+1, start_interval + max_interval_len)
        end_interval = random.randint(end_interval, start_interval+max_interval_len)
        video_to_intervals[frame_video_name].append(tuple((start_interval, end_interval)))
            
    queries_list = []
    for v in video_to_intervals:
        for interval in video_to_intervals[v]:
            queries_list.append(
                f"{v}[{interval[0]}:{interval[1]}].v"
            )
    random.shuffle(queries_list)
    return " + ".join(queries_list)
