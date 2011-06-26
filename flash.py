#! /usr/bin/env python
# flash obm path
# flash normal path

import sys
print sys.argv
argc = len(sys.argv)
if argc !=3 :
    print "error"
else:
    cmdsig = 'sudo ./fastflash signature {0}/{1}' 
    sigboot = cmdsig.format(sys.argv[2],'boot.sig');
    sigsystem = cmdsig.format(sys.argv[2],'system.sig');

    command = 'sudo ./fastflash flash {0} {1}/{2}'
    
    flashboot = command.format('boot',sys.argv[1],'boot.img');
    flashsystem = command.format('system',sys.argv[1],'system.img');

    print sigboot
    print sigsystem

    print flashboot
    print flashsystem

