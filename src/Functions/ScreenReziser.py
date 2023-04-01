from PyQt5.QtWidgets import QApplication

'''
    This function is used to resize the GUI based on the screen resolution.
'''
def gui_scale():    

    screen = QApplication.screens()[0]
    dpi = screen.logicalDotsPerInch()
    return int(dpi / 96)