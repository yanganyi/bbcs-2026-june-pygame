import os,numpy as np
from multiprocessing import Pool
from moviepy import VideoFileClip
from PIL import Image,ImageDraw,ImageFont,ImageFilter

def font(s):
 p=["/System/Library/Fonts/Supplemental/Arial Black.ttf"]
 return ImageFont.truetype(next(x for x in p if os.path.exists(x)),s)

def overlay(w,h,txt):
 im=Image.new("RGBA",(w,h),(0,0,0,0));s=int(h*.33);f=font(s);d=ImageDraw.Draw(im)
 while d.textbbox((0,0),txt,font=f)[2]>w*.92:s-=8;f=font(s)
 sh=Image.new("RGBA",(w,h),(0,0,0,0));ImageDraw.Draw(sh).text((w//2+18,h//2+18),txt,font=f,anchor="mm",fill=(0,0,0,190),stroke_width=26,stroke_fill=(0,0,0,190))
 im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
 d.text((w//2,h//2),txt,font=f,anchor="mm",fill="white",stroke_width=12,stroke_fill=(20,20,20,255))
 return im

def process(d):
 v=VideoFileClip("assets/fih.mp4").subclipped(0,d).with_fps(24);w,h=v.size
 def gf(g,t):
  a=g(t).copy();r=max(0,d-int(t));o=overlay(w,h,f"{r//60}:{r%60:02d}");m=np.array(o.split()[-1])[:,:,None]/255;rgb=np.array(o.convert("RGB"));a[:]=(a*(1-m)+rgb*m).astype(np.uint8);return a
 c=v.transform(gf);c.write_videofile(f"assets/fih_{d if d<60 else d//60}{'sec' if d<60 else 'min'}.mp4",codec="libx264",audio_codec="aac",threads=1,preset="ultrafast",logger=None);v.close();c.close()

if __name__=="__main__":
 with Pool(6) as p:p.map(process,[5])