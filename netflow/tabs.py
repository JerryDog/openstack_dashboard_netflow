from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.project.netflow import tables


class NetFlowTab(tabs.TableTab):
    name = _("NetFlow Tab")
    slug = "netflow_tab"
    table_classes = (tables.NetFlowTable,)
    #template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_monitor_data(self):
        try:
            marker = self.request.GET.get(
                        tables.NetFlowTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class NetFlowTabs(tabs.TabGroup):
    slug = "netflow_tabs"
    tabs = (NetFlowTab,)
    sticky = True


class GraphsTab(tabs.Tab):
    name = _("Graphs")
    slug = "graphs"
    template_name = "project/netflow/_graphs.html"

    def get_context_data(self, request):
	return {"meters": self.tab_group.kwargs['meters']}

class GraphsDetailTabs(tabs.TabGroup):
    slug = "graphs_details"
    tabs = (GraphsTab,)
    sticky = True

class GraphsRateTab(tabs.Tab):
    name = _("Graphs")
    slug = "graphsrate"
    template_name = "project/netflow/_graphs_rate.html"
    
    def get_context_data(self, request):
        return {"meters": self.tab_group.kwargs['meters']}

class GraphsDetailRateTabs(tabs.TabGroup):
    slug = "graphs_details_rate"
    tabs = (GraphsRateTab,)
    sticky = True
