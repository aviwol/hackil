import random
import time
import numpy

WEBSITE_TEMPLATE = (
    {'page': 'index.html','bytes': 1058, 'code': 200},
    {'page': 'contact.html', 'bytes': 1029, 'code': 200},
    {'page': 'about.html', 'bytes': 954, 'code': 200},
    {'page': 'career.html', 'bytes': 699, 'code': 200},
    {'page': 'blog/', 'bytes': 999, 'code': 200},
    [
        {'page': '/blog/post1.html', 'bytes': 628, 'code': 200}, 
        {'page': '/blog/post2.html', 'bytes': 456, 'code': 200}, 
        {'page': '/blog/post3.html', 'bytes': 852, 'code': 200}, 
        {'page': '/blog/post4.html', 'bytes': 349, 'code': 200}, 
        {'page': '/blog/post5.html', 'bytes': 222, 'code': 200}, 
        {'page': '/blog/post6.html', 'bytes': 897, 'code': 200}, 
        {'page': '/blog/post7.html', 'bytes': 623, 'code': 200}, 
        {'page': '/blog/post8.html', 'bytes': 864, 'code': 200}, 
        {'page': '/blog/post9.html', 'bytes': 371, 'code': 200}, 
        {'page': '/blog/post10.html', 'bytes': 128, 'code': 200}
    ]
)

RULES = {
    'start':(['index.html','about.html','contact.html'],[60,90,100]),# {'index.html': 60,'about.html': 90,'contact.html': 100},
    'index.html':(['index.html','about.html','contact.html', 'blog/'],[40,60,80,100]), #{'about.html': 20, 'contact.html': 40, 'career.html': 60, 'blog.html': 80},
    'about.html':(['index.html','career.html','contact.html'],[40,60,100]), #{'index.html': 20, 'contact.html': 20, 'career.html': 20}, 
    'contact.html':(['index.html','about.html','career.html'],[30,60,100]), #{'about.html': 40, 'career.html': 80}, 
    'blog/':(['index.html','posts'],[50,100]), #{'index.html': 30, 'posts': 80}, 
    'career.html':(['index.html','about.html'],[40,100]), #{'index.html': 40, 'about.html': 80}, 
    'posts': (['index.html','posts'],[40,100])#{'index.html': 20, 'posts': 50}#, 'blog/': 80}
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

def get_page(page):
    probs=RULES[page][1]
    new_pages=RULES[page][0]
    rand=random.randint(0,99)
    new_page=''
    for i in range(len(probs)):
        if rand<probs[i] and new_pages[i] != page:
            new_page=new_pages[i]
    return new_page      


def create_user_activity():
    pages = []
    finished = []
    previous_page = "start"
    next_page = ""
    exit_num = 20
    exit = False
    timer = time.time()

    while exit == False:
        #Get random number for the exit route or next route
        rand = random.randint(0, 100)
        if rand <= exit_num:
            exit = True
        else:
            #Create random user view
            current_page=get_page(previous_page)
            previous_page = current_page
            detailed_page = create_fake_view(current_page)
            timer += int(numpy.random.normal(60.0,60.0))
            detailed_page['timestamp'] = timer
            pages.append(detailed_page)
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
    for i in range(0, 10):
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

