LCYAN = '\033[96m'
WHITE = '\033[37;1m'
ENDC = '\033[0m'

def print_format_table(): 
    """ 
    prints table of formatted text format options 
    """
    for style in range(8): 
        for fg in range(30, 38): 
            s1 = '' 
            for bg in range(40, 48): 
                format = ';'.join([str(style), str(fg), str(bg)]) 
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format) 
            print(s1) 
        print('\n') 
  
#print_format_table() 