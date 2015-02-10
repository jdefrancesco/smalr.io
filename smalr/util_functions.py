##############################################################################################
# Author: in70x, MadHax
# Date:   9/28/13
# 
#
# Description: helper functions used in our fews
# 
#
# Last Updated: 9/28/13
# Copyright (c) smalr.io
###############################################################################################

import os
#import BeautifulSoup
import requests
import httplib

# Global Constants
HTTP_BAD_REQUEST = 400
HTTP_PREFIX = 'http://'
HTTPS_PREFIX = 'https://'

# Function to determine if a website is real and online
def is_page_alive(url):

    global HTTP_BAD_REQUEST

    r = httplib.HTTPConnection(url)
    r.request('HEAD', '')
    if r.getresponse().status < HTTP_BAD_REQUEST:
        return True # Page is alive
    else:
        return False # Page isn't alive


# Grabs the title from a website if one exists.
def grab_page_title():
    pass


# Detect valid HTTP prefix for links (i.e http or https) 
def url_prefix_check(url):

	if (url[:7] == 'http://') or (url[:8] == 'https://'):
		return True
	else:
		return False
