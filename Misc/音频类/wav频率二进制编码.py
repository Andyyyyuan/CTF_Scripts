import numpy as np
from scipy.io import wavfile

def get_frequency_every_04s(wav_file):
    sample_rate, audio_data = wavfile.read(wav_file)
    window_size = int(0.4 * sample_rate)  # 0.4秒窗口
    results = []
    
    for i in range(0, len(audio_data), window_size):
        if i + window_size > len(audio_data):
            break
            
        # 获取窗口数据
        window = audio_data[i:i+window_size]
        # 应用窗函数
        window = window * np.hanning(len(window))
        # FFT分析
        fft_result = np.abs(np.fft.fft(window))
        frequencies = np.fft.fftfreq(len(window), 1/sample_rate)
        # 取正频率部分
        positive_freq_mask = frequencies >= 0
        positive_freqs = frequencies[positive_freq_mask]
        positive_magnitude = fft_result[positive_freq_mask]
        # 找到主频（跳过直流分量）
        if len(positive_magnitude) > 10:
            # 找幅度最大的频率
            dominant_idx = np.argmax(positive_magnitude[5:]) + 5  # 跳过前几个低频分量
            dominant_freq = positive_freqs[dominant_idx]
            
            time_mid = (i + window_size/2) / sample_rate
            results.append((time_mid, dominant_freq))
    
    return results

if __name__ == "__main__":
    wav_file = "mystery_sound.wav"
    frequencies = get_frequency_every_04s(wav_file)
    res = ""

    print(f"分析文件: {wav_file}")
    print("时间(秒) | 频率(Hz)")
    print("-" * 30)

    for time, freq in frequencies:
        print(f"{time:7.2f} | {freq:8.1f}")
        if freq < 20:
            res += "0"
        elif freq > 20000:
            res += "1"

    print(res)