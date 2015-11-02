from __future__ import division

class NetFlowTotal(object):
	def __init__(self,result):
		#self.time,self.incount,self.outcount,self.inrate,self.inratedate,self.outrate,self.outratedate = result
		self.time,self._incount,self._outcount,self._inrate,self.inratedate,self._outrate,self.outratedate = result
		#self.id = '%s;%s;%s' % (self.time, self.projectid, self.region)
		self.id = self.time
	def unitTrans4Flow(self,value):
		if float(value) < 1024:
			unit = 'B'
			result = value
		if 1024 <= float(value) < 1048576:
			unit = 'KB'
			result = round( float(value)/1024, 2 )
		if 1048576 <= float(value) < 1073741824:
			unit = 'MB'
			result = round( float(value)/1048576, 2 )
		if float(value) >= 1073741824:
			unit = 'GB'
			result = round( float(value)/1073741824, 2 )
	
		r = '%s %s' % (result, unit)
		return r

        def unitTrans4Rate(self,value):
                if float(value)*8 < 1024:
                        unit = 'bps'
                        result = round( float(value)*8, 2 ) 
                if 1024 <= float(value)*8 < 1048576:
                        unit = 'Kbps'
                        result = round( float(value)/1024 * 8, 2 )
                if 1048576 <= float(value)*8 < 1073741824:
                        unit = 'Mbps'
                        result = round( float(value)/1048576 * 8, 2 )
                if float(value)*8 >= 1073741824:
                        unit = 'Gbps'
                        result = round( float(value)/1073741824 * 8, 2 )

                r = '%s %s' % (result, unit)
                return r

	@property
	def incount(self):
		r = self.unitTrans4Flow(self._incount)
		return r

	@property
	def outcount(self):
		r = self.unitTrans4Flow(self._outcount)
		return r
	
	@property
	def inrate(self):
		r = self.unitTrans4Rate(self._inrate)
		return r

	@property
	def outrate(self):
		r = self.unitTrans4Rate(self._outrate)
		return r

class NetRate(object):
	def __init__(self,rate_type,result):
		self.name = result["name"]
		self.id = result["iface_id"]
		self.ipaddr = result["ipaddr"]
		self.status = result["status"]
		self.graphs = 'graphs'
		if rate_type == 'in':
			self._rate = result["inrate"]
		else:
		   	self._rate = result["outrate"]

        def unitTrans4Rate(self,value):
                if float(value)*8 < 1024:
                        unit = 'bps'
                        result = round( float(value)*8, 2 )
                if 1024 <= float(value)*8 < 1048576:
                        unit = 'Kbps'
                        result = round( float(value)/1024 * 8, 2 )
                if 1048576 <= float(value)*8 < 1073741824:
                        unit = 'Mbps'
                        result = round( float(value)/1048576 * 8, 2 )
                if float(value)*8 >= 1073741824:
                        unit = 'Gbps'
                        result = round( float(value)/1073741824 * 8, 2 )

                r = '%s %s' % (result, unit)
                return r

	@property
	def rate(self):
		r = self.unitTrans4Rate(self._rate)
		return r

class Meters(object):
        def __init__(self,resource_id):
                self.resource_id = resource_id

class NetFlowManager(object):
    def getNetFlowData(self,request,date,allLongID):
        from openstack_dashboard import api
        import datetime
        import time
        current_month_in_total = 0.0
        current_month_out_total = 0.0
        year, month = date.split('-')
        last_month = int(month)-1 or 12
        last_month_year = year
        if last_month == 12:
            last_month_year = int(year)-1
        for j in allLongID:
            end_query = [dict(field='end', op='eq', value='%s-%s-01' % (year, month)), dict(field='resource', op='eq', value=j)]
            begin_query = [dict(field='end', op='eq', value='%s-%s-01' % (last_month_year, last_month)), dict(field='resource', op='eq', value=j)]
            try:
                end_in = api.ceilometer.statistic_list(request, meter_name='network.incoming.bytes', query=end_query)[0].max
            except IndexError:
                end_in = 0.0

            try:
                begin_in = api.ceilometer.statistic_list(request, meter_name='network.incoming.bytes', query=begin_query)[0].max
            except IndexError:
                begin_in = 0.0

            current_month_in_total += end_in - begin_in

            ###--------------------------------------------------------------------------------------------------------
            try:
                end_out = api.ceilometer.statistic_list(request, meter_name='network.outgoing.bytes', query=end_query)[0].max
            except IndexError:
                end_out = 0.0

            try:
                begin_out = api.ceilometer.statistic_list(request, meter_name='network.outgoing.bytes', query=begin_query)[0].max
            except IndexError:
                begin_out = 0.0

            current_month_out_total += end_out - begin_out

        ####get the max of network.incoming/outgoing.bytes.rate #########
        out_rate_array = []
        in_rate_array = []
        end_time_end = datetime.datetime.strptime('%s-%s-01 00:00:00' % (year, month), '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(seconds=600)
        begin_time = datetime.datetime.strptime('%s-%s-01 00:00:00' % (last_month_year, last_month), '%Y-%m-%d %H:%M:%S')
        end_time = begin_time + delta
        while end_time < end_time_end:
            try:
                single_point_out_sum = api.ceilometer.statistic_list(request, meter_name='network.outgoing.bytes.rate', query=[dict(field='start', op='eq', value=begin_time.strftime('%Y-%m-%dT%H%M%S')), dict(field='end', op='eq', value=end_time.strftime('%Y-%m-%dT%H%M%S'))])[0].sum
            except IndexError:
                single_point_out_sum = 0.0

            out_rate_array.append(single_point_out_sum)

            try:
                single_point_in_sum = api.ceilometer.statistic_list(request, meter_name='network.incoming.bytes.rate', query=[dict(field='start', op='eq', value=begin_time.strftime('%Y-%m-%dT%H%M%S')), dict(field='end', op='eq', value=end_time.strftime('%Y-%m-%dT%H%M%S'))])[0].sum
            except IndexError:
                single_point_in_sum = 0.0

            in_rate_array.append(single_point_in_sum)

            begin_time = end_time
            end_time = end_time + delta
        ####end of get the max of network.incoming/outgoing.bytes.rate #########
        return (current_month_in_total, current_month_out_total, max(in_rate_array), max(out_rate_array))
