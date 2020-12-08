let original_data;

function bindEventHandlerForMain() {
  /* This function binds events to the GO Button in the Params.jinja HTML file. It first sends a request submitting the analysis parameters to the python server,
  upon success it POSTs the file to the python server, that then gets processed.*/

  const gobutt = document.getElementById("go-button");
  const resbutt = document.getElementById("result");
  resbutt.disabled = true;
  const onClickButton = () => {
    gobutt.innerText = "Running...";
    console.log("Skript wurde gestartet!");
    const itype = document.getElementById("input");
    const inorm = document.getElementById("norm");
    const iit = document.getElementById("it_adj");
    const baselineindex = document.getElementById("baseline");
    let formdata = {
      input_type: itype.value,
      normal_method: inorm.value,
      it_adj: iit.value,
      base_index: baselineindex.value,
    };
    dataasjson = JSON.stringify(formdata);

    $.ajax({
      url: "/api/params",
      dataType: "json",
      contentType: "application/json;charset=UTF-8",
      type: "POST",
      data: dataasjson,
      success: function (data) {
        if (data) {
          console.log("Returned:", data);
        }
        var formData = new FormData();

        formData.append("file", $("input[type=file]")[0].files[0]);
        original_data = formData;
        $.ajax({
          type: "POST",
          url: "/api/process",
          data: formData,
          contentType: false,
          cache: false,
          processData: false,
          success: function (data1) {
            resbutt.disabled = false;
            gobutt.innerText = "GO";
            let returned_data = JSON.parse(data1);

            stats_heavy = returned_data;
            console.log(stats_heavy);
          },
        });
      },
    });
  };
  gobutt.addEventListener("click", onClickButton);
}

function bindEventHandlerForMain_TPP() {
  /* This function binds events to the GO Button in the Params_TPP.jinja HTML file. It first sends a request submitting the analysis parameters to the python server,
  upon success it POSTs the file to the python server, that then gets processed.*/
  let pythonscript = "/api/params_TPP";
  const gobutt = document.getElementById("go-button");
  const resbutt = document.getElementById("result");
  resbutt.disabled = true;
  const onClickButton = () => {
    gobutt.innerText = "Running...";
    console.log("Skript wurde gestartet!");
    const itype = document.getElementById("input");
    const inorm = document.getElementById("norm");
    const iit = document.getElementById("it_adj");

    let formdata = {
      input_type: itype.value,
      normal_method: inorm.value,
      it_adj: iit.value,
    };
    dataasjson = JSON.stringify(formdata);

    $.ajax({
      url: pythonscript,
      dataType: "json",
      contentType: "application/json;charset=UTF-8",
      type: "POST",
      data: dataasjson,
      success: function (data) {
        if (data) {
          console.log("Returned:", data);
        }
        var formData = new FormData();
        formData.append("file", $("input[type=file]")[0].files[0]);
        $.ajax({
          type: "POST",
          url: "/api/process_TPP",
          data: formData,
          contentType: false,
          cache: false,
          processData: false,
          success: function (d1) {
            console.log("Bar");
            resbutt.disabled = false;
            gobutt.innerText = "GO";
            let returned_data = JSON.parse(d1);
            stats_light = JSON.parse(returned_data["light"]);
            stats_heavy = JSON.parse(returned_data["heavy"]);
            console.log(stats_heavy);
            console.log(stats_light);
          },
          error: function (xhr, status, error) {
            alert(xhr.responseText);
          },
        });
      },
    });
  };
  gobutt.addEventListener("click", onClickButton);
}

function boxplots(data, length) {
  /*This function reads in dataframes from Danfo.js and produces plotly traces for each column for a boxplot.
   */
  var plotting = [];
  let channels = data.columns;
  for (var i = 1; i < length; i++) {
    channel_name = channels[i];

    y0 = data.iloc({ columns: [String(i)] }).values.flat();
    var trace = {
      y: y0,
      type: "box",
      boxpoints: "outliers",
      name: channel_name,
    };
    plotting.push(trace);
  }
  return plotting;
}

async function parse_data(data) {
  /*
  This function puts a request to the python server returning the File in the TEMP Folder (mePROD output). The file is read with Danfo.js that returns a pandas like Dataframe 
  It prints summary statistics in the console (just for trial). It uses the tracer() function to create Plotly traces for each channel for a plot that is then pushed to 
  the HTML DOM. 
  */
  const TESTER = document.getElementById("tester");
  let df = await dfd.read_csv("/api/get_latest");
  const channels_length = df.columns.length;
  data1 = boxplots(df, channels_length);
  var layout = {
    colorway: [
      "#f3cec9",
      "#e7a4b6",
      "#cd7eaf",
      "#a262a9",
      "#6f4d96",
      "#3d3b72",
      "#182844",
    ],
    yaxis: {
      type: "log",
    },
  };
  Plotly.newPlot(TESTER, data1, layout);
}

async function parse_data_TPP_light(data) {
  /*
  This function puts a request to the python server returning the File in the TEMP Folder (Light). The file is read with Danfo.js that returns a pandas like Dataframe 
  It prints summary statistics in the console (just for trial). It uses the tracer() function to create Plotly traces for each channel for a plot that is then pushed to 
  the HTML DOM. 
  */
  const TESTER = document.getElementById("tester");
  let df = await dfd.read_csv("/api/get_latest_TPP_light");
  const channels_length = df.columns.length;
  data1 = boxplots(df, channels_length);
  var layout = {
    colorway: [
      "#f3cec9",
      "#e7a4b6",
      "#cd7eaf",
      "#a262a9",
      "#6f4d96",
      "#3d3b72",
      "#182844",
    ],
    yaxis: {
      type: "log",
    },
  };
  Plotly.newPlot(Light, data1, layout);
}

async function parse_data_TPP_heavy(data) {
  /*
  This function puts a request to the python server returning the File in the TEMP Folder (Heavy). The file is read with Danfo.js that returns a pandas like Dataframe 
  It prints summary statistics in the console (just for trial). It uses the tracer() function to create Plotly traces for each channel for a plot that is then pushed to 
  the HTML DOM. 
  */
  const TESTER = document.getElementById("tester");
  let df = await dfd.read_csv("/api/get_latest_TPP_heavy");
  const channels_length = df.columns.length;
  data1 = boxplots(df, channels_length);
  var layout = {
    colorway: [
      "#f3cec9",
      "#e7a4b6",
      "#cd7eaf",
      "#a262a9",
      "#6f4d96",
      "#3d3b72",
      "#182844",
    ],
    yaxis: {
      type: "log",
    },
  };
  Plotly.newPlot(Heavy, data1, layout);
}

function populate_select() {
  $.ajax({
    url: "/api/populate_select",
    success: function (arr) {
      selector = document.getElementById("result_selector");
      let parsed_dirs = JSON.parse(arr);
      console.log(parsed_dirs);
      for (let i = 0; i < parsed_dirs.length; i++) {
        let opt = document.createElement("option");
        opt.index = parsed_dirs[i];
        opt.innerText = parsed_dirs[i];
        selector.appendChild(opt);
      }
    },
  });
}

function get_result_type(cb) {
  let result_to_show = document.getElementById("result_selector").value;
  let dataasjson = JSON.stringify({ result: result_to_show });
  $.ajax({
    url: "/api/result_type",
    data: dataasjson,
    dataType: "json",
    contentType: "application/json;charset=UTF-8",
    type: "POST",
    data: dataasjson,
    success: function (data) {
      const datatype = data["type"];
      if (datatype == "mePROD") {
        //Return mePROD file
        console.log("DataType:", datatype);
        cb(datatype);
      } else if (datatype == "pSILAC") {
        //Return pSILAC files
        console.log("DataType:", datatype);
        cb(datatype);
      } else {
        alert("ERROR in filetype");
      }
    },
  });
}

function get_result(cb) {
  get_result_type(function(dtype){
    let result_to_show = document.getElementById("result_selector").value;
  
    console.log(dtype);
    let data_json = JSON.stringify({ result: result_to_show, type: dtype });
    console.log(data_json);
    $.ajax({
      url: "/api/get_defined_result",
      data: data_json,
      dataType: "json",
      contentType: "application/json;charset=UTF-8",
      type: "POST",

      success: function (df) {
        return_data = df
        if (dtype == "mePROD") {

          console.log(return_data);
          cb(return_data, dtype)
        } else if (dtype == "pSILAC") {
          console.log(return_data);
          cb(return_data, dtype)
          //Parse as pSILAC
        } else {
          alert("ERROR in filetype");
        };
        
      },
    });
    
    })
  
}

function plotImpl(df, dtype){
  console.log(dtype)
  if (dtype == 'mePROD'){
    document.getElementById("abundances").style.display = "block"
       
    let dataframe = new dfd.DataFrame(df['Data']);
    
    const Cont_01 = document.getElementById("plot_container_01");

    
    const channels_length = dataframe.columns.length;
    box_plot_data = boxplots(dataframe, channels_length);
    var layout_box = {
      colorway: [
        "#f3cec9",
        "#e7a4b6",
        "#cd7eaf",
        "#a262a9",
        "#6f4d96",
        "#3d3b72",
        "#182844",
      ],
      yaxis: {
        type: "log",
      },
    };
    Plotly.newPlot(Cont_01, box_plot_data, layout_box);
    //Plot stats//
    if (df['stats'] == 'yes'){
      document.getElementById("statistics").style.display = "block"
      let statistics_light = new dfd.DataFrame(df['stats_light']);
      let statistics_heavy = new dfd.DataFrame(df['stats_heavy']);
      statistics_light.columns = df['stats_columns']
      console.log(statistics_light.columns)
    }
  }
}


function plot_results(event){
  get_result(function (df, dtype) {
    plotImpl(df, dtype)
  })
}

async function visualize_page_plotter() {
  const vis_butt = document.getElementById("vis_button");
  vis_butt.addEventListener("click", plot_results);
}

function violinplots(data, length) {
  /*This function reads in dataframes from Danfo.js and produces plotly traces for each column for a boxplot.
   */
  var plotting = [];
  let channels = data.columns;
  for (var i = 1; i < length; i++) {
    channel_name = channels[i];

    y0 = data.iloc({ columns: [String(i)] }).values.flat();
    var trace = { y: y0, type: "violin", boxpoints: false, name: channel_name };
    plotting.push(trace);
  }
  return plotting;
}
