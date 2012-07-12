"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm.collections import attribute_mapped_collection

# Functions used for querying/commiting to db
from dbHelpers import *

# Some additional imports
import datetime as d

# Logging
import logging
log = logging.getLogger(__name__)

class VerticalProperty(object):
    """A key/value pair.

    This class models rows in the vertical table.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<%s %r=%r>' % (self.__class__.__name__, self.key, self.value)
class VerticalPropertyDictMixin(object):
    """Adds obj[key] access to a mapped class.

    This is a mixin class.  It can be inherited from directly, or included
    with multiple inheritence.

    Classes using this mixin must define two class properties::

    _property_type:
      The mapped type of the vertical key/value pair instances.  Will be
      invoked with two positional arugments: key, value

    _property_mapping:
      A string, the name of the Python attribute holding a dict-based
      relationship of _property_type instances.

    Using the VerticalProperty class above as an example,::

      class MyObj(VerticalPropertyDictMixin):
          _property_type = VerticalProperty
          _property_mapping = 'props'

      mapper(MyObj, sometable, properties={
        'props': relationship(VerticalProperty,
                          collection_class=attribute_mapped_collection('key'))})

    Dict-like access to MyObj is proxied through to the 'props' relationship::

      myobj['key'] = 'value'
      # ...is shorthand for:
      myobj.props['key'] = VerticalProperty('key', 'value')

      myobj['key'] = 'updated value']
      # ...is shorthand for:
      myobj.props['key'].value = 'updated value'

      print myobj['key']
      # ...is shorthand for:
      print myobj.props['key'].value

    """

    _property_type = VerticalProperty
    _property_mapping = None

    __map = property(lambda self: getattr(self, self._property_mapping))

    def __getitem__(self, key):
        return self.__map[key].value

    def __setitem__(self, key, value):
        property = self.__map.get(key, None)
        if property is None:
            self.__map[key] = self._property_type(key, value)
        else:
            property.value = value

    def __delitem__(self, key):
        del self.__map[key]

    def __contains__(self, key):
        return key in self.__map

    # Implement other dict methods to taste.  Here are some examples:
    def keys(self):
        return self.__map.keys()

    def values(self):
        return [prop.value for prop in self.__map.values()]

    def items(self):
        return [(key, prop.value) for key, prop in self.__map.items()]

    def __iter__(self):
        return iter(self.keys())



t_thing = sa.Table( 'thing', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('objType', sa.types.Unicode(100)),
    sa.Column('date', sa.types.DateTime, default = d.datetime.now),
    sa.Column('owner', sa.types.Unicode(100), default = 0),
    mysql_charset = 'utf8'
)

t_data = sa.Table( 'data', meta.metadata,
    sa.Column('thing_id', sa.types.Integer, sa.ForeignKey('thing.id'), primary_key = True),
    sa.Column('key', sa.types.Unicode(100), primary_key = True),
    sa.Column('value', sa.types.UnicodeText, default = None),
    mysql_charset = 'utf8'
)

class Data(VerticalProperty):
    """ The data class """

class Thing(VerticalPropertyDictMixin):
    """
        A thing - some object that requires persistence.

        thing properties are available via the 'data' property, or by using dict-like
        accessors on a Thing instance:

        user['name'] = 'edolfo'
        # Or:
        user.name = Data('name', 'edolfo')
    """
    _property_type = Data
    _property_mapping = 'data'

    def __init__(self, objType, owner = '0'):
        log.info('objType = %s, owner = %s' %(objType, owner))
        self.objType = objType
        log.info('just set the object type')
        self.owner = owner
        log.info('Just set the owner')

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)

    def __getattr__(self, attr):
        return self.__dict__.get(attr)

orm.mapper(Thing, t_thing, 
properties = {
    'data' : orm.relation(Data, backref = 'thing', collection_class = attribute_mapped_collection('key')),
})
orm.mapper(Data, t_data)
    
def getThingByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
