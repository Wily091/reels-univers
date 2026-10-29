import sys
from PIL import Image
ps=sys.argv[2:]; ims=[Image.open(p) for p in ps]
w=max(i.width for i in ims); h=sum(i.height for i in ims)
c=Image.new('RGB',(w,h)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height
c.thumbnail((1300,8000)); c.save(sys.argv[1],quality=70)
