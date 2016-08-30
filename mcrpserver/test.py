f = open('TEST.txt', 'r')

string = f.read()
print len(string)

for i in range(len(string)):
    checksum = 0
    for j in range(len(string) - i):
        checksum += ord(string[i+j])
        if checksum > 0xB632:
            break
        elif checksum == 0xB632:
            print 'Success!', ',', string[j], ',1', string[j+1], ',2', string[j+2], ',3', string[j+3], ',4', string[j+4], ',5', string[j+5]
            break

f.close()