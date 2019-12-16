import sys, bs4, os, tempfile
import constants
import logging

def parseArguments():
    import argparse
    from argparse import RawDescriptionHelpFormatter
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Parses html files, looks for img tags and replaces them with a structure suitable for both mobi and non-mobi kindle files. <img> has to have attribute style with css width specified (in percent). Width percentage is used to specify percentage of width of image on non-mobi devices and as a width percentage in pixels calculation for mobi devices.", formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("cssfile", help="Specify css file to add css classes to.", type=argparse.FileType(mode='rt', encoding='utf-8'))
    parser.add_argument("content", help="Name of the file or directory of files containing html to parse")
    parser.add_argument("-sw", "--screen-width", help="Screen width in pixels to use for calculations in mobi classes. Default value is 768.", type=int, default=768)
    parser.add_argument("-sh", "--screen-height", help="Screen height in pixels to use for calculations in mobi classes. Default value is 1024.", type=int, default=1024)
    return parser.parse_args()

def processFiles(files, screen_height, screen_width):
    for f in files:
        logging.info("Processing file {}".format(f))
        # reformatImageLayout(wdir, fname)    # put div/img formatting into a standard single format
        # dualFormatHTMLImages(wdir, fname)   # dual format html <img> images for Kindle KF7 and KF8 devices

def addMediaToCSS(cssref):  
    """ Adds the appropriate media queries to
        the css to control KF7/KF8 ebook image 
        displays    
    """
    css_needs_updating = False

    with cssref as cssfile:
        cssfile_content = cssfile.read()
        cssfile_lastline = cssfile_content.splitlines()[-1]
        logging.debug("Stylesheet last line is:\n{0}".format(cssfile_lastline))
    
    # Check if css file needs updating
    if cssfile_lastline != constants.MAGIC_STRING:
        css_needs_updating = True
    if not css_needs_updating:
        logging.debug("Media queries already exist in a stylesheet")
        return

    logging.info("Add media queries to stylesheet...")
    # Open temp file for writing
    css_dirname, css_basename = os.path.split(cssref.name)
    temp_cssfile = tempfile.NamedTemporaryFile(mode='wt', encoding='utf-8', delete=False, dir=css_dirname, prefix=css_basename + '.')
    with temp_cssfile:
        logging.debug("Creating temp css file: {0}".format(temp_cssfile.name))
        temp_cssfile.write(cssfile_content)
        logging.debug("Writing original css content to temp file.")
        data = '\n'
        data += '/* Media queries for image setting */\n'
        data += '@media amzn-mobi {\n'
        data += "    .{0} {{\n".format(constants.NON_MOBI_CLASS_NAME)
        data += '        display: none;\n' 
        data += '    }\n'
        data += '    .{0} {{\n'.format(constants.MOBI_CLASS_NAME)
        data += '        display: inline;\n' 
        data += '    }\n'     
        data += '}\n'       
        data += '@media not amzn-mobi {\n'
        data += '    .{0} {{\n'.format(constants.NON_MOBI_CLASS_NAME)
        data += '        display: inline;\n' 
        data += '    }\n'
        data += '    .{0} {{\n'.format(constants.MOBI_CLASS_NAME)
        data += '        display: none;\n' 
        data += '    }\n'     
        data += '}\n'            
        data += constants.MAGIC_STRING + '\n'
        temp_cssfile.write(data)
        logging.debug("Writing new css content to temp file.")
    os.replace(temp_cssfile.name, cssref.name)
    logging.debug("Replacing original stylesheet file with temp one.")

            
def getContentFiles(content_str):
    if not os.path.exists(content_str):
        logging.error("Content does not exist.")
        sys.exit()
    
    if os.path.isfile(content_str):
        return [content_str]

    if os.path.isdir(content_str):        
        filelist = []
        for root, dirs, files in os.walk(content_str):         
            for d in reversed(dirs):
                if d.startswith('.'):
                    del dirs[dirs.index(d)]
            for filename in files:
                if not filename.startswith('.') and filename.endswith('.xhtml'):
                    filelist.append(os.path.join(root, filename))

        return filelist
        

def parseHTML(fileHandle):
    with fileHandle as file:
        soup = bs4.BeautifulSoup(file.read(), "html.parser")
    return soup

def findIMG(html_soup):
    return html_soup.find_all("img")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(format='-- %(levelname)s: %(message)s', level=logging.DEBUG)

    # Guard against Py2
    if sys.version_info[0] == 2:
        logging.error("Need to use Python 3")
        sys.exit()
    
    # Program initialization
    args = parseArguments()
    logging.debug("Command line arguments: {}".format(args))
    
    # Verify that content is a valid file or directory of files.
    content_files = getContentFiles(args.content)
    if len(content_files) < 1:
        logging.error("No files found suitable for processing.")
        sys.exit()
    
    # Start file processing
    logging.debug("Content files to process {}".format(content_files))
    processFiles(content_files, args.screen_height, args.screen_width)
    
    # Add media classes to css file
    addMediaToCSS(args.cssfile)


    #soup = parse_html(args.filename)
    #addCaptions = args.captions
    #list_of_img = find_img(soup)
    #print(type(list_of_img))



    