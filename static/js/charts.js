// Initialize ECharts instances
document.addEventListener('DOMContentLoaded', () => {
    // Cyberpunk ECharts Theme Colors
    const neonCyan = '#00f3ff';
    const neonMagenta = '#ff00ff';
    const neonRed = '#ff003c';
    const neonYellow = '#ffea00';
    const darkBg = 'transparent';
    const textMain = '#e0e0e0';

    const patientChartEl = document.getElementById('patientInfluxChart');
    const heatmapEl = document.getElementById('deptLoadChart');

    if(patientChartEl && heatmapEl) {
        const patientChart = echarts.init(patientChartEl);
        const heatmapChart = echarts.init(heatmapEl);

        // 1. Patient Influx Line Chart
        const influxOption = {
            backgroundColor: darkBg,
            tooltip: { trigger: 'axis', backgroundColor: 'rgba(10,10,15,0.9)', borderColor: neonCyan, textStyle: { color: '#fff'} },
            legend: { data: ['ER Admissions', 'OPD Consultations'], textStyle: { color: textMain } },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                axisLabel: { color: textMain },
                axisLine: { lineStyle: { color: 'rgba(255,255,255,0.2)' } }
            },
            yAxis: {
                type: 'value',
                axisLabel: { color: textMain },
                splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
            },
            series: [
                {
                    name: 'ER Admissions',
                    type: 'line',
                    smooth: true,
                    lineStyle: { color: neonRed, width: 3 },
                    itemStyle: { color: neonRed },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(255,0,60,0.5)' },
                            { offset: 1, color: 'rgba(255,0,60,0.0)' }
                        ])
                    },
                    data: [12, 5, 20, 35, 28, 45, 15]
                },
                {
                    name: 'OPD Consultations',
                    type: 'line',
                    smooth: true,
                    lineStyle: { color: neonCyan, width: 3 },
                    itemStyle: { color: neonCyan },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(0,243,255,0.5)' },
                            { offset: 1, color: 'rgba(0,243,255,0.0)' }
                        ])
                    },
                    data: [0, 0, 45, 120, 90, 30, 5]
                }
            ]
        };
        patientChart.setOption(influxOption);

        // 2. Department Load Heatmap
        // Mock data for heatmap (Departments vs Time)
        const hours = ['8a', '10a', '12p', '2p', '4p', '6p', '8p'];
        const depts = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology'];
        
        // Generate random heatmap data
        const heatmapData = [];
        for (let i = 0; i < hours.length; i++) {
            for (let j = 0; j < depts.length; j++) {
                heatmapData.push([i, j, Math.floor(Math.random() * 100)]);
            }
        }

        const heatmapOption = {
            backgroundColor: darkBg,
            tooltip: { position: 'top', backgroundColor: 'rgba(10,10,15,0.9)', borderColor: neonMagenta, textStyle: { color: '#fff'} },
            grid: { top: '5%', bottom: '15%', left: '15%', right: '5%' },
            xAxis: {
                type: 'category',
                data: hours,
                splitArea: { show: true },
                axisLabel: { color: textMain }
            },
            yAxis: {
                type: 'category',
                data: depts,
                splitArea: { show: true },
                axisLabel: { color: textMain }
            },
            visualMap: {
                min: 0,
                max: 100,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '0%',
                inRange: {
                    color: ['rgba(0,243,255,0.2)', neonMagenta, neonRed]
                },
                textStyle: { color: textMain }
            },
            series: [{
                name: 'Patient Load %',
                type: 'heatmap',
                data: heatmapData,
                label: { show: true, color: '#fff' },
                emphasis: {
                    itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' }
                }
            }]
        };
        heatmapChart.setOption(heatmapOption);

        // Resize charts on window resize
        window.addEventListener('resize', () => {
            patientChart.resize();
            heatmapChart.resize();
        });
    }

    // Fetch KPI Data
    const fetchKPIs = () => {
        // ICU & General Occupancy
        fetch('/api/occupancy')
            .then(res => res.json())
            .then(data => {
                document.getElementById('icuValue').textContent = data.icu_current_occupancy + '%';
                const trend = data.icu_predicted_next_48h - data.icu_current_occupancy;
                document.getElementById('icuTrend').innerHTML = `${trend > 0 ? 'Up' : 'Down'} ${Math.abs(trend)}% (48h)`;
                document.getElementById('icuTrend').className = trend > 0 ? 'kpi-trend negative' : 'kpi-trend positive';
            });

        // Queue Prediction
        fetch('/api/queue')
            .then(res => res.json())
            .then(data => {
                document.getElementById('erWaitValue').textContent = data.emergency_room_wait_mins + ' min';
                document.getElementById('erTrend').textContent = 'Live prediction';
                document.getElementById('staffValue').textContent = data.active_doctors_er + data.active_doctors_opd;
            });

        // Outbreaks
        fetch('/api/outbreaks')
            .then(res => res.json())
            .then(data => {
                const outVal = document.getElementById('outbreakValue');
                const outTrend = document.getElementById('outbreakTrend');
                if(data.length === 0) {
                    outVal.textContent = "None";
                    outTrend.textContent = "System Clear";
                    outTrend.className = "kpi-trend positive";
                } else {
                    outVal.textContent = data.length + " Active";
                    outTrend.textContent = "High Alert";
                    outTrend.className = "kpi-trend negative";
                }
            });
    };

    if(document.getElementById('icuValue')) {
        fetchKPIs();
        // Refresh KPIs every 30 seconds
        setInterval(fetchKPIs, 30000);
    }
});
