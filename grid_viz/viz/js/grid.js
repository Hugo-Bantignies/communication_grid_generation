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
 
   self.zoom_row = 5;
   self.zoom_col = 5;

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
      .attr("height", self.zoom_height + self.zoom_margin.top + self.zoom_margin.bottom + 100)
      .append("g")
      .attr("transform", `translate(${self.zoom_margin.left},${self.zoom_margin.top})`)
      .style("opacity",0);
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
    createZoomSvg(divName)
    
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

    
    //Number of words / pictograms
    var nbwords = d3.count(data, d => d.row);
    
    //Dimension of the page
    var page_dim_x = d3.max(data, d => d.col) + 1;
    var page_dim_y = d3.max(data, d => d.row) + 1;

    //Dimension of the page grid
    var grid_dim_x = Math.ceil(Math.ceil(Math.sqrt(nbwords)) / page_dim_x);
    var grid_dim_y = Math.ceil(Math.ceil(Math.sqrt(nbwords)) / page_dim_y);
    
    var numcol = page_dim_x * grid_dim_x
    var numrow = page_dim_y * grid_dim_y

    const colors = getPageColors(data);
    const page_dict = buildPageDict(data);

    //Domain of the zoom grid
    x.domain(d3.range(numcol))
    x_zoom.domain(d3.range(self.zoom_row))
    y.domain(d3.range(numrow))
    y_zoom.domain(d3.range(self.zoom_col))

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
      self.zoom_container.style("opacity", 1)
      d3.select(this)
          .style("fill", "red")
          .style("opacity", 0.7);
      tooltip.style("opacity", 1);
    }

    /**
     * Functon to display the zoom grid of the selected word
     */
     const zoomGrid = function(event,d) {

      //Text to modify
      var text; var rect;
      var zoom_text; var zoom_r;

      for(let i = 0; i < data.length; i++)
      {
        if(data[i].page == d.page)
        {
          /*MAIN INFORMATION*/

          //Get the text and identifier
          text = data[i].word;
          id = "r_"+text+data[i].page;
          //Get the color of the pictogram
          rect = document.getElementById(id);
          rect_col = rect.style.fill;

          text = data[i].word;
        
          /*ZOOM INFORMATION*/
          zoom_text = document.getElementById("text"+((data[i].row * (page_dim_x))+ data[i].col));
          zoom_r = document.getElementById("rect"+((data[i].row * (page_dim_x))+ data[i].col));

          zoom_text.textContent = text;
          zoom_r.style.fill = rect_col;
          zoom_r.style.opacity = rect.style.opacity;

          document.getElementById("page_name").textContent = "Page : "+d.page;
        }
      }


    }

    const mousemove = function(event,d) {
      tooltip
        .html(d.word)
        .style("left", (event.x)/2 + "px")
        .style("top", (event.y)/2 + "px")

      zoomGrid(event,d)
    }

    const mouseleave = function(d) {
      self.zoom_container.style("opacity", 0)
      self.zoom_container.selectAll("rect").style("fill",d => "white")
      self.zoom_container.selectAll("text").text("")
      tooltip.style("opacity", 0)
      if(self.show_pages_state == true)
      {
        d3.select(this)
            .style("fill", d => colors(d.page))
            .style("opacity", 0.5);
      }
      else{
        d3.select(this)
        .style("fill", "white")
        .style("opacity",1);}
    }


    self.search_mem = [];
    self.show_pages_state = false;

    //Listener of the search bar
    const searchbar = function(event)
    {
      const word = document.getElementById("search").value;

      for (var i = 0; i < self.search_mem.length; i++) {
        if(self.search_mem[i] != null && self.search_mem[i].style.fill != "blue")
          if(self.show_pages_state)
            {self.main_container.select("#"+self.search_mem[i].id).style("fill",d => colors(d.page)).style("opacity",0.5);}
          else
            {self.search_mem[i].style.fill = "white"}
      }
      
      if(word !== "")
      {
        self.search_mem = document.getElementsByName(word);
        for (var i = 0; i < self.search_mem.length; i++) {
          self.search_mem[i].style.fill = "green";
          self.search_mem[i].style.opacity = 0.5;
        }
      }
    }

    //Listener of the marker button
    const searchmarker = function(event)
    {
      const word = document.getElementById("search").value;
      var elements = document.getElementsByName(word);
      elements.forEach(function (item, index) {
        item.style.fill = "blue";
        item.style.opacity = 0.7;
      });
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
      {self.main_container.selectAll("rect").style("fill",d => colors(d.page)).style("opacity",0.5);
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
           return x(d.col + (page_dict[d.page] % grid_dim_x) * (page_dim_x)) 
        })
        .attr("y", function(d) {
           return y(d.row + (Math.floor(page_dict[d.page] / grid_dim_y)) * (page_dim_y)) 
        })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .attr("id",function(d) { return "r_"+d.word+d.page; })
        .attr("name",function(d) {return d.word})
        .style("fill", "white")
        .style("stroke","black")
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)
        .on("mousemove", mousemove)
    
    const zoom_rect = d3.range(self.zoom_row*self.zoom_col);

    self.zoom_container.append("text").text("").attr("id","page_name").attr("y",-4).attr("x",550/2 - 50)

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