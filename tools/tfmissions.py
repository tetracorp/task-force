# Task Force mission file reader
# A quick Python script I wrote to extract maps from Task Force

import struct, random
import numpy as np
from PIL import Image, ImageDraw, ImageColor, ImageFont, ImageOps

colcodes = [0,8,15,8,15,11,11,8,15,0,17,18,18,17,17,1,1,1,1,1,1,1,17,17,17,17,6,6,6,6,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,19,19,9,9,9,9,6,2,2,2,2,2,6]
palette = "#000","#ABB","#F22","#812","#F81","#951","#EE0","#880","#0E2","#081","#17F","#149","#B4E","#739","#041","#641","#455","#899","#CDD","#FFF","#F77","#7BF","#677","#CA8","#526","#511","#136","#A86","#ECA","#567","#9AB","#DEF"
palette_list = [ ImageColor.getcolor(x, "RGB") for x in palette ]
sprite_file = Image.open("taskforce_sprites.png")
tiles = [ sprite_file.crop((0,n,16,n+16)) for n in range(0,73*16,16) ]

for n in range(1,9):
#for n in range(1,2):
  print(f"\n### Mission {n}")
  filename = f"TFSource/Mission{n}"
  with open (filename, "rb") as f:
    coords = f.read(40)
    text = f.read(360).decode("ascii").replace("\0","\n")
    maps = f.read(3600)
    grid = struct.unpack("3600b",maps)

  coords = struct.unpack('>20h', coords)
  coord_list = [(coords[n], coords[n+1]) for n in range(0,20,2)]

  print(f"```\n{text}\n```")
  print ("Target coordinates:")
  for c in coord_list:
    if not (c[0]==0 and c[1]==0):
      print(c)
# -21267 = aced

  print(f"![Mission {n}](../images/Mission{n}_map.png)"+"{:center}"+f"<br>Mission {n}")

  img = Image.new("RGB",(960,960),(0,0,0))
  draw = ImageDraw.Draw(img)
  enemy_no = -1
  blocks = [0]*76
  for y in range(0, 60):
    for x in range(0, 60):
      tile = grid[y*60+x]
      blocks[tile]+= 1
      if tile>66: # enemies
        enemy_no += 1
      img.paste(tiles[tile],(x*16,y*16))

      for goal in coord_list[1:]:
        if x and y and x==goal[0] and y==goal[1] and coord_list[0][0] < 0:
          print(coord_list[0][0])
          draw.rectangle((x*16, y*16, x*16+15, y*16+15), outline=(255,255,0), width=2)
        elif (goal[0] == enemy_no or goal[1] == enemy_no) and tile>66 and enemy_no!=0:
          draw.rectangle((x*16, y*16, x*16+15, y*16+15), outline=(255,255,0), width=2)
          
      if tile==1 or tile==2: # mines
        img.paste(tiles[tile+2],(x*16,y*16))
        draw.rectangle((x*16, y*16, x*16+15, y*16+15), outline=(255,0,255), width=2)

  print(f"=Mission {n}")
  print("=Enemies:")
  for n in [(67,"Normal"),(68,"Big Gun"),(69,"Elite"),(70,"Android"),(71,"Captain")]:
    print(f"=- {n[1]}: {blocks[n[0]]}")
  print(f"=- Total: {sum(blocks[67:72])}")

#      colcode = colcodes[tile]
#      color = palette[colcode]
#      color = ImageColor.getcolor(color, "RGB")
#
#      for goal in coord_list:
#        if x and y and x==goal[0] and y==goal[1]:
#          color = (255,0,255)
#      
#      if not tile in [5,6,7,8,10,16,26,27,28,29,62,63,64,66,65,49]:
#        draw.text((x*10, y*10), f"{tile:02}", align="center")
#  img.save(f"Mission{n}_map.png")
