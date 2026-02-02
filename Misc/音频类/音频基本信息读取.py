import wave
def get_info():
    with wave.open("flag.wav",'rb') as wf:
        n_channels = wf.getnchannels()
        samplewidth_bytes = wf.getsampwidth()
        bits_per_sample = samplewidth_bytes * 8
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        duration = n_frames / framerate
    print(f"通道数: {n_channels}")
    print(f"每个采样的字节数: {samplewidth_bytes}")
    print(f"每个采样的位数: {bits_per_sample}")
    print(f"采样率: {framerate}")
    print(f"总帧数: {n_frames}")
    print(f"时长(秒): {duration}")