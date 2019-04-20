var socket = io.connect('http://' + document.domain + ':' + location.port);

var x = []
socket.on('connect', function() {
  console.log('connected')
  socket.emit('send_data');
});
socket.on('data', function(data) {

  console.log(data)

  TESTER = document.getElementById('tester');

  x.push(data)
  console.log(x)

  var data_plot = [{
    x: x,
    type: 'histogram',
    histnorm: 'probability',
    marker: {
      color: 'rgb(255,0,0)',
    },
  }];
  Plotly.newPlot(TESTER, data_plot)
});
