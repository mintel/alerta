
"""
Example routing rules to take advantage of the `BLACKOUT_NOTIFICATION` setting.

It is assumed that the default 'blackout' plugin is enabled and is at
the start of a list of plugins that do GeoIP lookup and forward the alert to . For example...

BLACKOUT_NOTIFICATION=True   # default=False
PLUGINS=['reject', 'blackout', 'geoip', 'slack', 'pagerduty']
"""


def rules(alert, plugins):

    # take account of blackout notify attribute value
    if alert.attributes['notify']:
        # notify=True, no blackout suppressions

        # => send critical and major to slack and pagerduty
        if alert.severity in ['critical', 'major', 'ok']:
            return plugins.values()

        # => send everything else to slack only
        else:
            return [plugins['geoip'], plugins['slack']]
    else:
        # notify=Fase, blackout is in place

        # => suppress downstream notifications, only run GeoIP lookup
        return [plugins['geoip']]
