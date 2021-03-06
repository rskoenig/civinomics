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
    if filename == 'developmentTodd.ini':    
        log.info("Dropping existing tables...")
        meta.metadata.drop_all(bind=meta.engine)
        

    #Create the tables if they don't already exist
    if filename != 'testToddNoReset.ini':    
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
        name = conf['admin.name']
        email = conf['admin.email']
        passwd = conf['admin.pass']
        postalCode = conf['admin.postalCode']
        country = 'United States'
        memberType = 'professional'
        log.info('Aaaaaaaaaaaaaaaaa FILENAME IS %s', filename)
        if name != "" and passwd != ""  and email != "" and postalCode != "":
            if filename != 'developmentMaria.ini':
                # Create the admin user
                u = User( email, name, passwd, country, memberType, postalCode )
                u = getUserByEmail(email)
                u['accessLevel'] = '300'
                u['activated'] = '1'
                u['disabled'] = '0'
                # Create event log entry
                e = Event("Create", "Auto create admin acct.", u, u)
                log.info('hi!')
                commit(u)

    except:
        raise
        pass

    

