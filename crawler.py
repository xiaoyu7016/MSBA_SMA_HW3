# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 22:18:54 2016

Crawler for Edmunds.com

MSBA_SMA_Assignment 3

@author: Yuwen Wang
"""

from bs4 import BeautifulSoup
import requests
from lxml import html

url = "http://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans/p"
# url for entry level luxury performance sedan

def scrape_comments(start_page_num,end_page_num):
    """
    This function scrapes comments within the specified page range;
    Topic URL is globally defined    
    Specific to the Edmunds.com
    """
    comment_list = []
    
    for page_num in range(start_page_num,end_page_num+1): 
        ## Message the URL by appending page number
        web_page = requests.get(url+str(page_num)) 
        
        ## Create a BeautifulSoup object, a form to store the HTML documents
        BeautifulSoup_object = BeautifulSoup(web_page.content,"lxml")
    
        ## Locate the comments: <div class = "Message">
        comments_on_that_page = list(BeautifulSoup_object.find_all('div',class_='Message'))
        
        ## Collect the comments, unfold and append to a list
        for i in range(len(comments_on_that_page)):
            comment_list.append(comments_on_that_page[i])
        
        print (page_num) ## To make sure all is right
        
    return comment_list
        

entry_lux_300_671 = scrape_comments(300,302)
