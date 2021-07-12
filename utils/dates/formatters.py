import datetime
import time

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def combine_timetuple_and_zone(timetuple, zone):
    # An expected date format according to
    # RFC is Mon, 12 Jul 2021 15:47:08 GMT

    # Some values in the timetuple are numbers
    # and need to be converted to their actual
    # string value representation
    day_as_string = DAYS[timetuple.tm_wday]
    month_as_string = MONTHS[timetuple.tm_mon - 1]
    return (
        f'{day_as_string}, {timetuple.tm_mday} '
        f'{month_as_string} {timetuple.tm_year} {timetuple.tm_hour}:'
        f'{timetuple.tm_min}:{timetuple.tm_sec} {zone}'
    )


def format_datetime_object(instance: datetime.datetime, use_gmt: bool = False):
    # This creates a structured tuple that we
    # can them use to format with GTM parameter
    timetuple = instance.timetuple()

    zone = instance.strftime('%z')
    # If we have to use GMT then make sure
    # tz_info present in the tuple
    if use_gmt:
        logic = any([
            timetuple.tz_info is None,
            timetuple.tz_info != datetime.timezone.utc
        ])

        if not logic:
            raise ValueError('In order to use GMT, UTC needs to be set in the')
        zone = 'GMT'
    
    if instance.tzinfo is None:
        zone = '-0000'
    return combine_timetuple_and_zone(timetuple, zone)


def formatdate(timevalue: float = None, use_local_time: bool = False, use_gmt: bool = False):
    """
    Get an RFC compliant date that respects section xxx in such
    as the value respects the given example 
    Mon, 12 Jul 2021 15:47:08 GMT

    Parameters
    ----------

        - timevalue (float, optional): time in seconds. Defaults to None.
        - use_local_time (bool, optional): whether to use local time. Defaults to False.
        - use_gmt (bool, optional): whether to use GMT. Defaults to False.

    Returns
    -------

        str: an RFC compliant date string
    """
    timevalue = timevalue or time.time()
    
    result = datetime.datetime.utcfromtimestamp(timevalue)
    if use_local_time or use_gmt:
        result = datetime.datetime.fromtimestamp(timevalue, datetime.timezone.utc)

    if use_local_time:
        use_gmt = False
        result = result.astimezone()
    return format_datetime_object(result, use_gmt=use_gmt)
