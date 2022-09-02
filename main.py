# Add module to syspath
import sys, os
curr_path = os.path.dirname(os.path.abspath(__file__))
<<<<<<< HEAD
=======

'''
# for Windows
sys.path.append(curr_path+'\\GUI')  # import GUI_path
sys.path.append(curr_path+'\\API')  # import API_path
'''
# for Linux
>>>>>>> 03553848b4a20d7aa6696fb0646125f755fabc07
sys.path.append(curr_path+'/GUI')  # import GUI_path
sys.path.append(curr_path+'/API')  # import API_path

from MainWindow import *

if __name__ == '__main__':
    getID()
    getUserListFromLocal()
    initIcon()
    main_window = MainWindow()
    #main_window.show()
    main_window.showMaximized()
    sys.exit(app.exec_())
