import numpy as np
import moviepy.editor as mpy
from pydub import AudioSegment
import cv2
import os

from audio import Audio
from frames import Frames
from image import Image

dirName = os.path.dirname(os.path.abspath(__file__))
tempDir = os.path.join(dirName, "temp")


class VideoEditor:
    def __init__(self, file_path):
        self.silence = np.zeros(80000000, int)
        self.image_idx = -1
        self.video_idx = 0
        self.video_names = []
        self.image_names = []
        self.audio_list = []
        self.frames_list = []
        self.images_list = []
        self.audio_list.append(Audio(file_path=file_path))
        self.frames_list.append(Frames(file_path=file_path))
        self.video_names.append('original')

    def __cut_audio(self, beg_in_sec, end_in_sec, idx):
        audio = self.audio_list[idx]
        beg = round(beg_in_sec * int(audio.frame_rate))
        end = round(end_in_sec * int(audio.frame_rate))
        new_channels = []
        for channel in audio.channels:
            new_channels.append(channel[beg:end])
        self.audio_list.append(
            Audio(frame_rate=audio.frame_rate, channels=new_channels, channels_count=audio.channels_count,
                  sample_width=audio.sample_width))
        return len(self.audio_list) - 1

    def __cut_frames(self, beg_in_sec, end_in_sec, idx):
        frames = self.frames_list[idx]
        beg = round(beg_in_sec * frames.fps)
        end = round(end_in_sec * frames.fps)
        self.frames_list.append(Frames(data=frames.data[beg:end], fps=frames.fps))
        return len(self.frames_list) - 1

    def cut_fragment(self, beg, end, idx=None):
        if idx is None:
            idx = self.video_idx
        self.__cut_frames(beg, end, idx)
        res_idx = self.__cut_audio(beg, end, idx)
        self.video_names.append('{}| cut {}-{}'.format(self.video_names[idx], beg, end))
        return res_idx

    def __concat_frames(self, idx_1, idx_2):
        frames1 = self.frames_list[idx_1]
        frames2 = self.frames_list[idx_2]
        self.frames_list.append(Frames(data=np.concatenate([frames1.data, frames2.data]), fps=frames1.fps))
        return len(self.frames_list) - 1

    def __concat_audio(self, idx_1, idx_2):
        audio1 = self.audio_list[idx_1]
        audio2 = self.audio_list[idx_2]
        new_channels = []
        for i in range(0, audio1.channels_count):
            # new_channels.append(np.array([audio1.channels[0], audio2.channels[0]]).flatten())
            new_channels.append(np.concatenate((audio1.channels[i], audio2.channels[i])))
        self.audio_list.append(Audio(frame_rate=audio1.frame_rate, sample_width=audio1.sample_width,
                                     channels_count=audio1.channels_count, channels=new_channels))
        return len(self.audio_list) - 1

    def concat_fragments(self, idx_1, idx_2=None):
        if idx_2 is None:
            idx_2 = idx_1
            idx_1 = self.video_idx
        self.__concat_audio(idx_1, idx_2)
        self.video_names.append('{}| concat {}'.format(self.video_names[idx_1], self.video_names[idx_2]))
        return self.__concat_frames(idx_1, idx_2)

    def connect_image(self, sec, video_idx=None, image_idx=None):
        if video_idx is None:
            video_idx = self.video_idx
        if image_idx is None:
            image_idx = self.image_idx
        self.__add_silence(sec)
        self.video_names.append('{} | add image {}'.format(self.video_names[video_idx], self.image_names[image_idx]))
        return self.__connect_image_with_frames(sec)

    def __add_silence(self, sec,  idx=None):
        if idx is None:
            idx = self.video_idx
        audio = self.audio_list[idx]
        fr_count = round(int(audio.frame_rate)*sec)
        silence = np.zeros(fr_count, int)
        new_channels = []
        for i in range(audio.channels_count):
            new_channels.append(np.concatenate((audio.channels[i], silence)))
        self.audio_list.append(Audio(frame_rate=audio.frame_rate*audio.sample_width, sample_width=audio.sample_width,
                                     channels_count=audio.channels_count, channels=new_channels))
        return len(self.audio_list) - 1

    def __connect_image_with_frames(self, sec, idx=None, image_idx=None):
        if idx is None:
            idx = self.video_idx
        if image_idx is None:
            image_idx = self.image_idx
        frames = self.frames_list[idx]
        image = self.images_list[image_idx]
        fr_count = round(frames.fps*sec)
        resized = cv2.resize(image.data, (frames.data[0].shape[1], frames.data[0].shape[0]))
        new_data = np.empty(fr_count, dtype=np.ndarray)
        for i in range(fr_count):
            new_data[i] = resized
        self.frames_list.append(Frames(data=np.concatenate((frames.data, new_data)), fps=frames.fps))
        return len(self.frames_list) - 1

    def add_image(self, file_path):
        self.images_list.append(Image(file_path))
        self.image_names.append(os.path.basename(file_path))
        return len(self.images_list) - 1

    def save_result(self, file_path, idx=None):
        if idx is None:
            idx = self.video_idx
        if not file_path.endswith('.mp4'):
            file_path += '.mp4'
        audio = self.audio_list[idx]
        frames = self.frames_list[idx]
        height, width, channels = frames.data[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_path = os.path.join(tempDir, '{}.mp4'.format(idx))
        out = cv2.VideoWriter(video_path, fourcc, frames.fps, (width, height))
        for frame in frames.data:
            out.write(frame)

        # Release everything if job is finished
        out.release()
        cv2.destroyAllWindows()
        audio_path = os.path.join(tempDir, '{}.mp3'.format(idx))
        AudioSegment(
            audio.data.tobytes(),
            sample_width=audio.sample_width,
            frame_rate=audio.frame_rate,
            channels=audio.channels_count
        ).export(audio_path, format='mp3')

        my_clip = mpy.VideoFileClip(video_path)
        audio_background = mpy.AudioFileClip(audio_path)
        # final_audio = mpy.CompositeAudioClip([my_clip.audio, audio_background])
        final_clip = my_clip.set_audio(audio_background)
        final_clip.write_videofile(file_path)
        os.remove(audio_path)
        os.remove(video_path)

    def change_selected_video(self, idx):
        if 0 <= idx < len(self.audio_list):
            self.video_idx = idx
        else:
            raise ValueError

    def change_selected_image(self, idx):
        if 0 <= idx < len(self.images_list):
            self.image_idx = idx
        else:
            raise ValueError

    def get_video_length(self):
        return len(self.video_names)

    def get_image_length(self):
        return len(self.image_names)

    def get_fragment_duration(self, idx=None):
        if idx is None:
            idx = self.video_idx
        return len(self.frames_list[idx].data)//self.frames_list[idx].fps
