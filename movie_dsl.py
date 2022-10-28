import re
import moviepy.editor as mp


class MovClass:
    def __init__(self, clip_obj, path_params, common_fps=24, width=640, height=360, need_resize=True):
        self.common_fps = common_fps
        self.path_params = path_params
        obj_params = self.get_expr_parts(clip_obj)
        self.name, self.slice, self.dtype, self.cmd = obj_params
        self.start_sec, self.end_sec = self.parse_slice(self.slice)
        self.clip = None
        self.width = width
        self.height = height
        self.need_resize = need_resize

    @staticmethod
    def get_expr_parts(expr):
        pat = r'([a-zA-Z-_]+)(?:(\[[0-9:]+\]))?(?:\.([avi]?))?(?:\.(.*)$)?'
        return re.findall(pat, expr)[0]

    @staticmethod
    def parse_volume_cmd(expr):
        pat = 'volume\((.*)\)'
        groups = re.findall(pat, expr)
        if groups:
            print(groups[0])
            return float(groups[0])


    @staticmethod
    def parse_resize_cmd(expr):
        pat = 'resize\((\d+) *, *(\d+)\)'
        groups = re.findall(pat, expr)[0]
        if groups:
            print('parse resize', groups)
            return float(groups[0]), float(groups[1])

    def __str__(self):
        return ' '.join((self.name, self.slice, self.dtype, self.cmd))

    def parse_slice(self, slice):
        if slice:
            return [int(x) for x in slice.replace('[', '').replace(']', '').split(':')]
        else:
            return None, None

    def load(self):
        print('name:', self.name)
        ifile_path = self.path_params[self.name]
        if self.dtype == 'v':
            self.clip = mp.VideoFileClip(ifile_path, audio=False)
            self.clip.set_fps(self.common_fps)
            if self.need_resize:
                if self.cmd and self.cmd.startswith('resize'):
                    width, height = self.parse_resize_cmd(self.cmd)
                    self.clip = self.clip.resize(newsize=(width, height))
                else:
                    self.clip = self.clip.resize(newsize=(self.width, self.height))
        elif self.dtype == 'a':
            self.clip = mp.AudioFileClip(ifile_path)
            self.clip.set_fps(self.common_fps)
            if self.cmd:
                new_volume = self.parse_volume_cmd(self.cmd)
                if new_volume:
                    print('applied volume', new_volume)
                    self.clip = self.clip.volumex(new_volume)
                else:
                    print('not supported cmd for audio', self.cmd)
        elif self.dtype == 'i':
            self.clip = mp.ImageClip(ifile_path)
                # .set_pos(("right", "top"))
                # .margin(right=8, top=8, opacity=0) \
            if self.end_sec != self.start_sec:
                self.clip = self.clip.set_duration(self.end_sec - self.start_sec)
        elif self.dtype == '':
            self.clip = mp.VideoFileClip(ifile_path, audio=True)
            self.clip.set_fps(self.common_fps)
        else:
            print('unknown type', self.dtype)

        if self.dtype != 'i' and self.start_sec != self.end_sec:
            self.clip = self.clip.subclip(self.start_sec, self.end_sec)
        return self


class MovDSL:
    def __init__(self, params):
        self.params = params

    def query(self, query):
        query = ''.join(query.split())
        self.clips = []
        for clip_expr in query.split('+'):
            clip_parts = {}
            for clip_obj in self.get_objs(clip_expr):
                clip_part = MovClass(clip_obj, self.params).load()
                if clip_part.dtype in clip_parts:
                    raise Exception(f'Key exists {clip_part.dtype}')
                clip_parts[clip_part.dtype] = clip_part.clip
            self.clips.append(self.merge_parts(clip_parts))
        return self

    def save(self, ofile_path):
        final_clip = mp.concatenate_videoclips(self.clips, method='compose')
        final_clip.write_videofile(ofile_path,
                                   codec='libx264',
                                   audio_codec='aac',
                                   temp_audiofile='temp-audio.m4a',
                                   remove_temp=True,
                                   fps=24)
        return self

    def get_objs(self, clip_expr):
        return clip_expr.split('*')

    def merge_parts(self, clip_parts):
        if 'v' in clip_parts:
            clip = clip_parts['v']
        elif '' in clip_parts:
            clip = clip_parts['']
        if 'i' in clip_parts and 'v' in clip_parts:
            if not clip_parts['i'].duration:
                clip_parts['i'].set_duration(clip.duration)
            clip = mp.CompositeVideoClip([clip, clip_parts['i']])
        if 'i' in clip_parts and 'v' not in clip_parts:
            clip = clip_parts['i']
        if 'a' in clip_parts:
            clip = clip.set_audio(clip_parts['a'])
        return clip


def main():
    params = {
        'gbu': 'data/init_hb/хороший плохой злой.mp4',
        'gbu_a': 'data/init_hb/хороший плохой злой dasha cover.mp4',
        'bb': 'data/init_hb/breakin bad say my name.mp4',
        'bb_a': 'data/init_hb/breaking bad cover.mp4',
        'ww': 'data/init_hb/ww trailer 2 season.mp4',
        'ww_a': 'data/init_hb/ww music.mp4',
        'wh': 'data/init_hb/wh trailer.mp4',
        'wch': 'data/init_hb/witcher wild hunt.mp4',
        'hb': 'data/init_hb/hb dasha main 640.mp4',
        'hb_i': 'data/init_hb/hb eug.png',
    }

    query = '''
            gbu[230: 252].v * gbu_a[0: 22].a +
            bb[33: 43].v * bb_a[3: 13].a +
            ww[43: 50].v * ww_a[75: 82].a +
            wh[158: 173].v * wch[15: 30].a +
            hb[3: 21].v * hb[3: 21].a * hb_i[0:18].i + hb_i[0:10].i
    '''

    dsl = MovDSL(params) \
        .query(query) \
        .save('data/output/dsl_example.mp4')


if __name__ == '__main__':
    main()
