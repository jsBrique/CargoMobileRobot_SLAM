
Highcharts.setOptions({
	global: {
		useUTC: false
	}
});

 	// 建立socket连接，等待服务器“推送”数据，用回调函数更新图表

var namespace = '/test';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

socket.on('server_response', function(res) {
	update_mychart(res);
});


console.log('get!');
	var chart = Highcharts.chart('containerX', {
		chart: {
		type: 'scatter',
	
		polar: true,
		
		events: {
			load: function () {
				var series = this.series[0],
                chart = this;
			}
		}
	},xAxis: {
		tickInterval: 45,
		min: 0,
		max: 360,
		labels: {
			formatter: function () {
				return this.value + '°';
			}
		}
	},
	title: {
		text: '激光雷达数据'
	},
	yAxis: {
		min: 0,
		max :5
	},
	plotOptions: {
		series: {
			pointStart: 0,
			pointInterval: 45
		},
		column: {
			pointPadding: 0,
			groupPadding: 0
		}
	},
	legend: {
		enabled: false
	},series: [{
		name: 'cpu',
		marker: { 
			radius: 1.5, 
		},
		color: 'rgba(223, 83, 83, .5)',
		
		data: (function () {
			// 生成随机值
			var data = [],
				i;
			for (i = 0; i <= 360; i += 1) {
				data.push({
					x: i,
					y: 0
				});
			}
			return data;
		}())
	}]
});	
			
			var data = [],
			i;
//准备好统一的 callback 函数
var update_mychart = function (res) { //res是json格式的response对象
        
        
	//console.log('get!');
        // 准备数据
        // time.push(res.data[0]);
        // cpu1.push(parseFloat(res.data[1]));
        
		
			for (i = 0; i <= 720; i += 1) {
				data[i]={
					x: parseFloat(i)*0.5,
					y: parseFloat(res.data[i])
				};
			};

		chart.series[0].setData(data,true,false,false);
        //updatechart();
        
        
    };