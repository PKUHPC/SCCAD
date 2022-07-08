$(function(){
	var async_url = urls("async")
    $(".guage").height($(".guage").width())
	var all_donuts = new EchartDonutsPair(page[0])
	var cpu_donuts = new EchartDonutsPair(page[1])
    var gpu_donuts = new EchartDonutsPair(page[2],true)
	$.get(async_url,function(data){
        all_donuts.refresh(data.node.all_nodes)
        cpu_donuts.refresh(data.node.cpu_nodes)
        gpu_donuts.refresh(data.node.gpu_nodes)
		var job_url = urls("job")
        var job_info = new PanelList({id : "job-info"},job_url)
        var job_pending = new PanelList({id : "job-waiting"},job_url)
        var job_running = new PanelList({id : "job-running"},job_url)

		job_info.setup_content(data.job.job_info)
        job_pending.setup_content(data.job.pending_list)
        job_running.setup_content(data.job.running_list)

		$(window).resize(function(){
            $(".guage").height($(".guage").width())
            all_donuts.resize()
            cpu_donuts.resize()
            gpu_donuts.resize()
        })
		setInterval(function(){
		    $.get(async_url,function(data){
                all_donuts.refresh(data.node.all_nodes)
                cpu_donuts.refresh(data.node.cpu_nodes)
                gpu_donuts.refresh(data.node.gpu_nodes)

                job_info.setup_content(data.job.job_info)
                job_pending.setup_content(data.job.pending_list)
                job_running.setup_content(data.job.running_list)
		    })
        },15000)

	})
})

var node_chart = echarts.init(document.getElementById('node_chart'));
var user_chart = echarts.init(document.getElementById('user_chart'));

var node_opt = {
    legend: {data:['节点使用率', '核心使用率']},
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
			var content = params[0].name
			for(x in params){
				content = content + '<br>' + params[x].seriesName + ':' + params[x].value[1]+"%"
			}
            return content
        }
    },
    xAxis: {type: 'time'},
    yAxis: {
        type: 'value',
        min:0,
        max:100,
        axisLabel: {formatter: '{value}%'}
    },
    series: [{
            name: '节点使用率',
            showSymbol: false,
            type: 'line',
            hoverAnimation: false,
            itemStyle:{color: "#DC5712"}
        }, {
            name: '核心使用率',
            type: 'line',
            showSymbol: false,
            hoverAnimation: false,
            itemStyle:{color: "#FFC000"}
    }]
}
var user_opt = {
    legend: {data:['用户数', '任务数', '运行任务数', '排队任务数']},
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
			var content = params[0].name
			for(x in params){
				content = content + '<br>' + params[x].seriesName + ':' + params[x].value[1]
			}
            return content
        },
        axisPointer: {
            animation: false
        }
    },
    xAxis: {type: 'time'},
    yAxis: {type: 'value'},
    series: [
		{
            name: '用户数',
            type: 'line',
            itemStyle:{color: "#DC5712"},
            showSymbol: false,
            hoverAnimation: false
        }, {
            name: '任务数',
            type: 'line',
            itemStyle:{color: "#FFC000"},
            showSymbol: false,
            hoverAnimation: false
    	}, {
            name: '运行任务数',
            type: 'line',
            itemStyle:{color: "#95BCB2"},
            showSymbol: false,
            hoverAnimation: false
		}, {
            name: '排队任务数',
            type: 'line',
            itemStyle:{color: "#C7BB89"},
            showSymbol: false,
            hoverAnimation: false
		}
	]
}
node_chart.setOption(node_opt)
user_chart.setOption(user_opt)

node_chart.showLoading()
user_chart.showLoading()

var date_val = function(date_obj){
	var day = ("0" + date_obj.getDate()).slice(-2);
	var month = ("0" + (date_obj.getMonth()+1)).slice(-2);
	return date_obj.getFullYear()+"-"+(month)+"-"+(day)
}

$.get(urls("history"),function(data){
    $(".history[value='2-DAY']").addClass("active")

	var curDate = new Date();
	var preDate = new Date(curDate.getTime() - 2*24*60*60*1000)
	$("input.start-date").each(function(){
		$(this).val(date_val(preDate))
	})
	$("input.end-date").each(function(){
		$(this).val(date_val(curDate))
	})

    node_chart.hideLoading()
    user_chart.hideLoading()

    var node_data = {
		legend: {data:[data.lan.node_usage, data.lan.core_usage]},
		series: [
			{name:data.lan.node_usage,data:data.node},
			{name:data.lan.core_usage,data:data.core}
		]
    }
    var user_data = {
		legend: {data:[data.lan.user_count, data.lan.job_count, data.lan.running_job_count, data.lan.waiting_job_count]},
		series: [
			{name:data.lan.user_count,data:data.user},
			{name:data.lan.job_count,data:data.job},
			{name:data.lan.running_job_count,data:data.running_job},
			{name:data.lan.waiting_job_count,data:data.waiting_job}
		]
    }

    node_chart.setOption(node_data)
    user_chart.setOption(user_data)

    $("#node_chart").next().html(
		get_info(data.lan.node_usage,data.node,"%")+
		get_info(data.lan.core_usage,data.core,"%")
    )
    $("#user_chart").next().html(
		get_info(data.lan.job_count,data.job,"")+
		get_info(data.lan.user_count,data.user,"")
    )
})


//更新节点、用户使用历史表
$(".history").click(function(){
	var params = {}
	var action = ($(this).hasClass("check") ? "history_check" : "history");

	/* 有check: 处理一个时间段的查询
	 * 没有 check: 处理最近多长时间的查询
	 */
	if($(this).hasClass("check")){
		$(this).parent().parent().parent().parent().parent().find("#history a").removeClass("active")
		var start_date_val = $(this).parent().parent().find(".start-date").val()
		var end_date_val = $(this).parent().parent().find(".end-date").val()
		var start_date = new Date(start_date_val)
		var end_date = new Date(end_date_val)

		// 时间格式检测，如果错了弹出提示框
		var add_popover = function(dom,text){
			var opt = function(text){
				var content = "<p class='text-danger'>"
				content += text
				content += "<div>"
				return {"content":content,"placement":"top","html":true}
			}
			dom.popover(opt(text))
			dom.popover("show")
			dom.focus()
			dom.parent().parent().find("input").each(function(){
				$(this).click(function(){
					dom.popover("dispose")
				})
			})
		}

		if (start_date == "Invalid Date"){
			add_popover($(this).parent().parent().find(".start-date"),"开始日期错误")
			return
		} else if (end_date == "Invalid Date"){
			add_popover($(this).parent().parent().find(".end-date"),"结束日期错误")
			return
		} else if (start_date >= end_date){
			add_popover($(this).parent().parent().find(".start-date"),"开始日期应早于结束日期")
			return
		}
		params.start_date = start_date_val
		params.end_date = end_date_val
	} else {
    	$(this).parent().parent().find("a").removeClass("active")
		$(this).addClass("active")
		params.period = $(this).attr("value")
		var dates = params.period.split('-')
		var offset = 24*60*60*1000
		if(dates[1] == 'DAY'){
			offset = offset*dates[0]
		} else {
			offset = offset*dates[0]*30
		}
		var curDate = new Date();
		var preDate = new Date(curDate.getTime() - offset)
		$("input.start-date").each(function(){
			$(this).val(date_val(preDate))
		})
		$("input.end-date").each(function(){
			$(this).val(date_val(curDate))
		})
	}

    if($(this).hasClass("node")){
        node_chart.showLoading()
		params.type = "node"
        $.get(urls(action,params),function(data){
            node_chart.hideLoading()
            var node_data = {
				legend: {data:[data.lan.node_usage, data.lan.core_usage]},
                series: [
                    {name:data.lan.node_usage,data:data.node},
                    {name:data.lan.core_usage,data:data.core}
                ]
            }
            node_chart.setOption(node_data)
            $("#node_chart").next().html(
				get_info(data.lan.node_usage,data.node,"%")+
				get_info(data.lan.core_usage,data.core,"%")
            )
        })
    } else if ($(this).hasClass("user")) {
        user_chart.showLoading()
		params.type = "user"
        $.get(urls(action,params),function(data){
            user_chart.hideLoading()
            var user_data = {
				legend: {data:[data.lan.user_count, data.lan.job_count, data.lan.running_job_count, data.lan.waiting_job_count]},
                series: [
                    {name:data.lan.user_count,data:data.user},
                    {name:data.lan.job_count,data:data.job},
					{name:data.lan.running_job_count,data:data.running_job},
					{name:data.lan.waiting_job_count,data:data.waiting_job}
                ]
            }
            user_chart.setOption(user_data)
            $("#user_chart").next().html(
				get_info(data.lan.job_count,data.job,"")+
				get_info(data.lan.user_count,data.user,"")
            )
        })
    }
})

$(window).resize(function(){
    node_chart.resize()
    user_chart.resize()
})
