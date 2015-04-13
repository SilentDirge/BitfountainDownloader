from BitfountainCourse import BitfountainCourse
import sys

if len(sys.argv) == 2 and sys.argv[1] == 'delete':
    import shutil
    shutil.rmtree('output')
    exit()

if len(sys.argv) < 4:
    print 'Usage: <email> <password> <courseAlias> <simulate>[optional]'
    print 'Aliases: iOS8, AppleWatch, FlappyBird'
    exit()

if BitfountainCourse.login(sys.argv[1], sys.argv[2]):
    if len(sys.argv) == 5:
        simulate = sys.argv[4].lower() == 'true'
    else:
        simulate = False

    BitfountainCourse.download_course(sys.argv[3], simulate)
else:
    print 'Invalid email or password.'
