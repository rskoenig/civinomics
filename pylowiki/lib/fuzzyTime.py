import datetime
import logging
log = logging.getLogger(__name__)

def ungettext(a,b,count):
    if count and count > 1:
        return b
    return a

def ugettext(a):
    return a

def timeSince(d, now=None):
    d = unicode(d)
    dList = d.split('.')
    d = dList[0]
    if now:
        now = unicode(now)
        nowList = now.split('.')
        now = nowList[0]
    
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    Adapted from http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    
    """

    """
    chunks = (
      (60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
      (60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
      (60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
      (60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
      (60 * 60, lambda n: ungettext('hour', 'hours', n)),
      (60, lambda n: ungettext('minute', 'minutes', n)),
    )
    """

    chunks = (
      (60 * 60 * 24 * 365, lambda n: ungettext('y', 'y', n)),
      (60 * 60 * 24 * 30, lambda n: ungettext('m', 'm', n)),
      (60 * 60 * 24 * 7, lambda n : ungettext('w', 'w', n)),
      (60 * 60 * 24, lambda n : ungettext('d', 'd', n)),
      (60 * 60, lambda n: ungettext('h', 'h', n)),
      (60, lambda n: ungettext('m', 'm', n)),
    )
    

    # Check for unicodeness
    if isinstance(d, unicode):
        d = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    if isinstance(now, unicode):
        now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        if d.tzinfo:
            now = datetime.datetime.now(LocalTimezone(d))
        else:
            now = datetime.datetime.now(None)

    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return u'0 ' + ugettext('seconds')
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = ugettext('%(number)d%(type)s') % {'number': count, 'type': name(count)}
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            s += ugettext(', %(number)d%(type)s') % {'number': count2, 'type': name2(count2)}
    if s == "0 minute":
        return "0 minutes"
    return s

def timeuntil(d, now=None):
    """
    Like timesince, but returns a string measuring the time until
    the given time.
    """
    if not now:
        now = datetime.datetime.now(utc if is_aware(d) else None)
    return timesince(now, d)

def timeUntil(d, now=None):
    if not now:
        now = datetime.datetime.now(None)
    return timeSince(now, d)
