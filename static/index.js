function removeElementsByClass(className) {
  var elements = document.getElementsByClassName(className);
  while (elements.length > 0) {
    elements[0].parentNode.removeChild(elements[0]);
  }
}


var socket = io.connect('http://' + document.domain + ':' + location.port);



socket.on('connect', function() {
  console.log('connected')
  socket.emit('send_data');
});


var x = []
var update = false
TESTER = document.getElementById('tester');

socket.on('data', function(data) {
  x.push(data)
  update = true
});



function showPlot() {

  var trace1 = {
    x: x,
    type: "histogram",
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

showPlot()

function buttonClicked() {
  socket.emit('clicked');
}
