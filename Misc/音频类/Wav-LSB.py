import wave
import libnum

def extract_lsb(wav_file):
    res = ""
    with wave.open(wav_file, 'rb') as wf:
        sample_width = wf.getsampwidth() # # 获取每个采样的字节数
        n_frames = wf.getnframes()
        frame_data = wf.readframes(n_frames)  # 读取2000个采样点需要的字节
        # print(type(frame_data)) # <class 'bytes'>
        
        if sample_width == 2:  # 16位采样，每2个字节组成一个采样点
            for i in range(0, n_frames, 2):
                # 将数据从小端序转换为大端序，因为WAV文件使用小端序存储数据
                sample = frame_data[i] | (frame_data[i+1] << 8)
                res += str(sample & 1)
        else:  # 8位采样
            for i in range(min(len(frame_data), 1000)):
                res += str(frame_data[i] & 1)
                
    print("[+] 二进制字符串长度:", len(res))
    print("[+] 提取出的 LSB 信息:", libnum.b2s(res)[:100])
    #  7avpassword:NO996!