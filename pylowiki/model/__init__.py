#from sqlalchemy import (MetaData, Table, Column, Integer, Unicode, DateTime,
from sqlalchemy import (Table, Column, Integer, Unicode, DateTime, BLOB, 
        ForeignKey, UnicodeText, and_, not_)
from sqlalchemy.orm import mapper, relationship, Session
from sqlalchemy.orm.collections import attribute_mapped_collection


from pylowiki.model import meta

import datetime as d

#metadata = MetaData()

def init_model(engine):
    meta.Session.configure(bind=engine)
    meta.engine = engine

"""Mapping a vertical table as a dictionary.

This example illustrates accessing and modifying a "vertical" (or
"properties", or pivoted) table via a dict-like interface.  These are tables
that store free-form object properties as rows instead of columns.  For
example, instead of::

  # A regular ("horizontal") table has columns for 'species' and 'size'
  Table('animal', metadata,
        Column('id', Integer, primary_key=True),
        Column('species', Unicode),
        Column('size', Unicode))

A vertical table models this as two tables: one table for the base or parent
entity, and another related table holding key/value pairs::

  Table('animal', metadata,
        Column('id', Integer, primary_key=True))

  # The properties table will have one row for a 'species' value, and
  # another row for the 'size' value.
  Table('properties', metadata
        Column('animal_id', Integer, ForeignKey('animal.id'),
               primary_key=True),
        Column('key', UnicodeText),
        Column('value', UnicodeText))

Because the key/value pairs in a vertical scheme are not fixed in advance,
accessing them like a Python dict can be very convenient.  The example below
can be used with many common vertical schemas as-is or with minor adaptations.

"""

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


# Here we have objects (things) and their properties (data)
t_thing = Table('thing', meta.metadata,
                Column('id', Integer, primary_key=True),
                Column('objType', Unicode(100)),
                Column('date', DateTime, default = d.datetime.now),
                Column('owner', Integer))

t_data = Table('data', meta.metadata,
              Column('thing_id', Integer, ForeignKey('thing.id'),
                     primary_key=True),
              Column('key', Unicode(100), primary_key=True),
              Column('value', UnicodeText, default=None),)

t_blob = Table('blobbicus', meta.metadata,
               Column('thing_id', Integer, ForeignKey('thing.id'), primary_key = True),
               Column('key', Unicode(100), primary_key=True),
               Column('value', BLOB, default = None))

class Blob(VerticalProperty):
    """ Used to store things like images, pdf files, etc... """

class Data(VerticalProperty):
    """thing properties"""

class Thing(VerticalPropertyDictMixin):
    """An object on the site.

    thing properties are available via the 'data' property or by using
    dict-like accessors on a Thing instance::

      cat['color'] = 'calico'
      # or, equivalently:
      cat.data['color'] = Data('color', 'calico')
    """

    _property_type = Data
    _property_mapping = 'data'

    def __init__(self, objType, owner = u'0'):
        self.objType = objType
        self.owner = owner

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.objType)


mapper(Thing, t_thing, properties={
    'data': relationship(
        Data, backref='thing',
        collection_class=attribute_mapped_collection('key')),
    'blob' : relationship(Blob, backref = 'thing', 
        collection_class=attribute_mapped_collection('key')),
    })
mapper(Data, t_data)
mapper(Blob, t_blob)