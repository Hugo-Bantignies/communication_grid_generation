let Grid = (() => {

  let self = {};

  /**
   * Dimension of the main grid in the visualization
   */
  self.main_margin = {top: 30, right: 30, bottom: 30, left: 30},
  self.main_width = 700 - self.main_margin.left - self.main_margin.right;
  self.main_height = 700 - self.main_margin.top - self.main_margin.bottom;

  /**
  * SVG Element that will contain the main grid
  */
   const createMainSvg = (divName) => {
    self.main_container = d3.select(divName)
    .append("svg")
    .attr("width", self.main_width + self.main_margin.left + self.main_margin.right)
    .attr("height", self.main_height + self.main_margin.top + self.main_margin.bottom)
    .append("g")
    .attr("transform", `translate(${self.main_margin.left},${self.main_margin.top})`);
   }

   /**
    * Colorscale for the different pages
    */
   const getPageColors = (data) => {
    const pages = d3.map(data, d => d.page);

    // Eliminate duplicates.
    const keys = [... new Set(pages)];

    //Color scale
    var color_list = [];

    //Generate a random color scale
    for(let i = 0; i < keys.length; i++)
    {
      var r = () => Math.random() * 256 >> 0;
      var color = `rgb(${r()}, ${r()}, ${r()})`;
      color_list.push(color);
    }

    // Associate a color with each key. 
    return colors = d3.scaleOrdinal()
        .domain(keys)
        .range(color_list);
    }

  /**
   * Build a dictionary of pages to get its number
   */

  const buildPageDict = (data) => {
    var page_dict = {}

    const pages = d3.map(data, d => d.page);

    // Eliminate duplicates.
    const keys = [... new Set(pages)];

    for (i = 0; i < keys.length; i++) {
      page_dict[keys[i]] = i
    }
      
    return page_dict
  }


  self.displayGrid = (divName) => {

    createMainSvg(divName)
    
    /**
     * X scale and axis for the main grid
     */
    const x = d3.scaleBand()
    .range([ 0, self.main_width ])
    .domain(d3.range(0))
    .padding(0.01);
    self.main_container.append("g")
    .attr("transform", `translate(0, ${self.main_height})`)

    /**
     * Y scale and axis for the main grid
     */
    const y = d3.scaleBand()
    .range([ 0 , self.main_height ])
    .domain(d3.range(0))
    .padding(0.01);
    self.main_container.append("g")

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

    
    //Number of words / pictograms
    var nbwords = d3.count(data, d => d.row);

    //Dimension of the page grid
    var grid_dim_x = 3;
    var grid_dim_y = 3;

    //Dimension of the page
    var page_dim_x = d3.max(data, d => d.col);
    var page_dim_y = d3.max(data, d => d.row);
    
    var numcol = Math.ceil(Math.sqrt(nbwords)) * grid_dim_x
    var numrow = Math.ceil(Math.sqrt(nbwords)) * grid_dim_x

    const colors = getPageColors(data);
    const page_dict = buildPageDict(data);

    //Information display
    d3.select("#information")
    .text("Number of pictograms : " + nbwords)

    x.domain(d3.range(numcol))
    y.domain(d3.range(numrow))


    // create a tooltip
    const tooltip = d3.select("#pictogram_grid")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

    /**
     * Mouse : Three function that change the wordtip when user hover / move / leave a cell
     */
    const mouseover = function(event,d) {
      d3.select(this)
          .style("fill", "red")
          .style("opacity", 0.7);
      tooltip.style("opacity", 1);
    }

    const mousemove = function(event,d) {
      tooltip
        .html(d.word)
        .style("left", (event.x)/2 + "px")
        .style("top", (event.y)/2 + "px")
    }

    const mouseleave = function(d) {
      tooltip.style("opacity", 0)
      if(self.show_pages_state == true)
      {
        d3.select(this)
            .style("fill", d => colors(d.page))
            .style("opacity", 0.6);
      }
      else{
        d3.select(this)
        .style("fill", "white")
        .style("opacity",1);}
    }


    self.search_mem = null;
    self.show_pages_state = false;

    //Listener of the search bar
    const searchbar = function(event)
    {
      const word = document.getElementById("search").value;

      if(self.search_mem != null && self.search_mem.style.fill != "blue")
        {self.search_mem.style.fill = "white"}
      
      if(word !== "")
      {
        self.search_mem = document.getElementById("r_"+word)
        self.search_mem.style.fill = "green"
        self.search_mem.style.opacity = 0.5
      }
    }

    //Listener of the marker button
    const searchmarker = function(event)
    {
      const word = document.getElementById("search").value;
      var el = document.getElementById("r_"+word);
      el.style.fill = "blue";
      el.style.opacity = 0.7;
    }

    //Listener of the reset button
    const resetmarker = function(event)
    {
      self.main_container.selectAll("rect").style("fill","white").style("opacity",1);
      document.getElementById("search").value = "";
      self.show_pages_state = false;
    }

    //Listener to hollow the pages
    const hollowpages = function(event)
    {
      if(self.show_pages_state == false)
      {self.main_container.selectAll("rect").style("fill",d => colors(d.page)).style("opacity",0.6);
      self.show_pages_state = true;}
      else
      {self.main_container.selectAll("rect").style("fill","white").style("opacity",1);
      document.getElementById("search").value = "";
      self.show_pages_state = false;}
    }

    //Buttons and search bar
    const marker = document.getElementById("markbutton");
    const reset = document.getElementById("resetmark");
    const search_bar = document.getElementById("search");
    const show_pages = document.getElementById("showpages");
    
    //Bind events to the buttons and the search bar
    search_bar.addEventListener('keyup', searchbar);
    marker.addEventListener("click", searchmarker);
    reset.addEventListener("click",resetmarker);
    show_pages.addEventListener("click",hollowpages);

    /**
     * Fill the grid : squares and hollow for pages
     */
    
    self.main_container.selectAll()
      .data(data)
      .enter()
      .append("rect")
        .attr("x", function(d) {
           return x(d.col + (page_dict[d.page]) % grid_dim_x * (page_dim_x + 1)) 
        })
        .attr("y", function(d) {
           return y(d.row + (Math.floor(page_dict[d.page] / grid_dim_x)) * (page_dim_y + 1)) 
        })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .attr("id",function(d) { return "r_"+d.word; })
        .style("fill", "white")
        .style("stroke","black")
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)
        .on("mousemove", mousemove)
        .on("click", searchmarker);
    })
  }

  return self;
})();