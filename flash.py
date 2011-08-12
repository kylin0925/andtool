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
options = ['boot','system','-w','--with-key']
flags = {'FBOOT': False,'FSYS' : False, 'FKEY': False,'FWIPE': False}
target_product = ''
def find_img_location():
    return
def match_opt(o):
    #print "match " +o
    for opt in options:
        print opt
        if cmp(o,opt) == 0:
            flags[o]=True
            return True
    return False

def check_inoptions(opt):
    if len(opt) == 0 :
        print 'input options is 0'
        return False
    for o in opt:
        if match_opt(o) == False:
            return False
    return True
def do_flash():

    fastboot= 'fastboot'
    sig_cmd = 'sudo fastboot signature {0}/{1}' 
    flash_cmd = 'sudo fastboot flash {0} {1}/{2}'
    
args = sys.argv[1:]
print args

if check_inoptions(args) ==False:
    print "arg error"
else:    
    print "ok .....go"
    print "flags :" ,flags

    target_product = os.getenv('TARGET_PRODUCT')
    print "TARGET_PRODUCT " ,target_product

    if target_product == '':
        print "error exec envset.sh"
    
    do_flash(s)
