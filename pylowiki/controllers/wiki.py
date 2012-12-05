# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.utils import urlify

#fox added following imports
#from pylowiki.model import commit_edit, get_page, get_all_pages
from pylowiki.lib.db.page import get_page, get_all_pages, getPageByID
from pylowiki.lib.db.workshop import getWorkshopByCode
from pylowiki.lib.db.revision import Revision
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.user import isAdmin
from pylowiki.lib.db.facilitator import isFacilitator

import pylowiki.lib.helpers as h
import re

log = logging.getLogger(__name__)

class WikiController(BaseController):

    def index(self, id):
        """ Loads view or section edit page data for URL/ID depending on login status """
        
        c.p = get_page(id)
        if c.p == False: # Error page not found
            abort(404, h.literal("This page does not exist! Would you like to <a href='/create/assist/" + id + "'> Create it?</a>") )
        
        c.title = c.p.url
        c.url = c.p.url 
    
        r = c.p.revisions[0]

        c.lastmoddate = r.event.date
        c.lastmoduser = r.event.user.name

        if session.get('user'): # if use in session load wiki logic else just view the page
            reST = r.data

            reSTlist = self.get_reSTlist(reST) # function below
            HTMLlist = self.get_HTMLlist(reST) # function below 

            #print "HTML rows " + str(len( HTMLlist ))
            #print "reST rows " + str(len( reSTlist ))
        
            c.wikilist = zip ( HTMLlist, reSTlist ) # link the lists (a list of lists) 
            return render( '/derived/wiki.mako' )
        else:
            c.content = h.literal(h.reST2HTML(r.data))
            return render('/derived/view.mako')

    def readThisArticle(self):
        readArticle(c.authuser.id)
        numPoints = c.authuser.pointsObj.points
        if numPoints % 10 == 0:
            h.flash('Congratulations on winning the %d points award!' % numPoints)
        return redirect('/' + c.url) 
    
    def random( self ):
        import random   
        pagelist = get_all_pages()
        pagelistlen = len( pagelist ) - 1
        rand = random.randint(0, pagelistlen)
        pageurl = pagelist[rand].url
        redirect( "/" + pageurl )
        

    @h.login_required   
    def handler(self, id1, id2):
        """ Handles wiki Submit """
        code = id1
        url = id2

        w = getWorkshopByCode(code)
        session['confTab'] = "tab5"
        alert = {'type':'success'}
        alert['title'] = 'Background Information Updated.'
        session['alert'] = alert
        session.save()
        if not w:
            h.flash('Workshop not found', 'error')
            return redirect('/')

        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, w.id)): 
            
            try:

                request.params['submit'] #Try submit, if false redirect back.
                data = remark = ""
                for i in range( 0, int(request.params['count'])): # Get all the textarea content, append to data
                    data = data + request.params['textarea'+str(i)]
                    if request.params.get('remark'+str(i)) is None:
                        pass # Do nothing
                    else:
                        remark = remark + request.params.get('remark'+str(i))
                
                page = getPageByID(w['page_id'])
                r = Revision(c.authuser, data, page)
                w['mainRevision_id'] = r.r.id
                commit(w)
            
            except KeyError: 
                h.flash( "Do not access a handler directly", "error" )
            
            if 'configure' in request.params:
                return redirect( "/workshop/%s/%s/configure" %(code, url) )
            else:
                return redirect( "/workshop/%s/%s/background" %(code, url) )
        else:
            return redirect( "/workshop/%s/%s" %(code, url) )
    
    @h.login_required
    def previewer( self, id ):
        """ AJAX Handler - Accepts reST returns HTML """
        try:
            preview = h.literal(h.reST2HTML(request.params['data']))
        except:
            preview = "There is a problem with your syntax, please fix to save your comment/edits."
        return preview


# ------------------------------------------
#    Helper functions for wiki controller
#-------------------------------------------

    @h.login_required
    def CleanList( self, l ):
        """ Remove all empty rows from list """
        counter = 0
        length = len( l )
        while counter < length:
            if l[counter].isspace() or l[counter] == None or l[counter] == "":
                del l[counter]
                length = len( l )   
            counter += 1
        return l


    @h.login_required
    def isodd( self, integer ):
        """ if interger is odd return True, else return False"""
        if integer % 2 == 0:
            return False
        else:
            return True


    @h.login_required
    def get_reSTlist( self, reST ):
        """Accept a reST string and return a list of sections
        This code is a bit ugly but it works... 
        SORRY IF YOU HAVE TO WORK ON THIS..."""

        splitter = re.compile('(.*\r\n[=\-`:~^_*+#]{3,}.+\r\n+)') # Create regex object that splits reST string by headings
        reSTlist = self.CleanList(splitter.split( reST )) # Split the reST into a list, and remove any empty rows
        
        """reSTlist has heading and section data in seperate rows.
        The logic below merges the heading and section data rows."""
        
        lenght = len( reSTlist )
        
        if self.isodd( lenght ): # if the lenght is odd, the first row doesn't have a heading and will be in its own section
            offset = counter = 1
        else:
            offset = counter = 0

        """ join the heading list row with the data list row """
        while counter < lenght: # loop through list until end
            if self.isodd( counter + offset ): # do nothing if even
                reSTlist[counter-1] = reSTlist[counter-1] + reSTlist[counter]
                reSTlist[counter] = "" # set current row to empty
            counter = counter + 1

        return self.CleanList( reSTlist ) # remove empty rows and return list


    @h.login_required
    def get_HTMLlist( self, reST):
        """Accept reST list, convert to html, remove newlines so regex works, split HTML into a list by heading."""

        splitter = re.compile('(<div class\="section".*?)(?=<div class\="section")', re.DOTALL) # Create regex object to split HTML by header section.
        HTMLlist = self.CleanList(splitter.split(h.literal(h.reST2HTML( reST ))))
        
        if len(HTMLlist) == 1: # This only happens if there are two sections but only one heading
            splitter = re.compile('(<div class\="section".*</div>)', re.DOTALL) # Create regex object to split HTML by header section.
            HTMLlist = self.CleanList(splitter.split(h.literal(h.reST2HTML( reST ))))      
    
        return HTMLlist

            
        
