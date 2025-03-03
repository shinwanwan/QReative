from PIL import Image, ImageFont
import cv2
import qrcode
import QR_frame as QR
import dot




font = ImageFont.truetype("FreeMono.ttf", 150)#引入字型文件





""" PIL圖片疊合,去背換色等函式"""

def matting_inverse(src,dst):

    image = Image.open(src)
    image = image.convert("RGBA")
    #print(image)
    temp = []
    for item in image.getdata():
        if item[:3] == (255, 255, 255):
            temp.append((255, 255, 255, 0))
        else:
            temp.append(item[:3])

    image.putdata(temp)

    image.save(dst)

def clipping_mask(src,mask,dst):

    image = Image.open(src)##qr
    mask_img = Image.open(mask)##2base1
    image = image.convert("RGBA")
    mask_img = mask_img.convert("RGBA")
    #print(image)

    qrlst = list(image.getdata())
    temp = []
    seq = 0

    for item in mask_img.getdata():
        if item[:3] == (0,0,0):
            temp.append(qrlst[seq])
        else:
            temp.append((255,255,255,0))
        seq = seq + 1

    image.putdata(temp)

    image.save(dst)


def image_paste(src,src2,dst):
    image = Image.open(src)
    image2 = Image.open(src2)
    image = image.convert("RGBA")

    image2.paste(image,None,image)
    image2.save(dst)





"""SizePicker"""

def getImageSize(src):
    sp = src.shape
    height = sp[0]
    width = sp[1]
    return height,width

def imageQR_Resize(src,ver,box,qr):
    height,width = getImageSize(src)
    qr_h,qr_w = getImageSize(qr)
    
    if height != qr_h or width != qr_w and height == width:
        #print('Wrong Size,Now resize into ',qr_h)
        src = cv2.resize(src,(qr_h,qr_w),interpolation=cv2.INTER_AREA)
        height,width = getImageSize(src)
   
    elif height != width:
        pass
        #print('Wrong input')

    #print(" ",height," ",width)

    return height,width,src


"""ps圖層混合"""
##色彩增值
def ps_Multiply(src0,src1,alpha):
    dst = src0 / 255 * src1 / 255 * alpha
    return dst

##濾色
def ps_Screen(src0,src1,alpha):
    dst = 1 - (1 - src0 / 255)  * (1 - src1 / 255) * alpha
    return dst

##透明度調整 EX:value = 0.8 -> (80%不透明度)
def ps_Opacity(src0,src1,val):
    dst = (src0 / 255 * val) + ( src1 / 255 * (1 - val) )
    return dst



def write_image(path, img):
    # img = img*(2**16-1)
    # img = img.astype(np.uint16)
    # img = img.astype(np.uint8)

    img = cv2.convertScaleAbs(img, alpha=(255.0))
    cv2.imwrite(path, img)

"""mosaic"""

def do_mosaic(frame, x, y, w, h, neighbor):
  """
  
  :param frame: opencv frame
  :param int x : 左頂點
  :param int y: 右頂點
  :param int w: width
  :param int h: height
  :param int neighbor: each box_size_width
  """
  fh, fw = frame.shape[0], frame.shape[1]
  if (y + h > fh) or (x + w > fw):
    return
  for i in range(0, h - neighbor, neighbor): 
    for j in range(0, w - neighbor, neighbor):
      rect = [j + x, i + y, neighbor, neighbor]
      color = frame[i + y][j + x].tolist() 
      left_up = (rect[0], rect[1])
      right_down = (rect[0] + neighbor - 1, rect[1] + neighbor - 1)
      cv2.rectangle(frame, left_up, right_down, color, -1)




""" 1st methon"""
def QRArt_firstPack(in_ver,insrc,qrsrc,qr_frame,multiply_value,screen_value,opacity_value):

    #print('1st method')

    height,width,insrc = imageQR_Resize(insrc,in_ver,10,qrsrc)

    ##base_h,base_w = getImageSize(qrsrc)

    wbg_temp = Image.new("RGBA", (height, width), "#FFFFFF")

    wbg_temp.save('data\wbg.png')




    wbg = cv2.imread('data/wbg.png')
    qr_frame = cv2.imread('data/qr_frame.png')


    base0 = ps_Multiply(insrc,insrc,multiply_value)

    write_image('data/base0.jpg',base0);


    base1 = cv2.imread('data/base0.jpg')

    base1 = ps_Multiply(insrc,base1,multiply_value)

    write_image('data/base1.jpg',base1)


    base2 = cv2.imread('data/base1.jpg')

    base2 = ps_Screen(qrsrc,base2,screen_value)


    write_image('data/base2.jpg',base2)


    base2 = cv2.imread('data/base2.jpg')

    base3 = ps_Opacity(insrc,wbg,opacity_value)

    write_image('data/base3.jpg',base3)



    base3 = cv2.imread('data/base3.jpg')

    base4 = ps_Multiply(base3,base2,multiply_value)

    write_image('data/base4.jpg',base4)


    base5 = cv2.imread('data/base4.jpg')

    base5 = ps_Multiply(base5,qr_frame,1.0)

    write_image('data/1_color_final.png',base5)
    
    
    wbg_new = Image.new("RGBA", (int(height*1.2), int(width*1.2)), "#FFFFFF")

    

    final_img = Image.open("data/1_color_final.png")

    wbg_new.paste(final_img,(int(height*0.1),int(width*0.1)))

    wbg_new.save('data/1_color_final.png')




"""2nd method"""
def QRArt_secondPack(in_ver,insrc,qrsrc,qr_frame,threshold_value,mosaic_value):

    #print('2nd method')

    height,width,insrc = imageQR_Resize(insrc,in_ver,10,qrsrc)
    
    qr_frame = cv2.imread('data/qr_frame.png')


    base0 = cv2.cvtColor(insrc,cv2.COLOR_BGR2GRAY)

    ret,base1 = cv2.threshold(base0, threshold_value, 255, cv2.THRESH_BINARY)

    

    do_mosaic(base1, 0, 0, height, width ,mosaic_value)


    ##cv2.imshow('base1',base1)

    write_image('data/2base1.jpg',base1)

    clipping_mask('data/qr.jpg','data/2base1.jpg','data/2base_cube.png')
    clipping_mask('data/2dot_opacity.png', 'data/2base1.jpg' , 'data/2base_dot.png')

    image_paste('data/2base_cube.png','data/2dot_opacity.png', 'data/2base_dot_cube_noframe.png')##外點內格
    image_paste('data/2base_dot.png', 'data/qr.jpg', 'data/2base_cube_dot_noframe.png') ##外格內點


    ##外點內格
    base3 = cv2.imread('data/2base_dot_cube_noframe.png')

    base3 = ps_Multiply(qr_frame,base3,1.0)

    write_image('data/2_dot_cube_final.png',base3)

    ##外格內點
    base3 = cv2.imread('data/2base_cube_dot_noframe.png')

    base3 = ps_Multiply(qr_frame,base3,1.0)

    write_image('data/2_cube_dot_final.png',base3)
    
    
    wbg_new = Image.new("RGBA", (int(height*1.2), int(width*1.2)), "#FFFFFF")


    final_dot = Image.open("data/2_dot_cube_final.png")
    final_cube = Image.open("data/2_cube_dot_final.png")

    wbg_new.paste(final_dot,(int(height*0.1),int(width*0.1)))

    wbg_new.save('data/2_dot_cube_final.png')

    wbg_new.paste(final_cube,(int(height*0.1),int(width*0.1)))

    wbg_new.save('data/2_cube_dot_final.png')
    
    

def init_1(in_var):
    
    in_ver,url,multiply,screen,opacity=in_var
    qr = qrcode.QRCode(
        version=in_ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0
    )
    
    
    QR.get_qr_frame(in_ver,bg_color = 254,level = 'H', quiet_zone_len = 0,img_size=10)
    
    qr.add_data(url)     

    image = qr.make_image()    
    image.save('data/qr.jpg')  
    
    
    
    qr_dot = qrcode.QRCode(
        version=in_ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=40,##這裡不動 由後續resize
        border=0
    )
    
    qr_dot.add_data(url)   
    qr_img = qr_dot.make_image(fill_color='black', back_color='white')
    
    
    dot.dot_2(qr_img, "#000000", "#FFFFFF")#2dot生成完畢
    
    qrsrc = cv2.imread('data/qr.jpg')
    insrc = cv2.imread('data/input.png') ##<- 原圖片
    frame = cv2.imread('data/qr_frame.png')


    qr_h,qr_w = getImageSize(qrsrc)

    dot_opacity = cv2.imread('data/dot2.png')

    dot_opacity = cv2.resize(dot_opacity,(qr_h,qr_w),interpolation=cv2.INTER_AREA)

    write_image('data/2dot_opacity.png',dot_opacity)

    ##=================================================================================================================

    """
        呼叫方法環節
    """

    QRArt_firstPack(in_ver,insrc,qrsrc,frame,multiply,screen,opacity)
    
def init_2(in_var):
    
    in_ver,url,thresh,mosaic=in_var
    qr = qrcode.QRCode(
        version=in_ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0
    )
    
    
    QR.get_qr_frame(in_ver,bg_color = 254,level = 'H', quiet_zone_len = 0,img_size=10)
    
    qr.add_data(url)     

    image = qr.make_image()    
    image.save('data/qr.jpg')  
    
    
    
    qr_dot = qrcode.QRCode(
        version=in_ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=40,##這裡不動 由後續resize
        border=0
    )
    
    qr_dot.add_data(url)   
    qr_img = qr_dot.make_image(fill_color='black', back_color='white')
    
    
    dot.dot_2(qr_img, "#000000", "#FFFFFF")#2dot生成完畢
    
    qrsrc = cv2.imread('data/qr.jpg')
    insrc = cv2.imread('data/input.png') ##<- 原圖片
    frame = cv2.imread('data/qr_frame.png')


    qr_h,qr_w = getImageSize(qrsrc)

    dot_opacity = cv2.imread('data/dot2.png')

    dot_opacity = cv2.resize(dot_opacity,(qr_h,qr_w),interpolation=cv2.INTER_AREA)

    write_image('data/2dot_opacity.png',dot_opacity)

    ##=================================================================================================================

    """
        呼叫方法環節
    """

    QRArt_secondPack(in_ver,insrc,qrsrc,frame,thresh,mosaic)
    
    
def first_3(in_var):
    url,fg,bg,lg,data_type=in_var
    
    
    qr = qrcode.QRCode(version = 3, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 40, border = 1)
    qr.add_data(url)
    qr.make(fit = True)
    qr_img = qr.make_image(fill_color='black', back_color='white')
    qr_version = int(((qr_img.size[0] / 40) - 21) / 4 + 1)
    QR.get_qr_frame(qr_version, bg_color = 160, level = 'M', mask = 1, quiet_zone_len = 4, img_size = 40, timing_pattern = False, version_inform = False, format_inform = False, quiet_zone = False)
    dot.dot(qr_img, fg, bg, lg,data_type)
    
    
    
def second_3(fg,bg):
    back = Image.open("data/input.png")
    dd = Image.open("data/dot.png")
    ff = Image.open("data/frame.png")
    back=back.resize(dd.size)
    dot.add_background_picture(back, dd, ff, fg, bg)
    

"""
    主程式
"""
if __name__ == '__main__':



    """
        參數表:
               QRcode參數  in_ver == QRcode_version
                           in_box == QRcode_box_size
                           in_border == QRcode_border
                           url_str == QRcode_data

              原圖讀取檔名 input_file = image_directory,圖片讀取位置

        第一種方法調整參數 multiply == 色彩增值效果倍率 (default = 1)
                           screen == 濾色效果倍率 (default = 1)
                           opacity == 透明處理倍率 (0 ~ 1)


        第二種方法調整參數 thresh == Image_threshold_edging-value,決定圖片的臨界值域值 (0 ~ 255)
                           mosaic == mosaic_alpha_value,調整強度用 (0 ~ box_size)
    """

    ##QRCode 輸入參數
    in_ver = 10
    in_box = 10
    in_border = 0
    url_str = 'https://www.google.com'

    ##第一種方法調整參數
    multiply = 1
    screen = 1
    opacity = 0.8

    ##第二種方法調整參數
    thresh = 200
    mosaic = 4
    
    ##原始圖片路徑,務必為長寬相等之正方形,不一定要等於QRCode原圖大小
    input_file = 'input3.png'




    """
        前處理環節
    """


    ##底圖生成
    qr = qrcode.QRCode(
        version=in_ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=in_box,
        border=in_border
    )
    
    ##=========================================================改動過 請複核===========================================


    #get_qr_frame(path,version, bg_color = 0, level = 'H', mask = 1, quiet_multi = 0, img_size = 10):
    qr_f = QR.get_qr_frame(in_ver,bg_color = 254,level = 'H', quiet_zone_len = 0,img_size=in_box)

    ##=================================================================================================================

    qr.add_data(url_str)     

    image = qr.make_image()    
    image.save('data/qr.jpg')  


    ##點圖生成
    qr_dot = qrcode.QRCode(
        version=in_ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=40,##這裡不動 由後續resize
        border=0
    )

    qr_dot.add_data(url_str)    

    qr_img = qr_dot.make_image(fill_color='black', back_color='white')

    dot.dot_2(qr_img, "#000000", "#FFFFFF")#2dot生成完畢



    ##=========================================================改動過 請複核===========================================
    ##改動執行順序,把公式填入替代掉,改成直接擷取qrcode的尺寸以防錯誤

    """
        讀取環節 
    """

    qrsrc = cv2.imread('data/qr.jpg')
    insrc = cv2.imread(input_file) ##<- 原圖片
    frame = cv2.imread('data/qr_frame.png')


    qr_h,qr_w = getImageSize(qrsrc)

    dot_opacity = cv2.imread('data/dot2.png')

    dot_opacity = cv2.resize(dot_opacity,(qr_h,qr_w),interpolation=cv2.INTER_AREA)

    write_image('data/2dot_opacity.png',dot_opacity)

    ##=================================================================================================================

    """
        呼叫方法環節
    """

    QRArt_firstPack(insrc,qrsrc,frame,multiply,screen,opacity) ##第一種方法呼叫 

    ##insrc = cv2.imread('data/input_logo.png')

    QRArt_secondPack(insrc,qrsrc,frame,thresh,mosaic) ##第二種方法呼叫 










