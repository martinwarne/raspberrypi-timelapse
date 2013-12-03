import dropbox
import json
import os
import time


class DropboxUpload(object):
    """Simple Class to help uploading files to Dropbox"""

    @staticmethod
    def _read_value(file, json_key):
        json_file = open("{file}.json".format(file=file), "r")
        data = json.load(json_file)
        json_file.close()
        try:
            return data[json_key]
        except KeyError:
            return False

    @staticmethod
    def _save_access_token(access_token):
        # load the json
        json_file = open("data.json", "r")
        data = json.load(json_file)
        json_file.close()
        # edit the value
        data['accessToken'] = access_token
        # save the file
        json_file = open("data.json", "w+")
        json_file.write(json.dumps(data))
        json_file.close()
        return True

    @classmethod
    def _get_access_token(cls):
        """
        Return the Dropbox access token if we have one or get the user to 
        generate it
        """

        # If we already have an access token
        access_token = cls._read_value('data', 'accessToken')
        if access_token:
            return access_token
        else:
            app_key = self._read_value('settings', 'appKey')
            app_secret = self._read_value('settings', 'appSecret')
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, 
                                                              app_secret)
            authorize_url = flow.start()
            print '1. Go to: ' + authorize_url
            print '2. Click "Allow" (you might have to log in first)'
            print '3. Copy the authorization code.'
            code = raw_input("Enter the authorization code here: ").strip()
            access_token, user_id = flow.finish(code)
            cls._save_access_token(access_token=access_token)
            return access_token

    @classmethod
    def _get_client(cls):
        """Get the Dropbox client"""
        access_token = cls._get_access_token()
        return dropbox.client.DropboxClient(access_token)

    @classmethod
    def upload_file(cls, file_path, filename):
        """Upload a file to the server"""
        f = open("{file_path}".format(file_path=file_path), 'r')
        client = cls._get_client()
        response = client.put_file(filename, f, overwrite=True)
        print "uploaded:", response
        return filename


class RaspberryPiCamera:
    """Class to interact through the RaspberryPi camera"""
    
    def __init__(self):
        self.folder = 'images'
        self.last_filename = ''

    def _create_name(self):
        """Create a filename based off the counter"""

        # load the json
        json_file = open("data.json", "r")
        data = json.load(json_file)
        json_file.close()
        # edit the value
        counter = data['counter'] + 1
        data['counter'] = counter
        # save the file
        json_file = open("data.json", "w+")
        json_file.write(json.dumps(data))
        json_file.close()

        return 'image-%04d.jpg' % (counter,)

    def get_picture_location(self, filename=False):
        """
        By default returns the path to the last file. If a filename is passed in
        then it will return the location that file will be save to.
        """
        if not filename:
            filename = self.last_filename
        return "{folder}/{filename}".format(folder=self.folder, 
                                            filename=filename)

    def take_picture(self):
        """Take a picture with the camera"""
        filename = self._create_name()
        file_location = self.get_picture_location(filename=filename)
        os.system("raspistill -o {path_to_image}".format(path_to_image=file_location))
        self.last_filename = filename
        return True


class VideoGenerator(object):
    """Takes a series of images and produces a time lapse video out of them"""
    file_path = 'images'
    filename = 'timelapse.mp4'

    @staticmethod
    def create_video():
        """Use anconv to create the timelapse."""
        # TODO this is really slow. Need to find a way to do it remotely on a
        # more powerful box
        os.system("avconv -y -i images/image-%04d.jpg -r 10 video/timelapse.mp4")
        return True


def main():
    """
    Takes a picture, uploads it to Dropbox.
    Makes a timelapse video, uploads it to Dropbox.
    """
    # Take a photo
    camera = RaspberryPiCamera()
    picture = camera.take_picture()

    # Upload the image
    DropboxUpload.upload_file(file_path=camera.get_picture_location(), 
                              filename=camera.last_filename)

    # Make the video
    video = VideoGenerator.create_video()

    # Upload the video
    DropboxUpload.upload_file(file_path='video/timelapse.mp4',
                              filename='timelapse.mp4')

if __name__ == "__main__":
    main()
