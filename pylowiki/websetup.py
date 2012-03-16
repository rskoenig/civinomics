# -*- coding: utf-8 -*-
"""Setup the Pylowiki application"""
import logging, os

from pylons import config
from pylowiki.config.environment import load_environment
#from pylowiki.model import meta, commit, User, Page, Revision, Event, Points
from pylowiki.model import meta
from pylowiki.lib.db.user import User, getUserByEmail
from pylowiki.lib.db.event import Event
from pylowiki.lib.db.dbHelpers import commit


log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup ballestrini here"""
    load_environment(conf.global_conf, conf.local_conf)


    # If test.ini drop all existing tables
    filename = os.path.split(conf.filename)[-1]
    if filename == 'development.ini':    
        log.info("Dropping existing tables...")
        meta.metadata.drop_all(bind=meta.engine)

    #Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)

    
    # We are only working with this part of the config list
    conf = config['app_conf']

    """
    # if db is mysql, setup fulltext search.
    db = conf['sqlalchemy.url'].split(":")
    if db[0] == "mysql":
        meta.engine.execute("ALTER TABLE revision ADD FULLTEXT(data)")
    """

    # Try to create admin account and homepage
    try:

        #user, passwd, email = conf['admin.user'], conf['admin.pass'], conf['admin.email']
        # Edolfo
        firstName = conf['admin.firstName']
        lastName = conf['admin.lastName']
        email = conf['admin.email']
        passwd = conf['admin.pass']
        zipCode = conf['admin.zipCode']
        userName = "%s %s"%(firstName, lastName)

        if firstName != "" and lastName != "" and userName != "" and passwd != ""  and email != "" and zipCode != "":
        
            # Create the admin user
            u = User( email, firstName, lastName, passwd, zipCode )
            u = getUserByEmail(email)
            u['accessLevel'] = '300'
            u['activated'] = '1'
            u['disabled'] = '0'
            # Create event log entry
            e = Event("Create", "Auto create admin acct.", u)
            u['events'] = e.id
            log.info('hi!')
            commit(u)
            
            # Create home page
            #p = Page( "home" )
            # Create first revision
            #r = Revision ("This is your homepage, please edit this page as you like!")

            # relate the revision and event
            #r.event = e
            # append the event to the user
            #u.events.append( e )
            # append the event to the page
            #p.events.append( e )
            # append revision to the page
            #p.revisions.append( r )

            #commit( e )
            #try:
            #    p = Points(u.id)
            #    commit(p)
            #except:
            #    log.info('unable to create points object')

    except:

        pass

    

