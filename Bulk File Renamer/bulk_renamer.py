import os



def main():
    i = 0
    path = "E:/GIAIC/Quarter 3/Assignments/Assignment Projects/Bulk File Renamer/New folder/"
    for filename in os.listdir(path):
        my_dest = "image" + str(i) + ".png"
        my_source = path + filename
        my_dest = path + my_dest
        os.rename(my_source,my_dest)
        i += 1 

if __name__ == '__main__':
    main()