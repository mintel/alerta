import logging

from alerta.exceptions import RateLimit
from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.transient')

FLAPPING_COUNT = 2
FLAPPING_WINDOW = 120  # seconds


class TransientAlert(PluginBase):

    def pre_receive(self, alert):

        LOG.info("Detecting transient alerts...")
        if alert.is_flapping(window=FLAPPING_WINDOW, count=FLAPPING_COUNT):
            alert.severity = 'indeterminate'
            alert.attributes['flapping'] = True
            # uncomment following line to stop alerts from being processed
            # raise RateLimit("Flapping alert received more than %s times in %s seconds" % (FLAPPING_COUNT, FLAPPING_WINDOW))
        else:
            alert.attributes['flapping'] = False

        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
