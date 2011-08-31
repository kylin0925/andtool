#! /usr/bin/env python
# fast boot wrapper 
# 
# add otpion
#  --with-key 
#  boot
#  system
#  all
#  -w
# execute in android root ,
# auto find out/target/product/<sku>/
# fastboot signature <path_to_sig>/<sig_file>
# fastboot flash <image> <path_to_img>/<image_file>
# fastboot <cmd>
import sys
import os
import optparse
optmap = {'boot':'FBOOT','system':'FSYS','recovery':'FREC','-w':'FWIPE','--with-key':'FKEY','-k':'FKEY','reboot':'REBOOT'}
flags = {'FBOOT': False,'FSYS' : False,'FREC':False ,'FKEY': False,'FWIPE': False,'REBOOT':False}

target_product = ''
def set_flag(o):
    print 'set flag :',o
    if optmap.has_key(o) == True:
        flags[optmap[o]] = True
        return True
    else:
        return False

def check_inoptions(opt):
    if len(opt) == 0 :
        print 'input options is 0'
        return False
    for o in opt:
        if set_flag(o) == False:
            return False
    return True

def flash(img_type,path,with_key):
    fastboot = 'sudo ' + os.getenv('HOME') + '/android_tool/bin/fastboot'
    img_path = path + img_type + ".img"
    sig_path = path + img_type + ".sig"

    sig_cmd = fastboot +' signature {0}' 
    flash_cmd = fastboot + ' flash {0} {1}'

    if with_key == True:
        sig = sig_cmd.format(sig_path)
        print sig
        #os.system(sig)

    flash_img = flash_cmd.format(img_type,img_path)
    print flash_img
    os.system(flash_img)

def do_flash():
    img_path = 'out/target/product/' + target_product + '/'

    fastboot = 'sudo ' + os.getenv('HOME') + '/android_tool/bin/fastboot'
    reboot_cmd = fastboot + ' reboot'     
    wipe_cmd = fastboot + ' -w'

    key = flags['FKEY']
    if flags['FBOOT'] == True:
        flash('boot',img_path,key)

    if flags['FSYS'] == True:
        flash('system',img_path,key)

    if flags['FREC'] == True:
        flash('recovery',img_path,key)

    if flags['FWIPE'] ==True:
        print wipe_cmd
        os.system(wipe_cmd)
 
    if flags['REBOOT'] == True:
        print reboot_cmd
        os.system(reboot_cmd)

#-----------------
# start
#-----------------
args = sys.argv[1:]
#print args

if check_inoptions(args) ==False:
    print "arg error"
else:    
#    print "ok .....go"
#    print "flags :" ,flags

    target_product = os.getenv('TARGET_PRODUCT')
    print
    print "TARGET_PRODUCT " ,target_product
    print 
    if target_product == '' or target_product == None:
        print "error exec envset.sh"
    
    do_flash()
