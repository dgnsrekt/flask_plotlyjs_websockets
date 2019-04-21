function removeElementsByClass(className) {
  var elements = document.getElementsByClassName(className);
  while (elements.length > 0) {
    elements[0].parentNode.removeChild(elements[0]);
  }
}


var socket = io.connect('http://' + document.domain + ':' + location.port);

var x = []
var update = false
TESTER = document.getElementById('tester');

socket.on('connect', function() {
  console.log('connected')
  socket.emit('send_data');
});

socket.on('data', function(data) {
  x.push(data)
  update = true
});

function showPlot() {

  var trace1 = {
    x: x,
    type: "histogram",
    histnorm: 'density',
    opacity: 0.5,
    marker: {
      color: 'green',
    },
  };

  var data = [trace1];
  var layout = { barmode: "overlay" };
  // console.log(x)

  Plotly.newPlot(TESTER, data, layout, { responsive: true });
}

var interval = setInterval(function() {
  if (update === true) {
    removeElementsByClass('modebar')
    showPlot()
    update = false
  }
}, 300);


function buttonClicked() {
  emit_data = document.getElementById('emit_data').value
  x = []
  socket.emit('clicked', { data: emit_data });
}
showPlot()
