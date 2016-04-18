import glob
import os
import string
import argparse

def checkImagefileAndExist(path):
    if checkImagefile(path):
        if not os.path.isdir(path):
            return True
    return False

def checkImagefile(path):
    tmp, ext = os.path.splitext(path)
    if ext == ".jpg":
        return True
    elif ext == ".bmp":
        return True
    return False

def getdirlist(path):
    dirs = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
    return dirs

def getdirslist(path):
    for root, dirs, files in os.walk(path):
        yield root
        for file in files:
            yield os.path.join(root, file)

def getfilepath(path):
    return glob.glob(path + "/*.*")

def getlstname(path):
    return path.replace("/", "")

def getlist(path, target, tag):
    f = open(target + "/" + getlstname(path) + ".lst", "w")
    for e in getdirslist(path):
        if checkImagefileAndExist(e):
            f.write(e + " " + str(tag) + "\n")
    f.close()

def getlist_Ncustom(path, target, tag, interval):
    counter = 0
    cnt = 0
    f = open(target + "/" + getlstname(path) + "_NcInt" + str(interval) + ".lst", "w")
    for e in getdirslist(path):
        if checkImagefileAndExist(e):
            cnt += 1
            if cnt % interval == 0:
                print(str(counter))
                f.write(e + " " + str(tag) + "\n")
                counter += 1
    f.close()

def getlist_custom(path, target, tag, interval):
    counter = 0
    cnt = 0
    f = open(target + "/" + getlstname(path) + "_cInt" + str(interval) + ".lst", "w")
    for e in getdirslist(path):
        if checkImagefileAndExist(e):
            cnt += 1
            if cnt % interval != 0:
                print(str(counter))
                f.write(e + " " + str(tag) + "\n")
                counter += 1
    f.close()

def getlist_Eliminate(path, target, tag, eliminate):
    counter = 0
    Elist = []
    f = open(eliminate)
    data1 = f.read()
    f.close()
    lines1 = data1.split('\n')
    for line in lines1:
        Elist.append(line.split(' ')[0])
    f = open(target + "/" + getlstname(path) + "_E.lst", "w")
    for e in getdirslist(path):
        if checkImagefileAndExist(e):
            if not e in Elist:
                print(str(counter))
                f.write(e + " " + str(tag) + "\n")
                counter += 1
    f.close()

parser = argparse.ArgumentParser()
parser.add_argument("source_dir", help='ImageFile Dir')
parser.add_argument("target_dir", help='ImageList Output Dir')
parser.add_argument('tag', help='Image Identifer tag')
parser.add_argument('--interval', '-I', type=int, default=0,
                    help='Choose Image time of Interval')
parser.add_argument('--notInterval', '-N', type=int, default=0,
                    help='Not Choose Image time of Interval')
parser.add_argument('--eliminate', '-E', default='None',
                    help='eliminate listfile image')
args = parser.parse_args()


if args.notInterval != 0:
    getlist_Ncustom(args.source_dir, args.target_dir, args.tag, args.notInterval)
elif args.eliminate != "None":
    getlist_Eliminate(args.source_dir, args.target_dir, args.tag, args.eliminate)
elif args.interval != 0:
    getlist_custom(args.source_dir, args.target_dir, args.tag, args.interval)
else:
    getlist(args.source_dir, args.target_dir, args.tag)
