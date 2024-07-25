import os, pilk
from pydub import AudioSegment


def convert_to_silk(media_path: str) -> str:
    """将输入的媒体文件转出为 silk, 并返回silk路径"""
    media = AudioSegment.from_file(media_path)
    pcm_path = os.path.basename(media_path)
    pcm_path = os.path.splitext(pcm_path)[0]
    silk_path = pcm_path + '.silk'
    pcm_path += '.pcm'
    media.export(pcm_path, 's16le', parameters=['-ar', str(media.frame_rate), '-ac', '1']).close()
    pilk.encode(pcm_path, silk_path, pcm_rate=media.frame_rate, tencent=True)
    return silk_path

def main():
    # 替换为你的媒体文件路径
    media_file_path = "./audio/input.mp3"

    silk_file_path = convert_to_silk(media_file_path)
    print(f"转换完成！生成的 Silk 文件路径为: {silk_file_path}")

if __name__ == "__main__":
    main()
