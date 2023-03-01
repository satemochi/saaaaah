from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.crop import crop


input_path = "IMG_0165.mp4"
output_path = "IMG_0165.gif"

start = '00:00:03.3'
end = '00:00:08'

clip = VideoFileClip(input_path).subclip(start, end)
clip = crop(clip, x_center=clip.w*0.5, y_center=clip.h*0.5,
            width=clip.w, height=clip.h*0.75)

clip = clip.resize(width=300)

txtclip = TextClip(txt='2022.6.30', color='white', font='Amiri-Bold',
                   kerning=5, fontsize=16, method='label').set_duration(3)
clip = CompositeVideoClip([clip, txtclip])

clip.write_gif(output_path, fps=10)
clip.close()
