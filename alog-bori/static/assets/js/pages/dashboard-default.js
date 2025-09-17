'use strict';
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    floatchart();
  }, 500);
});

function floatchart() {
  (function () {
    var options11 = {
        chart: {height: 450,type: 'area',toolbar: {show: false}}
        ,dataLabels: {enabled: false}
        ,colors: ['#1890ff', '#13c2c2']
        ,series: [{name: 'Page Views',data: [31, 40, 28, 51, 42, 109, 100]}, {name: 'Sessions',data: [11, 32, 45, 32, 34, 52, 41]}]
        ,stroke: {curve: 'smooth',width: 2}
        ,xaxis: {categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],}
    };


    var chart = new ApexCharts(document.querySelector('#dchart-01-01'),
{
chart: {height: 450,type: 'area',toolbar: {show: false}}
,dataLabels: {enabled: false}
,colors: ['#1890ff', '#13c2c2']
,stroke: {curve: 'smooth',width: 2}
,series: [{name: 'Page Views',data: [131, 40, 28, 51, 42, 109, 100]}, {name: 'Sessions',data: [11, 32, 45, 32, 34, 52, 41]}]
,xaxis: {categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],}
}
    );
    chart.render();

    var options12 = {
        chart: {height: 450,type: 'area',toolbar: {show: false}}
        ,dataLabels: {enabled: false}
        ,colors: ['#1890ff', '#13c2c2']
        ,series: [{name: 'Page Views',data: [76, 85, 101, 98, 87, 105, 91, 114, 94, 86, 115, 35]}, {name: 'Sessions',data: [110, 60, 150, 35, 60, 36, 26, 45, 65, 52, 53, 41]}]
        ,stroke: {curve: 'smooth',width: 2}
        ,xaxis: {categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],}
    };
    var chart = new ApexCharts(document.querySelector('#dchart-01-02'), options12);
    chart.render();

    var options13 = {
        chart: {height: 450,type: 'area',toolbar: {show: false}}
        ,dataLabels: {enabled: false}
        ,colors: ['#1890ff', '#13c2c2', '#ff0000']
        ,series: [{name: 'Page Views',data: [176, 185, 101, 98, 87, 105, 91, 114, 94, 86, 115, 35]}, {name: 'Sessions',data: [110, 60, 150, 35, 60, 36, 26, 45, 65, 52, 53, 41]}, {name: 'Sessions2',data: [130, 60, 150, 35, 60, 36, 26, 45, 65, 52, 53, 41]}]
        ,stroke: {curve: 'smooth',width: 2}
        ,xaxis: {categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],}
    };
    var chart = new ApexCharts(document.querySelector('#dchart-01-03'), options13);
    chart.render();

    var options14 = {
        chart: {height: 450,type: 'area',toolbar: {show: false}}
        ,dataLabels: {enabled: false}
        ,colors: ['#1890ff', '#13c2c2']
        ,series: [{name: 'Page Views',data: [576, 185, 101, 98, 87, 105, 91, 114, 94, 86, 115, 35]}, {name: 'Sessions',data: [110, 60, 150, 35, 60, 36, 26, 45, 65, 52, 53, 41]}]
        ,stroke: {curve: 'smooth',width: 2}
        ,xaxis: {categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],}
    };
    var chart = new ApexCharts(document.querySelector('#dchart-01-04'), options14);
    chart.render();

    var options5 = {
        chart: {height: 450,type: 'area',toolbar: {show: false}}
        ,dataLabels: {enabled: false}
        ,colors: ['#1890ff', '#13c2c2']
        ,series: [{name: 'Page Views',data: [476, 185, 101, 98, 87, 105, 91, 114, 94, 86, 115, 35]}, {name: 'Sessions',data: [110, 60, 150, 35, 60, 36, 26, 45, 65, 52, 53, 41]}]
        ,stroke: {curve: 'smooth',width: 2}
        ,xaxis: {categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],}
    };
    var chart = new ApexCharts(document.querySelector('#dchart-02-02'), options5);
    chart.render();

    var options6 = {
        chart: {height: 450,type: 'area',toolbar: {show: false}}
        ,dataLabels: {enabled: false}
        ,colors: ['#1890ff', '#13c2c2']
        ,series: [{name: 'Page Views',data: [376, 185, 101, 98, 87, 105, 91, 114, 94, 86, 115, 35]}, {name: 'Sessions',data: [110, 60, 150, 35, 60, 36, 26, 45, 65, 52, 53, 41]}]
        ,stroke: {curve: 'smooth',width: 2}
        ,xaxis: {categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],}
    };
    var chart = new ApexCharts(document.querySelector('#dchart-02-03'), options6);
    chart.render();
  })();

  (function () {
    var options = {
      chart: {
        type: 'bar',
        height: 365,
        toolbar: {
          show: false
        }
      },
      colors: ['#13c2c2'],
      plotOptions: {
        bar: {
          columnWidth: '45%',
          borderRadius: 4
        }
      },
      dataLabels: {
        enabled: false
      },
      series: [{
        data: [80, 95, 70, 42, 65, 55, 78]
      }],
      stroke: {
        curve: 'smooth',
        width: 2
      },
      xaxis: {
        categories: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Sㅕ'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        }
      },
      yaxis: {
        show: false
      },
      grid: {
        show: false
      }
    };
    var chart = new ApexCharts(document.querySelector('#income-overview-chart'), options);
    chart.render();
  })();



  (function () {
    var options = {
      chart: {
        type: 'bar',
        height: 365,
        toolbar: {
          show: false
        }
      },
      colors: ['#13c2c2'],
      plotOptions: {
        bar: {
          columnWidth: '45%',
          borderRadius: 4
        }
      },
      dataLabels: {
        enabled: false
      },
      series: [{
        data: [80, 95, 70, 42, 65, 55, 78]
      }],
      stroke: {
        curve: 'smooth',
        width: 2
      },
      xaxis: {
        categories: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        }
      },
      yaxis: {
        show: false
      },
      grid: {
        show: false
      }
    };
    var chart = new ApexCharts(document.querySelector('#income-overview-chart2'), options);
    chart.render();
  })();
  
  (function () {
    var options21 = {
      chart: {type: 'line',height: 340,toolbar: {show: false}}
      ,colors: ['#faad14']
      ,plotOptions: {bar: {columnWidth: '45%',borderRadius: 4}}
      ,stroke: {curve: 'smooth',width: 1.5}
      ,grid: {strokeDashArray: 4}
      ,series: [{data: [58, 90, 38, 83, 63, 75, 35, 55]}]
      ,xaxis: {type: 'datetime'
        ,categories: ['2018-05-19T00:00:00.000Z','2018-06-19T00:00:00.000Z','2018-07-19T01:30:00.000Z','2018-08-19T02:30:00.000Z','2018-09-19T03:30:00.000Z','2018-10-19T04:30:00.000Z','2018-11-19T05:30:00.000Z','2018-12-19T06:30:00.000Z']
        ,labels: {format: 'MMM'}
        ,axisBorder: {show: false}
        ,axisTicks: {show: false}
        }
    ,yaxis: {show: false},
    };
    var chart = new ApexCharts(document.querySelector('#ana_21'), options21);
    chart.render();

    var options22 = {
      chart: {type: 'line',height: 340,toolbar: {show: false}}
      ,colors: ['#faad14']
      ,plotOptions: {bar: {columnWidth: '45%',borderRadius: 4}}
      ,stroke: {curve: 'smooth',width: 1.5}
      ,grid: {strokeDashArray: 4}
      ,series: [{data: [58, 90, 38, 83, 63, 75, 35, 55]}]
      ,xaxis: {type: 'datetime'
        ,categories: ['2018-05-19T00:00:00.000Z','2018-06-19T00:00:00.000Z','2018-07-19T01:30:00.000Z','2018-08-19T02:30:00.000Z','2018-09-19T03:30:00.000Z','2018-10-19T04:30:00.000Z','2018-11-19T05:30:00.000Z','2018-12-19T06:30:00.000Z']
        ,labels: {format: 'MMM'}
        ,axisBorder: {show: false}
        ,axisTicks: {show: false}
        }
    ,yaxis: {show: false},
    };
    var chart = new ApexCharts(document.querySelector('#ana_22'), options22);
    chart.render();

    var options23 = {
      chart: {type: 'line',height: 340,toolbar: {show: false}}
      ,colors: ['#faad14']
      ,plotOptions: {bar: {columnWidth: '45%',borderRadius: 4}}
      ,stroke: {curve: 'smooth',width: 1.5}
      ,grid: {strokeDashArray: 4}
      ,series: [{data: [58, 90, 38, 83, 63, 75, 35, 55]}]
      ,xaxis: {type: 'datetime'
        ,categories: ['2018-05-19T00:00:00.000Z','2018-06-19T00:00:00.000Z','2018-07-19T01:30:00.000Z','2018-08-19T02:30:00.000Z','2018-09-19T03:30:00.000Z','2018-10-19T04:30:00.000Z','2018-11-19T05:30:00.000Z','2018-12-19T06:30:00.000Z']
        ,labels: {format: 'MMM'}
        ,axisBorder: {show: false}
        ,axisTicks: {show: false}
        }
    ,yaxis: {show: false},
    };
    var chart = new ApexCharts(document.querySelector('#ana_23'), options23);
    chart.render();

    var options24 = {
      chart: {type: 'line',height: 340,toolbar: {show: false}}
      ,colors: ['#faad14']
      ,plotOptions: {bar: {columnWidth: '45%',borderRadius: 4}}
      ,stroke: {curve: 'smooth',width: 1.5}
      ,grid: {strokeDashArray: 4}
      ,series: [{data: [58, 90, 38, 83, 63, 75, 35, 55]}]
      ,xaxis: {type: 'datetime'
        ,categories: ['2018-05-19T00:00:00.000Z','2018-06-19T00:00:00.000Z','2018-07-19T01:30:00.000Z','2018-08-19T02:30:00.000Z','2018-09-19T03:30:00.000Z','2018-10-19T04:30:00.000Z','2018-11-19T05:30:00.000Z','2018-12-19T06:30:00.000Z']
        ,labels: {format: 'MMM'}
        ,axisBorder: {show: false}
        ,axisTicks: {show: false}
        }
    ,yaxis: {show: false},
    };
    var chart = new ApexCharts(document.querySelector('#ana_24'), options24);
    chart.render();

    var options25 = {
      chart: {type: 'line',height: 340,toolbar: {show: false}}
      ,colors: ['#faad14']
      ,plotOptions: {bar: {columnWidth: '45%',borderRadius: 4}}
      ,stroke: {curve: 'smooth',width: 1.5}
      ,grid: {strokeDashArray: 4}
      ,series: [{data: [58, 90, 38, 83, 63, 75, 35, 55]}]
      ,xaxis: {type: 'datetime'
        ,categories: ['2018-05-19T00:00:00.000Z','2018-06-19T00:00:00.000Z','2018-07-19T01:30:00.000Z','2018-08-19T02:30:00.000Z','2018-09-19T03:30:00.000Z','2018-10-19T04:30:00.000Z','2018-11-19T05:30:00.000Z','2018-12-19T06:30:00.000Z']
        ,labels: {format: 'MMM'}
        ,axisBorder: {show: false}
        ,axisTicks: {show: false}
        }
    ,yaxis: {show: false},
    };
    var chart = new ApexCharts(document.querySelector('#ana_25'), options25);
    chart.render();

    var options26 = {
      chart: {type: 'line',height: 340,toolbar: {show: false}}
      ,colors: ['#faad14']
      ,plotOptions: {bar: {columnWidth: '45%',borderRadius: 4}}
      ,stroke: {curve: 'smooth',width: 1.5}
      ,grid: {strokeDashArray: 4}
      ,series: [{data: [58, 90, 38, 83, 63, 75, 35, 55]}]
      ,xaxis: {type: 'datetime'
        ,categories: ['2018-05-19T00:00:00.000Z','2018-06-19T00:00:00.000Z','2018-07-19T01:30:00.000Z','2018-08-19T02:30:00.000Z','2018-09-19T03:30:00.000Z','2018-10-19T04:30:00.000Z','2018-11-19T05:30:00.000Z','2018-12-19T06:30:00.000Z']
        ,labels: {format: 'MMM'}
        ,axisBorder: {show: false}
        ,axisTicks: {show: false}
        }
    ,yaxis: {show: false},
    };
    var chart = new ApexCharts(document.querySelector('#ana_26'), options26);
    chart.render();


  })();


  (function () {
    var options = {
      chart: {
        type: 'bar',
        height: 430,
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        bar: {
          columnWidth: '30%',
          borderRadius: 4
        }
      },
      stroke: {
        show: true,
        width: 8,
        colors: ['transparent']
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top',
        horizontalAlign: 'right',
        show: true,
        fontFamily: `'Public Sans', sans-serif`,
        offsetX: 10,
        offsetY: 10,
        labels: {
          useSeriesColors: false
        },
        markers: {
          width: 10,
          height: 10,
          radius: '50%',
          offsexX: 2,
          offsexY: 2
        },
        itemMargin: {
          horizontal: 15,
          vertical: 5
        }
      },
      colors: ['#faad14', '#1890ff'],
      series: [{
        name: 'Net Profit',
        data: [180, 90, 135, 114, 120, 145]
      }, {
        name: 'Revenue',
        data: [120, 45, 78, 150, 168, 99]
      }],
      xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
      },
    }
    var chart = new ApexCharts(document.querySelector('#sales-report-chart'), options);
    chart.render();
  })();
}
