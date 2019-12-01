import sys, bs4, os
import constants

def parse_arguments():
    import argparse
    from argparse import RawDescriptionHelpFormatter
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Parses html files, looks for img tags and replaces them with a structure suitable for both mobi and non-mobi kindle files. <img> has to have attribute style with css width specified (in percent). Width percentage is used to specify percentage of width of image on non-mobi devices and as a width percentage in pixels calculation for mobi devices.", formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("cssfile", help="Specify css file to add css classes to.", type=argparse.FileType(mode='rt+', encoding='utf-8'))
    parser.add_argument("content", help="Name of the file or directory of files containing html to parse")
    parser.add_argument("-sw", "--screen-width", help="Screen width in pixels to use for calculations in mobi classes. Default value is 768.", type=int, default=768)
    parser.add_argument("-sh", "--screen-height", help="Screen height in pixels to use for calculations in mobi classes. Default value is 1024.", type=int, default=1024)
    return parser.parse_args()

def add_media_to_CSS(cssref):  
    """ Adds the appropriate media queries to
        the css to control KF7/KF8 ebook image 
        displays    
    """
    with cssref as cssfile:
        lastline = cssfile.read().splitlines()[-1]
        # Check for 'magic' line, before adding media queries
        if lastline != constants.MAGIC_STRING:
            print('\n -- Add media queries to stylesheet...')
            data = '\n'
            data += '\n/* Media queries for image setting */\n'
            data += '@media amzn-mobi {\n'
            data += ' .kf8only {\n'
            data += '  display: none;\n' 
            data += '  }\n'
            data += ' .mobionly {\n'
            data += '  display: inline;\n' 
            data += '  }\n'     
            data += '}\n'       

            data += '@media not amzn-mobi {\n'
            data += ' .kf8only {\n'
            data += '  display: inline;\n' 
            data += '  }\n'
            data += ' .mobionly {\n'
            data += '  display: none;\n' 
            data += '  }\n'     
            data += '}\n'            
            data += constants.MAGIC_STRING + '\n'
            cssfile.write(data)
            
def getFilesToFix(content):
    if not os.path.exists(content):
        print ('Content does not exist.\n')
        sys.exit()
    
    if os.path.isfile(content):
        return [content]

    if os.path.isdir(content):        
        dirlist = []
        for root, dirs, files in os.walk(content):         
            for d in reversed(dirs):
                if d.startswith('.'):
                    del dirs[dirs.index(d)]
            for filename in files:
                if not filename.startswith('.') and filename.endswith('.xhtml'):
                    dirlist.append(os.path.join(root, filename))

        return dirlist
        

def parse_html(fileHandle):
    with fileHandle as file:
        soup = bs4.BeautifulSoup(file.read(), "html.parser")
    return soup

def find_img(html_soup):
    return html_soup.find_all("img")

if __name__ == "__main__":

    # Guard against Py2
    if sys.version_info[0] == 2:
        print("Need to use Python 3")
        sys.exit()
    # Program initialization
    args = parse_arguments()
    
    # Verify content is a valid file or directory of files.
    print(getFilesToFix(args.content))
    # Add media classes to css file
    add_media_to_CSS(args.cssfile)

    #soup = parse_html(args.filename)
    #addCaptions = args.captions
    #list_of_img = find_img(soup)
    #print(type(list_of_img))



    