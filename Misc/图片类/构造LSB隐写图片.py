from PIL import Image
import sys

def toasc(strr):
    return int(strr, 2)       
         
#str1为所要提取的信息的长度（根据需要修改），str2为加密载体图片的路径，str3为提取文件的保存路径
def decode(str1,str2,str3): 
    b="" 
    im = Image.open(str2)
    lenth = int(str1)*8  
    width,height = im.size[0],im.size[1]
    count = 0
    for h in range(height): 
        for w in range(width):
            #获得(w,h)点像素的值
            pixel = im.getpixel((w, h))
            #此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息 
            if count%3==0:
                count+=1 
                b=b+str((mod(int(pixel[0]),2))) 
                if count ==lenth:
                    break
            if count%3==1:
                count+=1
                b=b+str((mod(int(pixel[1]),2)))
                if count ==lenth:
                    break
            if count%3==2: 
                count+=1
                b=b+str((mod(int(pixel[2]),2)))
                if count ==lenth:
                    break
        if count == lenth:
            break
 
    with open(str3,"w",encoding='utf-8') as f: 
        for i in range(0,len(b),8):
            #以每8位为一组二进制，转换为十进制            
            stra = toasc(b[i:i+8]) 
            #将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            #print((stra))
            f.write(chr(stra))
    print("sussess")

def plus(string): 
    #Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    return string.zfill(8)
 
def get_key(strr):
    #获取要隐藏的文件内容
    with open(strr,"rb")  as f:
        s = f.read()
        string=""
        for i in range(len(s)):
         #逐个字节将要隐藏的文件内容转换为二进制，并拼接起来 
         #1.先用ord()函数将s的内容逐个转换为ascii码
         #2.使用bin()函数将十进制的ascii码转换为二进制
         #3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
         #4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
            string=string+""+plus(bin(s[i]).replace('0b',''))
    #print(string) 
    return string

def mod(x,y):
    return x%y

#str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径 
def encode(str1,str2,str3): 
    im = Image.open(str1) 
    #获取图片的宽和高
    width,height= im.size[0],im.size[1]
    print("width:"+str(width))
    print("height:"+str(height))
    count = 0
    #获取需要隐藏的信息 
    key = get_key(str2) 
    keylen = len(key)
    for h in range(height):
        for w in range(width):
            pixel = im.getpixel((w,h))
            a=pixel[0]
            b=pixel[1]
            c=pixel[2]
            if count == keylen:
                break
            #下面的操作是将信息隐藏进去 
            #分别将每个像素点的RGB值余2，这样可以去掉最低位的值
            #再从需要隐藏的信息中取出一位，转换为整型
            #两值相加，就把信息隐藏起来了
            a= a-mod(a,2)+int(key[count])
            count+=1
            if count == keylen:
                im.putpixel((w,h),(a,b,c)) 
                break
            b =b-mod(b,2)+int(key[count])
            count+=1 
            if count == keylen:
                im.putpixel((w,h),(a,b,c)) 
                break
            c= c-mod(c,2)+int(key[count])
            count+=1
            if count == keylen:
                im.putpixel((w,h),(a,b,c))
                break
            if count % 3 == 0:
                im.putpixel((w,h),(a,b,c))
    im.save(str3)


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 2:
        print ('Usage: python test.py <cmd> [arg...] [opts...]')
        print ('  cmds:')
        print ('    encode image + flag -> image(encoded)')
        print ('    decode length + image(encoded) -> flag')
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd != 'encode' and cmd != 'decode':
        print('wrong input')
        sys.exit(1)
    str1 = sys.argv[2]
    str2 = sys.argv[3]
    str3 = sys.argv[4]
    if cmd != 'encode' and cmd != 'decode':
        print ('Wrong cmd %s' % cmd)
        sys.exit(1)
    elif cmd=='encode':
        encode(str1,str2,str3)
    elif cmd=='decode':
        decode(str1,str2,str3)