import sensor, image, time, math

from machine import UART
import json

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA) # High Res!
#sensor.set_windowing((640, 80)) # V Res of 80 == less work (40 for 2X the speed).
sensor.skip_frames(30)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()
black = (0,10,-10,10,-10,10)
uart = UART(3, 115200)

def barcode_name(code):
    if(code.type() == image.EAN2):
        return "EAN2"
    if(code.type() == image.EAN5):
        return "EAN5"
    if(code.type() == image.EAN8):
        return "EAN8"
    if(code.type() == image.UPCE):
        return "UPCE"
    if(code.type() == image.ISBN10):
        return "ISBN10"
    if(code.type() == image.UPCA):
        return "UPCA"
    if(code.type() == image.EAN13):
        return "EAN13"
    if(code.type() == image.ISBN13):
        return "ISBN13"
    if(code.type() == image.I25):
        return "I25"
    if(code.type() == image.DATABAR):
        return "DATABAR"
    if(code.type() == image.DATABAR_EXP):
        return "DATABAR_EXP"
    if(code.type() == image.CODABAR):
        return "CODABAR"
    if(code.type() == image.CODE39):
        return "CODE39"
    if(code.type() == image.PDF417):
        return "PDF417"
    if(code.type() == image.CODE93):
        return "CODE93"
    if(code.type() == image.CODE128):
        return "CODE128"

while(True):
    clock.tick()
    img = sensor.snapshot()
    codes = img.find_barcodes()
    for code in codes:
        img.draw_rectangle(code.rect())
        #print_args = (barcode_name(code), code.payload(), (180 * code.rotation()) / math.pi, code.quality(), clock.fps())
        #print("Barcode %s, Payload \"%s\", rotation %f (degrees), quality %d, FPS %f" % print_args)

        if code.payload() == "123456789X":
            img.draw_rectangle(code.rect(), color=(255,0,0))

            blobs = img.find_blobs([black],roi=code.rect())#获取barcode角度
            for blob in blobs:
                barcode = blob.rotation()*180/math.pi - 90
                print(barcode)

            output_str = json.dumps([code.payload(), code.rect(), ])
            print("send:"+output_str+'\r\n')
            uart.write(output_str)
        else:
            img.draw_rectangle(code.rect())

    if not codes:
        print("FPS %f" % clock.fps())
    uart.write("output_str")
