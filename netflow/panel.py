from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.project import dashboard

class NetFlow(horizon.Panel):
	name = _("NetFlow")
	slug = 'netflow'

dashboard.Project.register(NetFlow)
