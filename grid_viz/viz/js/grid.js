let Grid = (() => {

  let self = {};

  /**
   * Dimension of the grid in the visualization
   */
  self.margin = {top: 30, right: 30, bottom: 30, left: 30},
  self.width = 650 - self.margin.left - self.margin.right,
  self.height = 650 - self.margin.top - self.margin.bottom;

  /**
  * SVG Element that will contain the grid
  */
   const createSvg = (divName) => {
    self.container = d3.select(divName)
    .append("svg")
    .attr("width", self.width + self.margin.left + self.margin.right)
    .attr("height", self.height + self.margin.top + self.margin.bottom)
    .append("g")
    .attr("transform", `translate(${self.margin.left},${self.margin.top})`);
   }


  self.displayGrid = (divName) => {

    createSvg(divName)
    
    /**
     * X scale and axis
     */
    const x = d3.scaleBand()
    .range([ 0, self.width ])
    .domain(d3.range(0))
    .padding(0.01);
    self.container.append("g")
    .attr("transform", `translate(0, ${self.height})`)
    .call(d3.axisBottom(x))

    /**
     * Y scale and axis
     */
    const y = d3.scaleBand()
    .range([ 0 , self.height ])
    .domain(d3.range(0))
    .padding(0.01);
    self.container.append("g")
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
          .style("fill", "red")
          .style("opacity", 0.8)
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
          .style("fill", "black")
          .style("opacity", 1)
    }

    //Listener
    const searchbar = function(event)
    {
      const word = document.getElementById("search").value;
      self.container.select('text.'+word).style("fill","green");
      
    }
    /*
        .data(data.filter(d => d.word == word))
        .enter()
        .insert("text")
        .attr("dy", ".35em")
          .attr("x", function(d) { return x(d.col) + self.width/(numcol * 4) })
        .attr("y", function(d) { return y(d.row) + self.height/(numcol * 2) })
        .style("font-size", function(d) { return Math.min(2 / x.bandwidth(), (2 / x.bandwidth() - 8) / this.getComputedTextLength() * 24) + "px"; })
        .style("fill","blue")
        .text(function(d) { return d.word; })
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)
    }*/

    const element = document.getElementById("mybutton");
    element.addEventListener("click", searchbar);

    /**
     * Fill the grid : squares and corresponding word text.
     */
    self.container.selectAll()
      .data(data)
      .enter()
      .append("rect")
        .attr("x", function(d) { return x(d.col) })
        .attr("y", function(d) { return y(d.row) })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", "white" )
        .style("stroke","black")

    self.container.selectAll()
      .data(data)
      .enter()
        .append("text")
        .attr("dy", ".35em")
          .attr("x", function(d) { return x(d.col) + self.width/(numcol * 4) })
        .attr("y", function(d) { return y(d.row) + self.height/(numcol * 2) })
        .style("font-size", function(d) { return Math.min(2 / x.bandwidth(), (2 / x.bandwidth() - 8) / this.getComputedTextLength() * 24) + "px"; })
        .text(function(d) { return d.word; })
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)
    })
  }

  return self;
})();