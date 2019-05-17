var width = 700,
    height = 1600;
var w = 700,
        h = 1600;
var cluster = d3.layout.cluster()
    .size([height, width - 160]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });
var margin = {top: 50, right: 20, bottom: 70, left: 70};
    var pad = 80;
    var width = 2 * w + pad;


// var svg = d3.select("body").append("svg")
//     .attr("width", width)
//     .attr("height", height)
//   .append("g")
//     .attr("transform", "translate(40,0)");
    var svg = d3.select('svg')
        .attr({
            'width': width + margin.left + margin.right,
            'height': h + margin.top + margin.bottom
        })
        .append('g')
        .attr({
            'transform': 'translate(' + margin.left + ',' + margin.top + ')',
            'width': width,
            'height': h
        });

d3.json("./static/json/test7.json", function(error, root) {
  var nodes = cluster.nodes(root),
      links = cluster.links(nodes);

  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

  node.append("circle")
      .attr("r", 4.5);

  node.append("text")
      .attr("dx", function(d) { return d.children ? -8 : 8; })
      .attr("dy", 3)
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      .text(function(d) { return d.name; });
});

d3.select(self.frameElement).style("height", height + "px");