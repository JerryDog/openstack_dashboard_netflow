from django.utils.translation import ugettext_lazy as _

from horizon import tables
import logging
from django import template
LOG = logging.getLogger(__name__)

class MyFilterAction(tables.FilterAction):
	name = "myfilter"





def get_ips(instance):
    template_name = 'project/instances/_instance_ips.html'
    context = {"instance": instance}
    return template.loader.render_to_string(template_name, context)


class NetFlowTable(tables.DataTable):
	name = tables.Column("name", 
				link=("horizon:project:instances:detail"),
				verbose_name = _("Instance Name"))
	ipaddr = tables.Column(get_ips, verbose_name = _("Instance Ipaddress"))
	status = tables.Column("status",verbose_name = _("Instance Status"))
	graphs = tables.Column("graphs", 
				link=("horizon:project:netflow:graphsdetail"),
				verbose_name = _("Graphs"))

	class Meta:
		name = "netflow"
		verbose_name = _("DailyNetFlow")
		table_actions = (MyFilterAction,)

class TotalNetFlowTable(tables.DataTable):
	time = tables.Column("time", verbose_name = _("Month"))
	incount = tables.Column("incount", verbose_name = _("Total InNetFlow"))
	outcount = tables.Column("outcount", verbose_name = _("Total OutNetFlow"))
	inrate = tables.Column("inrate",
				link=("horizon:project:netflow:in"),
				verbose_name = _("Max Inrate"))
	inratedate = tables.Column("inratedate", verbose_name = _("Inrate Last Update"))
	outrate = tables.Column("outrate",
				link=("horizon:project:netflow:out"),
				verbose_name = _("Max Outrate"))
	outratedate =  tables.Column("outratedate", verbose_name = _("Outrate Last Update"))
	class Meta:
		name = "total"
		verbose_name = _("MonthlyNetFlow")

class InRateDetailTable(tables.DataTable):
	name = tables.Column("name",
                             #link=("horizon:project:instances:detail"),
                             verbose_name = _("Instance Name"))
        ipaddr = tables.Column("ipaddr", verbose_name = _("Instance Ipaddress"))
        status = tables.Column("status",verbose_name = _("Instance Status"))
        graphs = tables.Column("graphs",
                               link=("horizon:project:netflow:graphsdetailrate"),
                               verbose_name = _("Graphs"))

	rate = tables.Column("rate",verbose_name = _("Max Inrate"))
	     
	class Meta:
        	name = "inratedetail"
        	verbose_name = _("RateDetail")
        	table_actions = (MyFilterAction,)

class OutRateDetailTable(tables.DataTable):
        name = tables.Column("name",
                            # link=("horizon:project:instances:detail"),
                             verbose_name = _("Instance Name"))
        ipaddr = tables.Column("ipaddr", verbose_name = _("Instance Ipaddress"))
        status = tables.Column("status",verbose_name = _("Instance Status"))
        graphs = tables.Column("graphs",
                               link=("horizon:project:netflow:graphsdetailrate"),
                               verbose_name = _("Graphs"))

        rate = tables.Column("rate",verbose_name = _("Max Outrate"))

        class Meta:
                name = "outratedetail"
                verbose_name = _("RateDetail")
                table_actions = (MyFilterAction,)
