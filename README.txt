About Pylowiki
==================

.. contents:: Sections


Pylowiki's Primary Objective
=============================

 The original goal of *Pylowiki* was to create an advanced same page, section edit and preview, wiki solution.

 *Pylowiki* succeeded:

 * Browse and View articles.
 * Edit and Save changes on the same page.
 * Preview the result real-time and in place. See the page *before* submitting. 

 **Browse, Edit, Preview, and Submit from the same page!**


What does the name Pylowiki mean?
`````````````````````````````````

 The name *Pylowiki* is a portmanteau of the words *Pylons* and *wiki*.  To define Pylowiki we must first define *Pylons* and *wiki*.

 **def Pylons( pahy-lons ):**        
  Pylons is a lightweight python web framework emphasizing flexibility and rapid development.
        
  `. . . more about Pylons <http://pylonshq.com/>`_

 **def wiki( wik-ee ):**

    A collaborative website whose content can be edited by anyone who has access to it.

    `. . . more about wiki <http://en.wikipedia.org/wiki/Wiki>`_

 **def Pylowiki( pahy - loh - wik-ee ):**

    A wiki built using the Pylons framework.
    
    * Pylo wiki
    * Pile-O-wiki
    * Pile of wiki 
   

What mark-up does Pylowiki use?
````````````````````````````````

 Pylowiki uses `reStructured Text (reST) <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ as its wiki mark-up. 

How does Pylowiki render mark-up for real-time preview?
```````````````````````````````````````````````````````
 Pylowiki uses ajax to send reST mark-up to the web server.  The web server accepts reST and converts it to HTML.  The HTML is sent back to the browser and appears on the page in place and in real-time!


Why is real-time preview important?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Real-time preview of the users wiki mark-up is important because of the following reasons:

 * Users get feedback before they save changes.
 * Users do not have to leave the article to make a change, they may edit while the browse.
 * It is faster and leads to less consecutive edits by the same user.
 * Its fun and futuristic!


Installation and Setup
======================

#. Setup a working pylons virtualenv, review the pylons wiki to get started.

   http://pylonshq.com/docs/en/1.0/gettingstarted/

#. Acquire the Pylowiki source::

    hg clone ssh://hg@bitbucket.org/russellballestrini/pylowiki

#. Navigate to the pylowiki directory and create a config file as follows::

    paster make-config Pylowiki config.ini

#. Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

#. Test the install by running the dev paste server::

     paster serve --reload config.ini

#. Navigate a browser to http://127.0.0.1:5000
