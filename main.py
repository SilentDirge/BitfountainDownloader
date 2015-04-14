from BitfountainCourse import BitfountainCourse
import sys

if len(sys.argv) == 2 and sys.argv[1] == 'delete':
    import shutil
    shutil.rmtree('output')
    exit()

if len(sys.argv) < 4:
    print 'Usage: <email> <password> <courseAlias> <simulate>[optional] <start_index:alternate_url>[optional]'
    print 'Aliases: iOS8, AppleWatch, FlappyBird'
    exit()

if BitfountainCourse.login(sys.argv[1], sys.argv[2]):
    if len(sys.argv) >= 6:
        import urlparse
        start_index, alternate_url = sys.argv[5].split(':', 1)
        start_index = int(start_index)
        urlp = urlparse.urlparse(alternate_url)
        if not urlp.scheme:
            print "ERROR: invalid URL passed in as the starting URL"
            exit()
        start_url = alternate_url
    else:
        start_index = 1
        start_url = None

    if len(sys.argv) >= 5:
        simulate = sys.argv[4].lower() == 'true'
    else:
        simulate = False

    BitfountainCourse.download_course(sys.argv[3], simulate, start_url, start_index)
else:
    print 'Invalid email or password.'
