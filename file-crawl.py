import os
import subprocess
import sqlite3


#bool

populate_info = True
clean_filenames = True
count = 1

video_types = [
    '.mp4',
    '.mkv',
    ".avi",
    ".flv"
]

class Video:
    def __init__(self, name, dir, size, duration, height, width):
        self.name = name
        self.duration = duration
        self.height = height
        self.width = width
        self.dir = dir

con = sqlite3.connect("videos.db")

cur = con.cursor()

def ex_db(command_str: str):
    cur.execute(command_str)
    con.commit()



def is_video(input_string: str):
    output = False
    for i in video_types:
        #print(i)
        if str(input_string).endswith(i):
            output = True
    
    return output

def get_mediainfo(video: str):
    
    file_size_mb = os.stat(video).st_size / (1024 * 1024)
    file_size_mb = round(file_size_mb, 2)
    #print(f'Size: {file_size_mb} MB')
    size = str(file_size_mb) + 'MB'
    #os info get file size
    # duration, height, width, size

    #cmd = 'mediainfo --Inform="General;%Duration%"' 
    cc = f"{video} is {size}"
    cmd1 = f"mediainfo --Inform=\"General;%Duration%\" {video}"
    cmd2 = f"mediainfo --Inform=\"Video;%Height%\" {video}"
    cmd3 = f"mediainfo --Inform=\"Video;%Width%\" {video}"
    duration = subprocess.getoutput(cmd1)
    try:
        duration = round(int(duration)/1000/60, 2)
    except ValueError:
        print(f"duration not found! - {ValueError}")
    height = subprocess.getoutput(cmd2)
    width = subprocess.getoutput(cmd3)
    
    output = [size, duration, height, width]
    print(f"{video} - {size} - Duration: {duration}min - Height - {height}px - Width {width}px")
    
    #output2 = subprocess.getoutput('mediainfo --Inform="General;%Duration%" 2.avi')

def get_mediainfo2(video: str, dir_str: str):
    
    file_size_mb = os.stat(video).st_size / (1024 * 1024)
    file_size_mb = round(file_size_mb, 2)
    #print(f'Size: {file_size_mb} MB')
    size = str(file_size_mb) + 'MB'
    #os info get file size
    # duration, height, width, size

    #cmd = 'mediainfo --Inform="General;%Duration%"' 
    cc = f"{video} is {size}"
    cmd1 = f"mediainfo --Inform=\"General;%Duration%\" {video}"
    cmd2 = f"mediainfo --Inform=\"Video;%Height%\" {video}"
    cmd3 = f"mediainfo --Inform=\"Video;%Width%\" {video}"
    duration = subprocess.getoutput(cmd1)
    try:
        duration = round(int(duration)/1000/60, 2)
    except ValueError:
        print(f"duration not found! - {ValueError}")
    height = subprocess.getoutput(cmd2)
    width = subprocess.getoutput(cmd3)
    
    output = [size, duration, height, width]
    print(f"{video} - {size} - Duration: {duration}min - Height - {height}px - Width {width}px")
    
    global count

    c1 = f"""
        INSERT INTO videos VALUES
            ({count}, \'{video}\', \'{dir_str}\', \'{size}\', \'{duration}\', {width}, {height})
    """
    ex_db(c1)
    count += 1




thisfolder = os.getcwd()
# string of the last directory
lastdir = ""


# search for ' and rename

def tidy_name(input: str):
    spaced = False
    output = ""
    for c in input:
        if c != ' ' and c!= "\'":
            output += c
        else:
            spaced = True
            output += '.'
    return spaced, output

# media info won't work properly if file names contain spaces
def rename_nospaces():
    rename_count = 0
    for (root, dirs, file) in os.walk(thisfolder):
        for item in file:
            if is_video(item) == True:
                lastdir = root
                os.chdir(root)
                spaced, name = tidy_name(item)
                if spaced:
                    print(f"renamed {item} -> {name}")
                    os.rename(item, name)
                    rename_count += 1
                else:
                    print(f"{name}")

    if rename_count == 0:
        print("no files renamed!")
    else:
        print(f"Number of files renamed with no spaces{rename_count}")


# find every video and get mediainfo
if populate_info == True:
    #list all videos in current working directory
    for (root, dirs, file) in os.walk(thisfolder):
        for item in file:
            if is_video(item) == True:
                #print(item)
                lastdir = root
                os.chdir(root)
                get_mediainfo2(item, root)
                
                
                #print the root folder
                #print(root)

            else:
                pass

#todo - 
# mediainfo on teach file get duration, height, width, 
# get each file size
# add each one to a database
# give each file a unique primary key
# find duplicates (remove?)

# only run at the start
if clean_filenames == False:
    rename_nospaces()




#cmd2 = ['ls','-l']
#result = subprocess.run(cmd1, stdout=subprocess.PIPE)
#print(result.stdout.decode('utf-8'))
#print(lastdir)

#get_mediainfo("1.avi")

"""
cmd = ['mediainfo', '2.avi']
result = subprocess.run(cmd, stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))

output2 = subprocess.getoutput('mediainfo --Inform="General;%Duration%" 2.avi')
print(output2)



cmd = ['mediainfo', '2.avi']
result = subprocess.run(cmd, stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))

output2 = subprocess.getoutput('mediainfo --Inform="General;%Duration%" 2.avi')
print(output2)


output2 = subprocess.getoutput('mediainfo --Inform="Video;%Height%" 2.avi')
print(output2)




"""
