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
optmap = {
    'boot':'FBOOT',
    'system':'FSYS',
    'recovery':'FREC',
    'userdata':'FUDAT',
    '-w':'FWIPE',
    '--with-key':'FKEY',
    '-k':'FKEY',
    'reboot':'REBOOT',
    '-p':'FPATH',
    '-2k':'F2K'
    }
flags = {
    'FBOOT' : False,
    'FSYS'  : False,
    'FREC'  : False,
    'FUDAT' : False,
    'FKEY'  : False,
    'FWIPE' : False,
    'REBOOT': False,
    'FPATH' : False,
    'F2K'   : False
    }

target_product = ''
img_path = 'out/target/product/' + target_product + '/'
img_2k_path = img_path + '2kpagenand_images/'
img_dict = {
    'boot':'boot.img',
    'system':'system.img',
    'userdata':'userdata.img',
    'recovery':'recovery.img',
    'boot.2knand':'boot.2knand.img',
    'system.2knand':'system.2knand.img',
    'userdata.2knand':'userdata.2knand.img',
    'recovery.2knand':'recovery.2knand.img',
    }

sig_dict = {
    'boot':'boot.sig',
    'system':'system.sig',
    'userdata':'userdata.sig',
    'recovery':'recovery.sig',
    'boot.2knand':'boot.2knand.sig',
    'system.2knand':'system.2knand.sig',
    'userdata.2knand':'userdata.2knand.sig',
    'recovery.2knand':'recovery.2knand.sig',
    }
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
        if o!= '-p' and set_flag(o) == False:
            return False
        elif o == '-p' :
            path = o[2:]
            if path[0] != '=':
                return False
            print path[1:]
            img_path = path[1:]
            set_flag(o)
    return True

def flash(img_type,path,with_key):
    fastboot = 'sudo ' + os.getenv('HOME') + '/android_tool/bin/fastboot'
    img2k = '.2knand'
    if flags['F2K'] == True:
        print "check 2k path " + img_2k_path
        if os.access(img_2k_path,os.R_OK) == True:
            img_path = img_2k_path + img_dict[img_type + img2k]
            sig_path = img_2k_path + sig_dict[img_type + img2k]
        else:
            img_path = path + img_dict[img_type + img2k]
            sig_path = path + sig_dict[img_type + img2k]
    else:
        img_path = path + img_dict[img_type]
        sig_path = path + sig_dict[img_type]

    sig_cmd = fastboot +' signature {0}' 
    flash_cmd = fastboot + ' flash {0} {1}'

    if with_key == True:
        sig = sig_cmd.format(sig_path)
        print sig
        os.system(sig)

    flash_img = flash_cmd.format(img_type,img_path)
    print flash_img
    os.system(flash_img)

def do_flash():

    fastboot = 'sudo ' + os.getenv('HOME') + '/android_tool/bin/fastboot'
    reboot_cmd = fastboot + ' reboot'     
    wipe_cmd = fastboot + ' -w'

    key = flags['FKEY']
    if flags['FBOOT'] == True:
        flash('boot',img_path,key)

    if flags['FSYS'] == True:
        flash('system',img_path,key)

    if flags['FUDAT'] == True:
        flash('userdata',img_path,key)

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
# for test
    #target_product = "test"
    if target_product == '' or target_product == None:
        print "error exec envset.sh"
        sys.exit(1)

    img_path = 'out/target/product/' + target_product + '/'
    img_2k_path = img_path + '2kpagenand_images/'
    do_flash()
