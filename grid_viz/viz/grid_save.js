function Grid(){
  /**
   * Dimension of the grid in the visualization
   */
  const margin = {top: 30, right: 30, bottom: 30, left: 30},
  width = 720 - margin.left - margin.right,
  height = 720 - margin.top - margin.bottom;

  /**
   * SVG Element that will contain the grid
   */
  const svg = d3.select("#pictogram_grid")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

  /**
   * X scale and axis
   */
  const x = d3.scaleBand()
  .range([ 0, width ])
  .domain(d3.range(0))
  .padding(0.01);
  svg.append("g")
  .attr("transform", `translate(0, ${height})`)
  .call(d3.axisBottom(x))

  /**
   * Y scale and axis
   */
  const y = d3.scaleBand()
  .range([ 0 , height ])
  .domain(d3.range(0))
  .padding(0.01);
  svg.append("g")
  .call(d3.axisLeft(y));

  /**
   * Data preparation (read and assignation)
   */
  d3.csv("../../default.csv", d => (
  {
    word:     d.word,
    row:     +d.row,
    col:    +d.col,
    page: d.page,
    identifier: d.identifier,
  }
  )).then(function(data) {


  /**
   * Get the size of the grid (rows and columns)
   */
  var numcol = d3.max(data, d => d.col) + 1;
  var numrow = d3.max(data, d => d.row) + 1;

  x.domain(d3.range(numcol))
  y.domain(d3.range(numrow))

  // create a tooltip
  const tooltip = d3.select("#pictogram_grid")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  /**
   * Mouse : Three function that change the tooltip when user hover / move / leave a cell
   */
  const mouseover = function(event,d) {
    tooltip.style("opacity", 1)
    d3.select(this)
        .style("fill", "black")
        .style("stroke","black")
        .style("opacity", 0.3)
  }
  const mousemove = function(event,d) {
    tooltip
      .html("Word : " + d.word)
      .style("left", (event.x)/2 + "px")
      .style("top", (event.y)/2 + "px")
  }
  const mouseleave = function(d) {
    tooltip.style("opacity", 0)
    d3.select(this)
        .style("fill", "white")
        .style("opacity", 1)
  }

  /**
   * Fill the grid : squares and corresponding word.
   */
  svg.selectAll()
    .data(data)
    .enter()
    .append("rect")
      .attr("x", function(d) { return x(d.col) })
      .attr("y", function(d) { return y(d.row) })
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", "white" )
      .style("stroke","black")
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)

  svg.selectAll()
    .data(data)
    .enter()
      .append("text")
      .attr("dy", ".35em")
        .attr("x", function(d) { return x(d.col) + width/(numcol * 4) })
      .attr("y", function(d) { return y(d.row) + height/(numcol * 2) })
      .style("font-size", function(d) { return Math.min(2 / x.bandwidth(), (2 / x.bandwidth() - 8) / this.getComputedTextLength() * 24) + "px"; })
      .text(function(d) { return d.word; });
  })
}

Grid();