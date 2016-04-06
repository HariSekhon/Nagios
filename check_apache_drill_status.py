#!/usr/bin/env python
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2016-02-18 18:44:59 +0000 (Thu, 18 Feb 2016)
#
#  https://github.com/harisekhon/nagios-plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback # pylint: disable=line-too-long
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Nagios Plugin to check Apache Drill's status page

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import logging
import os
import re
import sys
import traceback
try:
    from bs4 import BeautifulSoup
except ImportError:
    print(traceback.format_exc(), end='')
    sys.exit(4)
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pylib'))
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import log, qquit
    from harisekhon.utils import support_msg
    from harisekhon import StatusNagiosPlugin
    from harisekhon import RequestHandler
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.2'


class CheckApacheDrillStatus(StatusNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckApacheDrillStatus, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = 'Apache Drill'
        self.default_port = 8047

    def get_status(self):
        url = 'http://{0}:{1}/status'.format(self.host, self.port)
        req = RequestHandler().get(url)
        status = self.parse(req)
        return status

    def parse(self, req):
        soup = BeautifulSoup(req.content, 'html.parser')
        # if log.isEnabledFor(logging.DEBUG):
        #     log.debug("BeautifulSoup prettified:\n%s\n%s", soup.prettify(), '='*80)
        status = None
        try:
            status = soup.find('div', {'class': 'alert alert-success'}).get_text().strip()
        except (AttributeError, TypeError):
            qquit('UNKNOWN', 'failed to parse Apache Drill status page. %s' % support_msg())
        if re.match('Running!', status):
            self.ok()
        else:
            self.critical()
        return status


if __name__ == '__main__':
    CheckApacheDrillStatus().main()
