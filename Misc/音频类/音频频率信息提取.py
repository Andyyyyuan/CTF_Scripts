import numpy as np
from scipy.io import wavfile
 
def extract_binary_from_wav(file_path, threshold_freq, output_path):
    sample_rate, data = wavfile.read(file_path)
    
    if len(data.shape) > 1:
        data = data[:, 0]
    
    window_size = int(sample_rate * 0.01)  # 10ms窗口
    binary_data = []
 
    for i in range(0, len(data), window_size):
        window = data[i:i + window_size]
        if len(window) < window_size:
            break
 
        fft_result = np.fft.fft(window)
        freqs = np.fft.fftfreq(len(window), d=1/sample_rate)
        
        magnitude = np.abs(fft_result)
        
        max_index = np.argmax(magnitude[:len(magnitude)//2])
        dominant_freq = freqs[max_index]
 
        binary_value = 1 if dominant_freq >= threshold_freq else 0
        binary_data.append(binary_value)
 
    with open(output_path, "w") as f:
        binary_string = "".join(map(str, binary_data))
        f.write(binary_string)
    print(f"提取的二进制数据已保存到 {output_path}")
 
file_path = "attachment.wav"
output_path = "output.txt"
threshold_freq = 500  # 设定高低频的分界点
extract_binary_from_wav(file_path, threshold_freq, output_path)