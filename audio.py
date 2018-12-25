import numpy as np
from pydub import AudioSegment
from pydub.utils import mediainfo


class Audio:
    def __init__(self, **kwargs):
        self.channels_count = None
        self.data = None
        self.sample_width = None
        self.frame_rate = None
        self.channels = None
        # self.bit_rate = None
        if 'file_path' in kwargs.keys():
            file_path = kwargs['file_path']
            self.get_segment_info(file_path)
            # self.get_bit_rate_from_file(file_path)
        else:
            self.channels_count = kwargs['channels_count']
            self.sample_width = kwargs['sample_width']
            self.frame_rate = kwargs['frame_rate']
            self.channels = kwargs['channels']
            self.unite_channels()
            # self.bit_rate = None

    def unite_channels(self):
        self.data = np.dstack(self.channels).flatten()

    def get_segment_info(self, file_path):
        segment = AudioSegment.from_file(file_path, format='mp4')
        samples = segment.get_array_of_samples()
        self.data = np.array(samples)
        self.sample_width = segment.sample_width
        self.channels_count = segment.channels
        self.frame_rate = segment.frame_rate
        self.get_channels()

    def get_channels(self):
        self.channels = []
        for i in range(self.channels_count):
            samples_for_current_channel = self.data[i::self.channels_count]
            self.channels.append(samples_for_current_channel)

    # def get_bit_rate_from_file(self, file_path):
    #     self.bit_rate = mediainfo(file_path)['bit_rate']
