"""

"""


def rules(alert, plugins):

    if alert.is_blackout():
        return [
            plugins['reject'],
            plugins['geoip'],
            plugins['blackout']
        ]
    else:
        if alert.severity in ['critical', 'major', 'ok']:
            return [
                plugins['reject'],
                plugins['transient'],
                plugins['geoip'],
                plugins['slack']
            ]
        else:
            return [
                plugins['reject'],
                plugins['transient'],
                plugins['geoip']
            ]
