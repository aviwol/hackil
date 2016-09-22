import random
import time

WEBSITE_TEMPLATE = (
    {'page': 'index.html', 'prob': 80, 'bytes': 1058, 'code': 200, 'allowed': {'about.html': 20, 'contact.html': 20, 'career.html': 20, 'blog.html': 20}},
    {'page': 'contact.html', 'prob': 50, 'bytes': 1029, 'code': 200, 'allowed': {'about.html': 40, 'career.html': 40}},
    {'page': 'about.html', 'prob': 50, 'bytes': 954, 'code': 200, 'allowed': {'index.html': 20, 'contact.html': 20, 'career.html': 20}},
    {'page': 'career.html', 'prob': 20, 'bytes': 699, 'code': 200},
    {'page': 'blog/', 'prob': 50, 'bytes': 999, 'code': 200},
    [
        {'page': '/blog/post1.html', 'prob': 40, 'bytes': 628, 'code': 200}, 
        {'page': '/blog/post2.html', 'prob': 40, 'bytes': 456, 'code': 200}, 
        {'page': '/blog/post3.html', 'prob': 40, 'bytes': 852, 'code': 200}, 
        {'page': '/blog/post4.html', 'prob': 40, 'bytes': 349, 'code': 200}, 
        {'page': '/blog/post5.html', 'prob': 40, 'bytes': 222, 'code': 200}, 
        {'page': '/blog/post6.html', 'prob': 40, 'bytes': 897, 'code': 200}, 
        {'page': '/blog/post7.html', 'prob': 40, 'bytes': 623, 'code': 200}, 
        {'page': '/blog/post8.html', 'prob': 40, 'bytes': 864, 'code': 200}, 
        {'page': '/blog/post9.html', 'prob': 40, 'bytes': 371, 'code': 200}, 
        {'page': '/blog/post10.html', 'prob': 40, 'bytes': 128, 'code': 200}
    ]
)

#Set list of IPS
IPS = []

def write_logs(USER_ACTIVITY):
    for i in USER_ACTIVITY['pages']:

        TEMPLATE = '{0} - - [{1}] "GET {2}" {4} {3}'.format(USER_ACTIVITY['ip'], i['timestamp'], i['page'], i['bytes'], i['code'])
        print TEMPLATE
        f = open("log.txt", "ab")
        f.write(TEMPLATE +"\r\n")
        f.close()
    print "--------------------------------------------------------"

def create_fake_ip(): 
    IP = "{0}.{1}.{2}.{3}".format(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
    return IP

def create_fake_view():
    random_page = WEBSITE_TEMPLATE[random.randint(0, len(WEBSITE_TEMPLATE)-1)]
    if type(random_page) == type([]):
        random_page = random_page[random.randint(0, len(WEBSITE_TEMPLATE[4])-1)]
    return random_page

def create_user_activity():
    pages = []
    finished = []
    previous_page = ""
    exit = False
    tim = time.time()+random.randint(0, 120)

    while exit == False:
        rand = random.randint(0, 100)
        if rand <= 15:
            exit = True
        else:
            print exit
            activity = create_fake_view()
            while activity['page'] == previous_page:
                activity = create_fake_view() 
            previous_page = activity['page']
            if "/blog" in activity['page'] and "blog/" not in finished:
                activity = create_fake_view()
                pass
            else:
                tim += random.randint(2, 60)
                activity['timestamp'] = tim
                activity['new_timestamp'] = time.ctime()
                pages.append(activity)
                finished.append(activity['page'])
    print pages
    return {'pages': pages}

def write_hacker_log(ip):
    f = open('hacker.log', 'ab')
    f.write(ip+"\r\n")
    f.close()

def create_hacker_activity():
    pages = []
    exit = False

    while exit == False:
        rand = random.randint(0, 100)
        if rand <= 5:
            exit = True
        else:
            activity = create_fake_view()
            activity['timestamp'] = time.time()
            pages.append(activity)
    return {'pages': pages}
             

if __name__ == '__main__':
    for i in range(0, 1):
        randi = random.randint(0, 100)
        ip = create_fake_ip()
        if ip in IPS:
            while ip in IPS:
                ip = create_fake_ip()
        IPS.append(ip)
        if randi <= 1:
            package = create_hacker_activity()
            write_hacker_log(ip)
        else:
            package = create_user_activity()
        package['ip'] = ip
        write_logs(package)
    print "Done."