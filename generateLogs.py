import random
import time
import numpy

WEBSITE_TEMPLATE = (
    {'page': 'index.html', 'prob': 80, 'bytes': 1058, 'code': 200},
    {'page': 'contact.html', 'prob': 50, 'bytes': 1029, 'code': 200},
    {'page': 'about.html', 'prob': 50, 'bytes': 954, 'code': 200},
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

RULES = {
    'index.html': {'about.html': 20, 'contact.html': 40, 'career.html': 60, 'blog.html': 80},
    'about.html': {'index.html': 20, 'contact.html': 20, 'career.html': 20}, 
    'contact.html': {'about.html': 40, 'career.html': 80}, 
    'blog/': {'index.html': 30, 'posts': 80}, 
    'career.html': {'index.html': 40, 'about.html': 80}, 
    'posts': {'index.html': 20, 'posts': 50}#, 'blog/': 80}
    }

#Set list of IPS
IPS = []

def write_logs(USER_ACTIVITY):
    for i in USER_ACTIVITY['pages']:
        TEMPLATE = '{0} - - [{1}] "GET {2}" {4} {3}'.format(USER_ACTIVITY['ip'], i['timestamp'], i['page'], i['bytes'], i['code'])
        f = open("log.txt", "ab")
        f.write(TEMPLATE +"\r\n")
        f.close()

def create_fake_ip(): 
    IP = "{0}.{1}.{2}.{3}".format(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
    return IP

def create_fake_view(get_page=""):
    #print "Page: "+get_page
    if get_page != "":
        if get_page == "posts":
            get_page = WEBSITE_TEMPLATE[5][random.randint(0, len(WEBSITE_TEMPLATE[4])-1)]
            return get_page
        for i in WEBSITE_TEMPLATE:
            if type(i) == type([]):
                for p in i:
                    if p['page'] == get_page:
                        return p
            else:
                if i['page'] == get_page:
                    return i
    else:
        random_page = WEBSITE_TEMPLATE[random.randint(0, len(WEBSITE_TEMPLATE)-1)]
        if type(random_page) == type([]):
            random_page = random_page[random.randint(0, len(WEBSITE_TEMPLATE[5])-1)]
        #print "Not page: "+random_page['page']
        return random_page

def create_user_activity():
    pages = []
    tim = time.time()
    finished = []
    previous_page = create_fake_view()
    next_page = ""
    exit_num = 15
    exit = False

    while exit == False:
        #Get random number for the exit route or next route
        rand = random.randint(0, 100)
        if rand <= exit_num:
            exit = True
        else:
            #Create random user view
            if next_page == "":
                activity = create_fake_view()
                while previous_page == activity['page']:
                    activity = create_fake_view()
            else:
                activity = create_fake_view(next_page)
                while previous_page == activity['page']:
                    activity = create_fake_view(next_page)

            #Check if a post was accessed before the blog page was
            if "/blog" in activity['page'] and "blog/" not in finished:
                pass
            else:
                activity['timestamp'] = time.time() + int(numpy.random.normal(60.0, 60.0))
                finished.append(activity['page'])
                previous_page = activity['page']
                pages.append(activity)
                for i in RULES.keys():
                    if i == activity['page'] and "/blog" not in activity['page']:
                        for p in RULES[i].keys():
                            if rand < RULES[i][p] and previous_page != p:
                                next_page = p
                    else:
                        if i == "posts":
                            for p in RULES[i].keys():
                                if rand < RULES[i][p] and previous_page != p:
                                    next_page = p
    #print pages

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
    #print create_fake_view("blog/")
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