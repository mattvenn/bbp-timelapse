#!/home/bristolbikeproject/.virtualenvs/timelapse/bin/python
import os
import datetime
import pdb;
import getpass
import gdata.youtube
import gdata.youtube.service
import youtube_keys

path = "/home/bristolbikeproject/timelapse/"
imagepath = path + "images/"
YOUTUBE_TEST_CLIENT_ID = 'timelapse'
video_file = 'timelapse.avi'
file_list = "files.txt"
fps = 10

def make_filelist():
    filelist = os.listdir(imagepath)
    sorted_filelist = sorted(filelist, key=lambda x: os.stat(imagepath+x).st_mtime)
    from_format = "%y-%m-%d-%H-%M-%S.jpg"
    to_format = "%A %H:%M"
    from_str = datetime.datetime.strptime(sorted_filelist[0], from_format).strftime(to_format)    
    to_str = datetime.datetime.strptime(sorted_filelist[-1], from_format).strftime(to_format)    
    title = from_str, 'to', to_str
    f = open(file_list,'w')
    for file in sorted_filelist:
        f.write(imagepath + file + "\n")
    f.close()
    return (title, len(sorted_filelist))

def make_timelapse():
    #remove old file
    try:
        os.unlink(video_file)
    except:
        pass
    command = "mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o %s -mf type=jpeg:fps=%d mf://@files.txt" % ( video_file, fps )
    os.system(command)

#this code from the unit test: 
#http://code.google.com/p/gdata-python-client/source/browse/tests/gdata_tests/youtube/service_test.py
def upload_timelapse(title):
    #login
    client = gdata.youtube.service.YouTubeService()
    client.email = youtube_keys.email
    client.password = youtube_keys.password
    client.source = YOUTUBE_TEST_CLIENT_ID
    client.developer_key = youtube_keys.dev_key
    client.client_id = YOUTUBE_TEST_CLIENT_ID
    client.ProgrammaticLogin()

    #titles
    test_video_title = 'workshop timelapse ' + title
    test_video_description = "bbp workshop timelapse at %d fps\nhttp://thebristolbikeproject.org" % fps

    #category,tags etc
    my_media_group = gdata.media.Group(
        title = gdata.media.Title(text=test_video_title),
        description = gdata.media.Description(description_type='plain',
                                            text=test_video_description),
        keywords = gdata.media.Keywords(text='timelapse, workshop'),
        category = gdata.media.Category(
            text='Entertainment',
            scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
            label='Entertainment'),

        player=None
    )
    
    print "uploading file:", test_video_title
    video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group) #, geo=where)
    new_entry = client.InsertVideoEntry(video_entry, video_file)
    
    # check upload status also
    upload_status = client.CheckUploadStatus(new_entry)
    link = new_entry.link[0].href
    print "status:", upload_status[0], " link: ", link
    return (upload_status[0],link)

    """
    # test to delete the entry
    value = self.client.DeleteVideoEntry(updated_entry)

    if not value:
      # sleep more and try again
      time.sleep(20)
      # test to delete the entry
      value = self.client.DeleteVideoEntry(updated_entry)

    """

def remove_files():
    print "removing files"
    f = open(file_list)
    for file in f.readlines():
        os.unlink(file.strip())

if __name__=="__main__":  
    #make the filelist
    (title, num_files) = make_filelist()
    exit(1)
    if num_files < 6 * 60: #6 hours of images
        print "not enough files: %d" % num_files
        exit(1)

    #make a timelapse using mencoder
    make_timelapse()

    #upload to youtube
    (status,link) = upload_timelapse(title)

    #if get a good status from youtube remove the files
    if status == 'processing':
        remove_files()
        f = open(path + "latest_vid", 'w')
        f.write(link)
        f.close()


