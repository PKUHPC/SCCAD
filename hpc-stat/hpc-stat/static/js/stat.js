var EchartDonutsPair = function(chart_info,gpu){
    if(!gpu){gpu = false}
    this.is_gpu = gpu

    var max_width = 25*chart_info.size

    var donut_id = chart_info.id
    var target_html_prifex = "#"+chart_info.id+" "
    var _this = this

    var fontsize = 1.5*chart_info.size+4

    if(navigator.userAgent.match(/mobile/i)) {
        fontsize = 12
    }

    var opt = {
        series:[
            {
                type:'pie',
                radius: ['50%', '75%'],
                startAngle:270,
                hoverOffset:6,
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center',
                        formatter:function(params){
                            return "{line|"+params.name+"\n"+params.value+"\n"+Math.round(params.percent)+"%}";
                        }
                    },
                    emphasis: {
                        show: true,
                        fontSize: fontsize,
                        fontWeight: 'normal',
                        color: 'rgb(50,50,50)',
                            rich:{
                                line:{lineHeight:fontsize+2}
                            },
                    }
                },
                labelLine: {
                    normal: {show: false}
                }
            },
            {
                type:'pie',
                radius: ['46%', '46%'],
                startAngle:270,
                avoidLabelOverlap: false,
                hoverOffset:2,
                label: {
                    normal: {show: false},
                    emphasis: {show: false}
                },
                labelLine: {
                    normal: {show: false}
               }
            },
        ]
    }

    var mouseover_action = function(params,who){
        for(var i=0;i<3;i++){
            who.dispatchAction({
                type: 'downplay',
                seriesIndex:[0,1],
                dataIndex:i
            });
        }
        who.dispatchAction({
            type: 'highlight',
            seriesIndex:[0,1],
            dataIndex:params.dataIndex
        });
    }

    var mouseout_action = function(who){
        for(var i=0;i<3;i++){
            who.dispatchAction({
            type: 'downplay',
            seriesIndex:[0,1],
            dataIndex:i
            });
        }
        who.dispatchAction({
            type: 'highlight',
            seriesIndex:[0,1],
            dataIndex:1
        });
    }

    this.setup_html = function(data){
        $(target_html_prifex+".node_tot").html(data.node_tot)
        $(target_html_prifex+".node_free").html(data.node_available)
        $(target_html_prifex+".node_alloc").html(data.node_busy+data.node_running)
        $(target_html_prifex+".node_error").html(data.node_error)
        if(this.is_gpu){
            $(target_html_prifex+".cpu_tot").html(data.gpu_tot)
            $(target_html_prifex+".cpu_free").html(data.gpu_free)
            $(target_html_prifex+".cpu_alloc").html(data.gpu_alloc)
            $(target_html_prifex+".cpu_error").html(data.gpu_error)
        } else {
            $(target_html_prifex+".cpu_tot").html(data.cpu_tot)
            $(target_html_prifex+".cpu_free").html(data.cpu_free)
            $(target_html_prifex+".cpu_alloc").html(data.cpu_alloc)
            $(target_html_prifex+".cpu_error").html(data.cpu_error)
        }
    }

    this.refresh = function(data){
        this.node_donut.hideLoading()
        var node_dataset = {
            series:[
                {
                    data:[
                        {name:data.lan_error, value:data.node_error, emphasis: {itemStyle:{color:chart_info.colors.node[0]}}},
                        {name:data.lan_running, value:data.node_busy+data.node_running, emphasis: {itemStyle:{color:chart_info.colors.node[1]}}},
                        {name:data.lan_available, value:data.node_available, emphasis: {itemStyle:{color:chart_info.colors.node[2]}}}
                    ]
                },{
                    data:[
                        {name:data.lan_error, value:data.node_error},
                        {name:data.lan_running, value:data.node_busy+data.node_running},
                        {name:data.lan_available, value:data.node_available}
                    ]
                }
            ]
        }
        this.node_donut.setOption(node_dataset)
        mouseout_action(_this.node_donut)

        if(this.is_gpu){
            this.gpu_donut.hideLoading()
            var gpu_dataset = {
                series:[
                    {
                    data:[
                        {name:data.lan_error, value:data.gpu_error, emphasis: {itemStyle:{color:chart_info.colors.core[0]}}},
                        {name:data.lan_running, value:data.gpu_alloc, emphasis: {itemStyle:{color:chart_info.colors.core[1]}}},
                        {name:data.lan_available, value:data.gpu_free, emphasis: {itemStyle:{color:chart_info.colors.core[2]}}}
                    ]
                    },{
                    data:[
                        {name:data.lan_error, value:data.gpu_error},
                        {name:data.lan_running, value:data.gpu_alloc},
                        {name:data.lan_available, value:data.gpu_free}
                    ]
                    }
                ]
            }
            this.gpu_donut.setOption(gpu_dataset)
            mouseout_action(_this.gpu_donut)
        } else {
            this.core_donut.hideLoading()
            var core_dataset = {
                series:[
                    {
                    data:[
                        {name:data.lan_error, value:data.cpu_error, emphasis: {itemStyle:{color:chart_info.colors.core[0]}}},
                        {name:data.lan_running, value:data.cpu_alloc, emphasis: {itemStyle:{color:chart_info.colors.core[1]}}},
                        {name:data.lan_available, value:data.cpu_free, emphasis: {itemStyle:{color:chart_info.colors.core[2]}}}
                    ]
                    },{
                    data:[
                        {name:data.lan_error, value:data.cpu_error},
                        {name:data.lan_running, value:data.cpu_alloc},
                        {name:data.lan_available, value:data.cpu_free}
                    ]
                    }
                ]
            }
            this.core_donut.setOption(core_dataset)
            mouseout_action(_this.core_donut)
        }

        this.setup_html(data)
    }

    this.resize = function(){
        var w = $("#"+donut_id+"-node-chart").parent().width();
        if(w>max_width)
            w=max_width;
        $("#"+donut_id+"-node-chart").height(w-10)
        $("#"+donut_id+"-cpu-chart").height(w-10)
        $("#"+donut_id+"-node-chart").width(w-10)
        $("#"+donut_id+"-cpu-chart").width(w-10)
        this.node_donut.resize()
        this.core_donut.resize()
        mouseout_action(_this.node_donut)
        mouseout_action(_this.core_donut)
    }


    this.node_donut = echarts.init(document.getElementById(donut_id+"-node-chart"));
    this.node_donut.setOption(opt)
    this.node_donut.setOption({color:chart_info.colors.node})
    this.node_donut.showLoading()
    this.node_donut.on("mouseover", function(params){mouseover_action(params,_this.node_donut)})
    this.node_donut.on("mouseout", function(params){mouseout_action(_this.node_donut)})
    this.node_donut.on("click", function(params){
        window.location.href=urls("node")
    })

    if(this.is_gpu){
        $("#"+donut_id+"-cpu-chart").siblings("h6.cpu_title").css("display","none")
        $("#"+donut_id+"-cpu-chart").siblings("h6.gpu_title").css("display","block")

        this.gpu_donut = echarts.init(document.getElementById(donut_id+"-cpu-chart"));
        this.gpu_donut.setOption(opt)
        this.gpu_donut.setOption({color:chart_info.colors.core})
        this.gpu_donut.showLoading()
        this.gpu_donut.on("mouseover", function(params){mouseover_action(params,_this.gpu_donut)})
        this.gpu_donut.on("mouseout", function(params){mouseout_action(_this.gpu_donut)})
        this.gpu_donut.on("click", function(params){
            window.location.href=urls("node")
        })
    } else {
        this.core_donut = echarts.init(document.getElementById(donut_id+"-cpu-chart"));
        this.core_donut.setOption(opt)
        this.core_donut.setOption({color:chart_info.colors.core})
        this.core_donut.showLoading()
        this.core_donut.on("mouseover", function(params){mouseover_action(params,_this.core_donut)})
        this.core_donut.on("mouseout", function(params){mouseout_action(_this.core_donut)})
        this.core_donut.on("click", function(params){
            window.location.href=urls("node")
        })
    }
}

$(function(){
	var async_url = urls("async")
    var w = $(".brief-bar").parent().width();
    $(".brief-bar").width(w-10)
    $(".brief-bar").height(w-10)
    var all_bars = new EchartBarCharts()

    $.get("/stat/brief",function(data){
        all_bars.refresh(data)
    })

	setInterval(function(){
        $.get("/stat/brief",function(data){
            all_bars.refresh(data)
        })
    },60000)

    $(window).resize(function(){
        all_bars.resize()
    })
})
