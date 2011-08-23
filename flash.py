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
#options = ['boot','system','recovery','-w','-k','--with-key','reboot']
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
'''
    if cmp(o,'boot') == 0 :
        flags['FBOOT'] = True

    if cmp(o,'system')== 0 :
        flags['FSYS'] = True

    if cmp(o,'-W')== 0 :
        flags['FWIPE'] = True

    if cmp(o,'--with-key') == 0 :
        flags['FKEY'] = True
 

def match_opt(o):
    #print "match " +o
    for opt in options:
        #print opt
        if cmp(o,opt) == 0:
            #flags[o]=True
            set_flag(o)
            return True
    return False
'''
def check_inoptions(opt):
    if len(opt) == 0 :
        print 'input options is 0'
        return False
    for o in opt:
        if set_flag(o) == False:
            return False
    return True
def do_flash():
    img_path = 'out/target/product/' + target_product + '/'
    boot_sig_path = img_path + 'boot.sig'
    system_sig_path = img_path + 'system.sig'
    recovery_sig_path= img_path + 'recovery.sig'

    boot_img_path = img_path + 'boot.img'
    system_img_path = img_path + 'system.img'
    recovery_img_path = img_path + 'recovery.img'

    fastboot = 'sudo ' + os.getenv('HOME') + '/android_tool/bin/fastboot'
    sig_cmd = fastboot +' signature {0}' 
    flash_cmd = fastboot + ' flash {0} {1}'
    reboot_cmd = fastboot + ' reboot'     
    wipe_cmd = fastboot + ' -w'

    if flags['REBOOT'] == True:
        print reboot_cmd
        os.system(reboot_cmd)
    elif flags['FWIPE'] ==True:
        print wipe_cmd
        os.system(wipe_cmd)
    else:
        if flags['FBOOT'] == True:
            if flags['FKEY']==True:    
                sig_boot = sig_cmd.format(boot_sig_path)
                print sig_boot
                os.system(sig_boot)
            flash_boot = flash_cmd.format('boot',boot_img_path)
            print flash_boot
            os.system(flash_boot)

        if flags['FSYS'] == True:
            if flags['FKEY']==True:    
                sig_system =sig_cmd.format(system_sig_path)
                print sig_system
                os.system(sig_system)
            flash_system = flash_cmd.format('system',system_img_path)
            print flash_system
            os.system(flash_system)

        if flags['FREC'] == True:
            if flags['FKEY']==True:    
                sig_system =sig_cmd.format(recovery_sig_path)
                print sig_system
                os.system(sig_system)
            flash_system = flash_cmd.format('recovery',recovery_img_path)
            print flash_system
            os.system(flash_system)
        
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
