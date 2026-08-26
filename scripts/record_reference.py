from __future__ import annotations

import argparse
from pathlib import Path

import sounddevice as sd
import soundfile as sf


def main():
    parser = argparse.ArgumentParser(description='Record a VoxCPM voice reference WAV')
    parser.add_argument('--seconds', type=int, default=8)
    parser.add_argument('--output', default='voice_reference.wav')
    args = parser.parse_args()
    rate = 16000
    print(f'开始录音 {args.seconds} 秒，请自然说话……', flush=True)
    audio = sd.rec(args.seconds * rate, samplerate=rate, channels=1, dtype='float32')
    sd.wait()
    output = Path(args.output).resolve()
    sf.write(output, audio, rate, subtype='PCM_16')
    print(f'已保存：{output}', flush=True)


if __name__ == '__main__':
    main()
