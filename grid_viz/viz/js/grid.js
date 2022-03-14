let Grid = (() => {

  /**
   * Define the dimension of the grid visualization
   */
  self.margin = {top: 30, right: 30, bottom: 30, left: 30},
  self.width = 720 - margin.left - margin.right,
  self.height = 720 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  const createSvg = (divName) => {
    const svg = d3.select("#pictogram_grid")
      .append("svg")
      .attr("width", self.width + self.margin.left + self.margin.right)
      .attr("height", self.height + self.margin.top + self.margin.bottom)
      .append("g")
      .attr("transform", `translate(${self.margin.left},${self.margin.top})`);

    return svg;
  }

  self.displayGrid = (divName) => {

    const svg = createSvg(divName);

    //Rows and cols
    const numrow = 9;
    const numcol = 9;

    // Build X scales and axis:
    const x = d3.scaleBand()
    .range([ 0, self.width ])
    .domain(d3.range(numrow))
    .padding(0.01);
    svg.append("g")
    .attr("transform", `translate(0, ${self.height})`)
    .call(d3.axisBottom(x))

    // Build X scales and axis:
    const y = d3.scaleBand()
    .range([ 0 , self.height ])
    .domain(d3.range(numcol))
    .padding(0.01);
    svg.append("g")
    .call(d3.axisLeft(y));

    //Read the data
    d3.csv("../../default.csv", d => (
    {
      word:     d.word,
      row:     +d.row,
      col:    +d.col,
      page: d.page,
      identifier: d.identifier,
    }
    )).then(function(data) {

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

    // Three function that change the tooltip when user hover / move / leave a cell
    const mouseover = function(event,d) {
      tooltip.style("opacity", 1)
    }
    const mousemove = function(event,d) {
      tooltip
        .html("Word : " + d.word)
        .style("left", (event.x)/2 + "px")
        .style("top", (event.y)/2 + "px")
    }
    const mouseleave = function(d) {
      tooltip.style("opacity", 0)
    }

    // add the squares
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

  return self;
})();