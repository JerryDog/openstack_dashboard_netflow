js and css put in /usr/share/openstack-dashboard/static/dashboard/(js/css)


dir "netflow" put in /usr/share/openstack-dashboard/openstack_dashboard/dashboards/project
and register in dashboard.py

add django.po.netflow to /usr/share/openstack-dashboard/openstack_dashboard/locale/zh_CN/LC_MESSAGES/django.po and 
exec command "msgfmt --statistics --verbose -o django.mo django.po"
