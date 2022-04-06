let Grid = (() => {

  let self = {};

  /**
   * Dimension of the main grid in the visualization
   */
  self.main_margin = {top: 30, right: 30, bottom: 30, left: 30},
  self.main_width = 700 - self.main_margin.left - self.main_margin.right;
  self.main_height = 700 - self.main_margin.top - self.main_margin.bottom;

  /**
   * Dimension of the zoom grid in the visualization 
   */
  self.zoom_margin = {top:15, right: 15, bottom: 15, left: 15}
  self.zoom_width = 550 - self.zoom_margin.left - self.zoom_margin.right;
  self.zoom_height = 550 - self.zoom_margin.top - self.zoom_margin.bottom;

  self.zoom_row = 7;
  self.zoom_col = 7;

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
    * SVG Element that will contain the zoom grid
    */
   const createZoomSvg = (divname) => {
     self.zoom_container = d3.select(divname)
     .append("svg")
     .attr("width", self.zoom_width + self.zoom_margin.left + self.zoom_margin.right)
     .attr("height", self.zoom_height + self.zoom_margin.top + self.zoom_margin.bottom)
     .append("g")
     .attr("transform", `translate(${self.zoom_margin.left},${self.zoom_margin.top})`);
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


  self.displayGrid = (divName) => {

    createMainSvg(divName)
    createZoomSvg("#wordtip")
    
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
     * X scale and axis for the zoom grid
     */
     const x_zoom = d3.scaleBand()
     .range([ 0, self.zoom_width ])
     .domain(d3.range(0))
     .padding(0.01);
     self.zoom_container.append("g")
     .attr("transform", `translate(0, ${self.zoom_height})`)

    /**
     * Y scale and axis for the main grid
     */
    const y = d3.scaleBand()
    .range([ 0 , self.main_height ])
    .domain(d3.range(0))
    .padding(0.01);
    self.main_container.append("g")


    /**
     * Y scale and axis for the zoom grid
     */
     const y_zoom = d3.scaleBand()
     .range([ 0 , self.zoom_height ])
     .domain(d3.range(0))
     .padding(0.01);
     self.zoom_container.append("g")

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
    var maxlength = d3.max(data, d => d.word.length);
    var nbwords = d3.count(data, d => d.row);

    const colors = getPageColors(data);

    //Information display
    d3.select("#information")
    .text("Number of words : " + nbwords + "  (" + numrow + "x" + numcol + ")"); 

    x.domain(d3.range(numcol))
    x_zoom.domain(d3.range(self.zoom_row))
    y.domain(d3.range(numrow))
    y_zoom.domain(d3.range(self.zoom_col))

    /**
     * Mouse : Three function that change the wordtip when user hover / move / leave a cell
     */
    const mouseover = function(event,d) {
      self.zoom_container.style("opacity", 1)
      d3.select(this)
          .style("fill", "red")
          .style("opacity", 0.7)
    }

    const mouseleave = function(d) {
      self.zoom_container.style("opacity", 0)
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

    /**
     * Functon to display the zoom grid of the selected word
     */
    const zoomGrid = function(event,d) {

      //Text to modify
      var text;

      //Apply the filter from the middle
      for(let i = -Math.floor(self.zoom_row/2); i < Math.ceil(self.zoom_row / 2); i++)
      {
        for(let j = -Math.floor(self.zoom_col/2); j < Math.ceil(self.zoom_col / 2); j++)
        {

          //Get the text
          text = document.getElementById("text"+((i+Math.floor(self.zoom_row/2)) 
                                                    * self.zoom_col + (j+Math.floor(self.zoom_col/2))));

          //Get the rect
          rect = document.getElementById("rect"+((i+Math.floor(self.zoom_row/2)) 
                                                    * self.zoom_col + (j+Math.floor(self.zoom_col/2))));

          var p_row = d.row + i;
          var p_col = d.col + j;
          
          //If not out of bounds
          if(p_row >= 0 && p_col >= 0 && p_row < numrow && p_col < numcol && ((p_row * numcol + p_col) < nbwords))
          {
            word = data[(p_row * numcol)+ p_col].word
            text.textContent = word;

            rect_color = document.getElementById("r_"+word).style.fill;
            rect.style.fill = rect_color;
          }
          //If out of bounds
          else{
            text.textContent = "";
            rect.style.fill = "white";
          }
        }
      }
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
        self.zoom_container.style("opacity", 1)
        self.search_mem = document.getElementById("r_"+word)
        self.search_mem.style.fill = "green"
        self.search_mem.style.opacity = 0.5
        for(let i = 0; i < nbwords; i++)
        {
          if(data[i].word == word)
          {
            zoomGrid(event,data[i]);
          }
        }
      }
      else {self.zoom_container.style("opacity", 0)}
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
      self.main_container.selectAll("rect").style("fill",d => colors(d.page)).style("opacity",0.6);
      self.show_pages_state = true;
    }

    //Events for the search bar and the marking buttons
    const marker = document.getElementById("markbutton");
    const reset = document.getElementById("resetmark");
    const search_bar = document.getElementById("search");
    const show_pages = document.getElementById("showpages")
    
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
        .attr("x", function(d) { return x(d.col) })
        .attr("y", function(d) { return y(d.row) })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .attr("id",function(d) { return "r_"+d.word; })
        .style("fill", "white")
        .style("stroke","black")
        .on("mouseover", mouseover)
        .on("mousemove", zoomGrid)
        .on("mouseleave", mouseleave)

      const zoom_rect = d3.range(self.zoom_row*self.zoom_col);

      self.zoom_container.selectAll()
        .data(zoom_rect)
        .enter()
        .append("rect")
          .attr("x", function(d) { return x_zoom(d%self.zoom_row); })
          .attr("y", function(d) { return y_zoom(Math.floor(d/self.zoom_col)); })
          .attr("width", x_zoom.bandwidth() )
          .attr("height", y_zoom.bandwidth() )
          .attr("id",function(d) {return "rect"+d})
          .style("stroke","black")
          .style("fill","white")
          .style("opacity",0.7)

      self.zoom_container.selectAll()
      .data(zoom_rect)
      .enter()
        .append("text")
        .attr("dy", ".35em")
          .attr("x", function(d) { return x_zoom(d%self.zoom_row) + self.zoom_width/(self.zoom_row * 4) })
        .attr("y", function(d) { return y_zoom(Math.floor(d/self.zoom_col)) + self.zoom_height/(self.zoom_col * 2) })
        .attr("id",function(d) {return "text"+d})
        .style("font-size", 11)
        .text("")
    })
  }

  return self;
})();