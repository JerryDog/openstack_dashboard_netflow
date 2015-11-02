#!/usr/bin/python

from sendmail4alarm import sendmail

sendmail('liujiahua@ztgame.com','127.0.0.1','test@ztgame.com','This is Subject','/usr/share/openstack-dashboard/openstack_dashboard/dashboards/admin/monitor/test.py','This is content')
