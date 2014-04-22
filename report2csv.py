#-------------------------------------------------------------------------------
# Name:        report2csv
# Purpose:
#
# Author:      krh5058
#
# Created:     22/04/2014
# Copyright:   (c) krh5058 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import os
import re
import sys

def write_csv(file,list):
    try:
        file.writerow(list)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

def main(argv):
    try:
       f = open('reports/140422.html', 'r')
       csvfile = open('140422.csv', 'w', newline='')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    try:
##    filedir = os.path.join(os.path.dirname(__file__), 'reports/')

        head = ['pi-id', 'project-id', 'billable-approved', 'billable-used', 'billable-remaining', 'in-kind-session-approved', 'in-kind-session-used', 'in-kind-session-remaining', 'in-kind-other-approved', 'in-kind-other-used', 'in-kind-other-remaining']

        fwrite = csv.writer(csvfile, delimiter=',')
        write_csv(fwrite,head)

        projn = 0
        storeswitch = False;
        l=[]
        for line in f:
##            print(line)
            if re.search(r'ProjectID',line):
                projn = projn + 1

                proj = re.search('\w{3}\d{1,4}_\w{3,4}',line)
                if proj:
                    l.append(re.search('\w{3}\d{1,4}',proj.group(0)).group(0))
                    print(l[0])
                    l.append(proj.group(0))
                    print(l[1])
            elif re.search(r'<TABLE',line):
                if projn>0:
                    storeswitch = True;
                    write_l = l
                    print(storeswitch)
            elif re.search(r'</TABLE>',line):
                if storeswitch:
                    write_csv(fwrite,write_l)
                    l=[]
                    write_l=[]
                    storeswitch = False;
                    print(storeswitch)
            else:
                dat = re.search('[-]?\d+[.]{1}\d{2}',line)
                if dat:
                    print(dat.group(0))
                    if storeswitch:
                        write_l.append(dat.group(0))
##                if storeswitch:
##                    l.append(

        print(projn, ' matches found.')
        print('Done!')
    finally:
        f.close()
        csvfile.close()

if __name__ == '__main__':
    main(sys.argv)
