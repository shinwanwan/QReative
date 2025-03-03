from PIL import Image, ImageDraw, ImageFont

# ★ • ♬ ● ▲ ☀ ♣ ♦ ♥ ♠ ☯ ◆ ◉ ◒ ◎ ◐ ◑ ◓ Ⅹ ※ ▼ ♫ ▶ 預設"●"

font = ImageFont.truetype("FreeMono.ttf", 50)#引入字型文件

def delete_background(img, remain_color):#去背改成除了要留的全改成透明的"""
    temp = []
    for item in img.getdata():
        if item[:3] != remain_color:#這裡"""
            temp.append((255, 255, 255, 0))
        else:
            temp.append(item)
    
    img.putdata(temp)
    
    return img

def check_idiot(dot_color, background_color):#多的function，前後景一樣把dot顏色[0]減50"""
    temp = []
    for i in range(3):
            temp.append(dot_color[i])

    if dot_color == background_color and dot_color[0] >= 50:
        dot_color = (temp[0]-50,temp[1],temp[2])
    elif dot_color == background_color:
        dot_color = ((temp[0]+50)%255,temp[1],temp[2])
    
    return dot_color

#這裡多一個參數dot_type"""
def creat_dot_background(dot_color, background_color, qr_size, dot_type = "●"):#生成背景點陣
    img = Image.new("RGBA", (qr_size, qr_size), background_color)
    draw = ImageDraw.Draw(img)  
    times = int(qr_size/40)
    
    dot_color = check_idiot(dot_color, background_color)#確認顏色不一樣"""
    
    for i in range(times):#version 3的qr code+兩格邊界共37格
        for j in range(times):
            draw.text((i*40+5, j*40-5), dot_type, font = font, fill = dot_color)
            
    img.save("data/bb.png")
    return img        


    

#這裡多一個參數dot_type"""
def dot(qr_img, dot_color, background_color, frame_color, dot_type = "●"):
    qr_img = qr_img.get_image().convert("RGBA")#轉成RGBA 來做去背       
    dot_img = creat_dot_background(dot_color, background_color, qr_img.size[0], dot_type)#產生背景點陣圖
                                                                             #這裡多一個參數dot_type"""
    #QR_frame.get_qr_frame(qr_version, bg_color = 160, level = 'M', mask = 1, quiet_zone_len = 4, img_size = 40, timing_pattern = False, version_inform = False, format_inform = False, quiet_zone = False)
    
    qr_frame = Image.open("data/qr_frame.png")
    qr_frame = qr_frame.convert("RGBA")
    #print(qr_img)
    """改成除黑塊外去掉"""
    qr_img = delete_background(qr_img, (0,0,0))#qrcode背景預設是白色
    
    
    
    temp = []
    for item in qr_img.getdata():#黑塊調成背景顏色"""
        if item[:3] == (0,0,0):
            temp.append(background_color)#之後要調顏色可能需要建立色碼表 這裡只能放tuple
        else:
            temp.append(item)
    
    qr_img.putdata(temp)
    
    dot_img.paste(qr_img, None, qr_img)#圖片疊合
    dot_img.save("data/test.png")
    
    qr_frame = delete_background(qr_frame, (0,0,0))#frame去背成剩黑色"""
    
    temp.clear()
    for item in qr_frame.getdata():#黑塊調成背景顏色"""
        if item[:3] == (0,0,0):
            temp.append(frame_color)#之後要調顏色可能需要建立色碼表 這裡只能放tuple
        else:
            temp.append(item)
    
    qr_frame.putdata(temp)
    
    
    qr_frame.save("data/frame.png")#這裡"""
    dot_img.paste(qr_frame, (40,40), qr_frame)#圖片疊合
    dot_img.save("data/dot.png")
    
def dot_2(qr_img, dot_color, background_color):
    qr_img = qr_img.get_image().convert("RGBA")#轉成RGBA 來做去背
    dot_img = creat_dot_background(dot_color, background_color, qr_img.size[0])#產生背景點陣圖
    
    temp = []
    
    for item in qr_img.getdata():#去背: 遇到白色轉成透明的
        if item[:3] == (0, 0, 0):
            temp.append((0,0,0,0))
        else:
            temp.append(item)
    
    qr_img.putdata(temp)
    
    dot_img.paste(qr_img, None, qr_img)#圖片疊合
    dot_img.save('data/dot2.png')
    temp.clear()
    
    
#多參數"""
def add_background_picture(back_img, dot_img, qr_frame, dot_color, background_color):
    back_img.convert("RGBA")
    dot_img.convert("RGBA")
    dot_color = check_idiot(dot_color, background_color)#這裡好像沒必要 以防萬一"""
    temp = []
    for item in dot_img.getdata():#點以外的去掉"""
        if item[:3] != dot_color:
            temp.append((255, 255, 255, 0))
        else:
            temp.append(item)
    
    dot_img.putdata(temp)    

    back_img.paste(dot_img, None, dot_img)
    back_img.paste(qr_frame, (40,40), qr_frame)#重貼一個frame"""
    back_img.save("data/dot_pic.png")
    