import os
import urllib
import urllib2
import urlparse
import cookielib
import time
from bs4 import BeautifulSoup

class BitfountainCourse:
    courses = {
        'iOS8':
                ('Bitfountain iOS8 Course',
                'http://bitfountain.io/courses/complete-ios8/lectures/4142'),
        'AppleWatch':
                ('Bitfountain Apple Watch Course',
                'http://bitfountain.io/courses/iwatch-course/lectures/84542'),
        'FlappyBird':
                ('Bitfountain iOS7 Flappy Bird Clone',
                'http://bitfountain.io/courses/the-complete-ios-game-course-build-a-flappy-bird-clone/lectures/4741'),
        }

    def __init__(self, name, start_url):
        self.name = os.path.join('output', name)
        self.start_url = start_url

    @staticmethod
    def login(email, password):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0')]

        # install our opener (note that this changes the global opener
        urllib2.install_opener(opener)

        authentication_url = 'https://sso.usefedora.com/secure/24/users/sign_in'

        form_data = {
          'user[school_id]': '24',
          'user[email]': email,
          'user[password]': password,
          'commit': 'Log+in'
          }

        data = urllib.urlencode(form_data)
        req = urllib2.Request(authentication_url, data)

        resp = urllib2.urlopen(req)
        contents = resp.read()

        return 'Invalid email or password.' not in contents

    @staticmethod
    def download_course(course_alias, simulate):
        try:
            course_info = BitfountainCourse.courses[course_alias]
        except:
            print "Error: Bad course Alias"
            return

        course = BitfountainCourse(course_info[0], course_info[1])
        course.download_all(simulate=simulate)

    def download_all(self, simulate):
        if simulate == False:
            os.makedirs(self.name)

        cur_url = self.start_url
        video_number = 1
        while cur_url != None:
            video_found, cur_url = self.crawl(cur_url, video_number, simulate)
            video_number += 1 if video_found == True else 0

    def download_video(self, url, filename, simulate):
        self.previous_progress = -1
        self.dl_total_size = -1

        def report_hook(blocks_read, block_size_bytes, total_size):
            bytes_read = float(blocks_read * block_size_bytes)
            perc = bytes_read / total_size
            perc_100 = int(perc * 100)
            if self.previous_progress != perc_100:
                if (perc_100 + 1) % 10 == 0:
                    print("*"),
                self.previous_progress = perc_100

                if self.dl_total_size == -1:
                    self.dl_total_size = total_size
                    print("%d MiB - Progress: " % (total_size / 1024 / 1024)),

        print "Downloading %s" % url
        if simulate == False:
            time_start = time.time()
            mp4_resp = urllib.urlretrieve(url, filename + '.temp', report_hook)
            total_time = time.time() - time_start

            dl_rate = (self.dl_total_size / 1024 / 1024) / total_time

            os.rename(filename + '.temp', filename)
        else:
            dl_rate = 0

        print "\nDownload Complete in %2d seconds (%2.2f MiB/s): %s" % (total_time, dl_rate, filename)
    
    def crawl(self, url, video_number, simulate):
        print '------------------------------BEGIN-----------------------------------'

        course_page_req = urllib2.Request(url)
        course_page_resp = urllib2.urlopen(course_page_req)
        course_page_contents = course_page_resp.read()
        soup = BeautifulSoup(course_page_contents)

        download_url = None
        try:
            download_url_tag = soup.find('a', class_="download")
            download_url = download_url_tag['href']
        except:
            print 'skipping -- no download or next lecture tag!'
    
        if download_url != None:
            lecture_heading = soup.find('h2', id='lecture_heading', class_="section-title")
            video_file_name = lecture_heading.text.strip() + '.mp4'
            video_file_name = os.path.join(self.name, "%03d - %s" % (video_number, video_file_name))
            self.download_video(download_url, video_file_name, simulate)
            video_found = True
        else:
            video_found = False
    
        print '-------------------------------END----------------------------------\n'
    
        next_url = None
        try:
            next_lecture_tag = soup.find('a', id="lecture_complete_button")
            next_url = next_lecture_tag['href']
            next_url = urlparse.urljoin('http://bitfountain.io/', next_url)
        except:
            print "no more urls to crawl"

        return (video_found, next_url)