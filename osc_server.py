from liblo import *
import sys
import datetime
import time
import numpy as np
import pickle

# o means sad 1 means happys
mood = 0
max_val = 1500
beta = np.zeros((max_val, 4))
alpha = np.zeros((max_val, 4))
start_time = (datetime.datetime.now()).minute - 2.5
count_beta = 0
count_alpha = 0
file_counter = 0
flag_mood = "sad"
first_print = 1
class MuseServer(ServerThread):
    #listen for messages on port 5001
    def __init__(self):
        ServerThread.__init__(self, 5001)

    #receive alphaelrometer data
    # @make_method('/muse/alpha', 'fff')
    @make_method('/muse/elements/alpha_absolute', 'ffff')
    def alpha_callback(self, path, args):
        global alpha, count_alpha, first_print, count_beta
        alpha_x, alpha_y, alpha_z, alpha_a = args
        # alpha = np.append(alpha, temp_alpha)
        # print "%s %f %f %f" % (path, alpha_x, alpha_y, alpha_z)
        cur_time = (datetime.datetime.now()).minute
        print cur_time, start_time, count_alpha, count_beta
        if cur_time >= start_time + 2 and first_print == 1: 
            print "Started Recording the data"
            first_print = 0
        if cur_time >= start_time + 2:
            temp_alpha = np.array([alpha_x, alpha_y, alpha_z, alpha_a])
            alpha[count_alpha, :] = temp_alpha    
            print alpha
            count_alpha = count_alpha + 1
            if count_alpha == max_val - 1:
                # count_alpha = 0
                # count_beta = 0
                write_data_to_file()

    #receive beta data
    @make_method('/muse/elements/beta_absolute', 'ffff')
    # @make_method('/muse/beta', 'ffff')
    def beta_callback(self, path, args):
        global beta, count_beta
        l_ear, l_forehead, r_forehead, r_ear = args
        beta_x, beta_y, beta_z, beta_a = args
        cur_time = (datetime.datetime.now()).minute
        if cur_time >= start_time + 2:
            temp_beta = np.array([beta_x, beta_y, beta_z, beta_a])
            beta[count_beta, :] = temp_beta
            count_beta = count_beta + 1
        # print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)

    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        i = 0
        # print "UNKNOW MESSAGE"
  #       print "Unknown message \
		# \n\t Source: '%s' \
		# \n\t Address: '%s' \
		# \n\t Types: '%s ' \
		# \n\t Payload: '%s'" \
		# % (src.url, path, types, args)


#writing data such as beta and alpha to pickle file
def write_data_to_file():
    counts = 0
    global count_beta, count_alpha, file_counter, beta, alpha, flag_mood
    if count_beta <= count_alpha:
        counts = count_beta
    else:
        counts = count_alpha
    t = (beta[:counts,:], alpha[:counts,:], str(mood))
    with open('beta_' + str(file_counter) + '.pickle', 'wb') as params:
        p = pickle.Pickler(params)
        p.dump(t)
    file_counter = file_counter + 1
    count_alpha = 0
    count_beta = 0
    first_print = 1
    beta = np.zeros((max_val, 4))
    alpha = np.zeros((max_val, 4))
    start_time = (datetime.datetime.now()).minute + 2
    if flag_mood == "sad":
        print ("Now Change your mood to happy")
        flag_mood = "happy"
    else:
        print ("Now Change your mood to happy")
        flag_mood = "sad"


try:
    server = MuseServer()
except ServerError, err:
    print "INSIDE EXCCEPTIPN"
    print str(err)
    sys.exit()

server.start()

if __name__ == "__main__":
    while 1:
        time.sleep(1)
