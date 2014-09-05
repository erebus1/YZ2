__author__ = 'user'
import parsing
import time

def check(trains):
    number_of_trains = len(trains)
    sum = 0
    for i in range(0, number_of_trains): #see all trains
        if trains[i].number.find("072")>=0: #find 72'th train
            for j in range(0,trains[i].carriage_num): #see all carriages of 72'th train
                if ((trains[i].carriages[j].price<140) and (trains[i].carriages[j].free_seat>0)): #if the price lower then 140 hrn and not empty carriage
                    for k in range(0,trains[i].carriages[j].free_seat): # see all free seats in carriage
                        if (trains[i].carriages[j].free_seats[k]<=35) and (trains[i].carriages[j].free_seats[k] % 2 == 1): #calc sum of
                            sum += 1                                                         #bottom not side seats


    global previous_sum #previous number of good seats
    if (sum>0) and (sum != previous_sum): #if number of good seats>0 and not equal previous number of free good seats
        import mail2
        msg = "find "+str(sum)+" free bottom good seats" #make message
        msg = msg.encode('ascii')
        mail2.mail(msg) #mail message to mobile
    previous_sum = sum #save number of free good seats
    print(sum)


def do_it(link):
    global previous_sum
    previous_sum = -1
    while True:
        try:
            trains = parsing.main(link) #get all information about all trains
            check(trains); #choose good seats
        except parsing.timeout_error:
            print("timeout_error")
        except parsing.number_of_trains_convert_error:
            print("maybe service does not work")
        except ValueError:
            print("Value Error")
        except:
            print("unexpected error")
        time.sleep(300) #wait



do_it("http://dprc.gov.ua/show.php?transport_type=2&src=22210800&dst=22200001&dt=2014-03-11&ret_dt=2001-01-01&ps=ec_privat")

