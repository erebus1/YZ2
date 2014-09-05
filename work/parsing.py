__author__ = 'user'
import urllib.request
import http.cookiejar
from socket import timeout
import time

class timeout_error(Exception): pass

class number_of_trains_convert_error(Exception): pass


class Tcarriage_type:
    typ = type(int)
    free_seats = type(int)
    price = type(float)
    sprice = type(str)
    empty = type(bool)


    def __init__(self):
        self.typ = 0
        self.free_seats = 0
        self.price = -1
        self.sprice = '-1'
        self.empty = False


    def print(self):
        print("     type = ", self.typ)
        print("     #free seats = ", self.free_seats)
        print("     price = ", self.sprice)
        print("     real price = ", self.price)
        print("     =========")


class Tcarriage:
    number = type(int)
    typ = type(str)
    free_seat = type(int)
    price = type(float)
    free_seats = []
    top = type(int)
    low = type(int)
    side_top = type(int)
    side_low = type(int)
    type_code = type(int)


    def print(self):
        print("     carriage number = ", self.number)
        print("     type = ", self.typ)
        print("     type code = ", self.type_code)
        # print("     type = ", self.typ)
        print("     #free seats = ", self.free_seat)
        print("     real price = ", self.price)
        print("     top = ", self.top)
        print("     low = ", self.low)
        print("     side top = ", self.side_top)
        print("     side low = ", self.side_low)
        print("     free seats:", self.free_seats)
        print("     =========")


    def __init__(self):
        self.number = -1
        self.free_seats = []
        self.price = -1
        self.free_seat = 0
        self.typ = ""
        self.low = 0
        self.side_top = 0
        self.side_low = 0
        self.type_code = 0


class Ttrain:
    number = type(str)
    departure = type(str)
    destination = type(str)
    depart_time = type(str)
    destination_time = type(str)
    on_way_time = type(str)
    code = type(str)
    carriages = []  #array of carriages
    carriage_num = type(int) #number of carriages

    def __init__(self):
        self.carriage_num = 0
        self.carriages = []
        self.number = ''
        self.departure = ''
        self.destination = ''
        self.depart_time = ''
        self.destination_time = ''
        self.on_way_time = ''
        self.code = ''


    def print(self):
        print("train number = ", self.number)
        print("point of departure = ", self.departure)
        print("point of destination = ", self.destination)
        print("time of depart = ", self.depart_time)
        print("time of destination=", self.destination_time)
        print("time in the way = ", self.on_way_time)
        # print("code = ", self.code)
        for i in range(0,self.carriage_num):
            self.carriages[i].print()
        print("================================")


def price_correct(price):
    price = price / 1.03 - 9
    price = round(price, 2)
    return price


def train_inf_from_code(train):
    code = train.code

    opener = urllib.request.build_opener()
    #send phpsessid in cookies
    opener.addheaders.append(('Cookie', phpsessid))
    #make link
    link = "http://dprc.gov.ua/trip-info.php?segment_id=" + code
    #get info
    try:
        s = opener.open(link, timeout = 10).read()
    except timeout:
        raise timeout_error()
    s = str(s, 'utf-8')
    # print(link)

    analyze_train_inf(s, train)


def analyze_train_inf(s, train):
    k1 = s.find('<tr id="wagon_')
    while k1>=0:
        carriage=Tcarriage()
        k1+=14
        k2 = s[k1:].find('"')
        k2+=k1
        carriage.number = s[k1:k2]
        s = s[k2:]

        #carriage type code
        k1 = s.find("wagon ct_")+9
        k2 = s[k1:].find("'")+k1
        carriage.type_code=int(s[k1:k2])

        #carriage type
        k1 = s.find("car_type'>")+10
        k2 = s[k1:].find("</")+k1
        carriage.typ = s[k1:k2]

        k1 = s.find("</td>")

        #top seats
        k1 = s[k1:].find("<td>")+k1+4
        k2 = s[k1:].find("</td>")+k1
        carriage.top = int(s[k1:k2])
        s = s[k2:]

        #low seats
        k1 = s.find("<td>")+4
        k2 = s[k1:].find("</td>")+k1
        carriage.low = int(s[k1:k2])
        s = s[k2:]

        #side top seats
        k1 = s.find("<td>")+4
        k2 = s[k1:].find("</td>")+k1
        carriage.side_top = int(s[k1:k2])
        s = s[k2:]

        #side low seats
        k1 = s.find("<td>")+4
        k2 = s[k1:].find("</td>")+k1
        carriage.side_low = int(s[k1:k2])
        s = s[k2:]

        #price
        k1 = s.find("'>")
        if k1>0:
            k1 += 2
            k2 = s[k1:].find("</td>")+k1
            carriage.price = price_correct(float(s[k1:k2].replace("&nbsp;", "")))


        train.carriage_num += 1
        train.carriages.append(carriage)
        k1 = s.find('<tr id="wagon_')


def train_code(train_number):
    k1 = s.find("window.trips_['" + str(train_number))
    k2 = s[k1 + 15:].find("'")
    train_number = int(s[k1 + 15:k1 + k2 + 15])
    k3 = s[k1 + k2 + 16:].find("guididx")
    k3 += k1 + k2 + 16
    k1 = s[k3:].find("'")
    k1 += k3 + 1
    k2 = s[k1:].find("'")
    k2 += k1
    return s[k1:k2]


def carriage_type_inf(c):
    carriage = Tcarriage_type()

    #type and is it empty
    k1 = c.find('"')
    k1 += 1
    k2 = c.find('">')
    header = c[k1:k2]
    if header.find('empty') > 0:
        carriage.empty = True
        free_seats = 0
    carriage.typ = int(header[header.find('c_') + 2:header.find('c_') + 6])


    #price
    k1 = c.find("price'>")
    k2 = c.find("<span")

    price = -1
    sprice = '-1'
    if (k1 > 0) and (k2 > 0):
        sprice = (c[k1 + 7:k2])

    sprice = sprice.replace("&nbsp;", " ")

    i = 0
    while (not sprice[i].isdigit()) and (sprice[i] != '-'):  #not use 'Ot' (find the place where digit begin)
        i += 1

    if sprice[i:] != '':  #if there is even one digit in price
        price = price_correct(float(sprice[i:]))


    carriage.price = price
    carriage.sprice = sprice


    #free seating
    k1 = c.find("'sts ")
    k2 = c.find("місц")
    if (k1 > 0) and (k2 > 0):
        cc = c[k1:k2 - 6]
        free_seats = int(cc[cc.find("'>") + 2:])

    carriage.free_seats = free_seats


    #print information
    if not carriage.empty:
        carriage.print()


def train_inf(curr_train):
    train = Ttrain()

    #point of beginning information about curr_train's train
    beg = s.find("row_" + str(curr_train))


    # all information about train in 'c'
    len = s[beg:].find("img src")
    c = s[beg:beg + len]

    #train name(number)
    k1 = c.find('info_row train first')
    k2 = c[k1:].find('</td>')
    k3 = c[k1 + 22:k2 + k1].find("'>")
    train.number = c[k1 + k3 + 24:k2 + k1]


    #point of train departure
    k1 = c.find('info_row name')
    k2 = c[k1:].find('</td>')
    train.departure = c[k1 + 15:k2 + k1]


    #point of train destination
    c = c[k2 + k1:]
    k1 = c.find('info_row name')
    k2 = c[k1:].find('</td>')
    train.destination = c[k1 + 15:k2 + k1]


    #time of depart
    c = c[k2 + k1:]
    k1 = c.find('info_row depart')
    k2 = c[k1:].find('</td>')
    c3 = c[k1 + 17:k2 + k1]
    train.depart_time = c3.replace('&nbsp;', '')


    # time on-the-way
    c = c[k2 + k1:]
    k1 = c.find('info_row onway')
    k2 = c[k1:].find('</td>')
    c4 = c[k1 + 16:k2 + k1]
    train.on_way_time = c4.replace('&nbsp;', '')


    #time of destination
    c = c[k2 + k1:]
    k1 = c.find('info_row arrive')
    k2 = c[k1:].find('</td>')
    c4 = c[k1 + 17:k2 + k1]
    train.destination_time = c4.replace('&nbsp;', '')


    #train code
    train.code = train_code(curr_train)


    #get numbers of carriages
    train_inf_from_code(train)

    #save information
    trains[curr_train] = train

    #print information
    # train.print()


    #carriage type information
    # while True:
    #     c = c[k2 + k1:]
    #     k1 = c.find('<td class="wagon_row')
    #     k2 = c[k1:].find('</td>')
    #     c5 = c[k1:k1 + k2]  #all information about carriage
    #     if c5 == '':
    #         break
    #     else:
    #         carriage_type_inf(c5)


def carriage_inf(curr_train, curr_carriage):
    carriage_num = trains[curr_train].carriages[curr_carriage].number #find carriage number
    link = "http://dprc.gov.ua/car_map.php?segment_id=" + trains[curr_train].code + "&car_id=" + carriage_num
    try:
        s = urllib.request.urlopen(link, timeout = 10).read()
    except timeout:
        raise timeout_error()

    s = str(s,'utf-8')
    # print(link)
    #create new carriage
    carriage = trains[curr_train].carriages[curr_carriage]
    #find all free seats
    carriage_inf_analyze(carriage,s)


def carriage_inf_analyze(carriage,s):
    #find first free seat
    k1 = s.find("free")
    if k1>=0:
        k1 += s[k1:].find("id='seat_")+9
    while k1>=0:
        #find number of seat
        k1 += s[k1:].find("'>")+2
        k2 = s[k1:].find("<")+k1
        #get number of free seat
        num = int(s[k1:k2])
        #put in array
        carriage.free_seat +=1
        carriage.free_seats.append(num)
        #try again
        s = s[k2:]
        k1 = s.find("free")
        if k1>=0:
            k1 += s[k1:].find("id='seat_")+9


def main(link):


    global s
#get all information in 's'

    #Create a CookieJar object to hold the cookies
    cj = http.cookiejar.CookieJar()
    #Create an opener to open pages using the http protocol and to process cookies.
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler())
    try:
    #create a request object to be used to get the page.
        s = opener.open(link, timeout=10).read()
    except timeout:
        raise timeout_error()

    s = str(s, 'utf-8')

#worck with cookies
    #get cookie
    for cookie in cj:
        cook = cookie
    #make str
    cook = str(cook)
    #find PHPSESSID info
    k1 = cook[9:].find(" ")
    global phpsessid
    phpsessid = cook[8:k1+9]


#number of trains
    k1 = s.find("всього знайдено")
    k2 = s[k1:].find(')')
    try:
        n = int(s[k1 + 16:k1 + k2])
    except:
        raise number_of_trains_convert_error

    # print(n)
    global trains
    trains = [Ttrain for i in range(0, n)]


#get all information about trains
    for i in range(0, n):
        train_inf(i)

#get all information about carriages
    for i in range(0, n):
        for j in range(0, trains[i].carriage_num):
            carriage_inf(i, j)

#print information
    # for i in range(0, n):
    #     trains[i].print()

    return trains #all data
