function bindEventHandlerForMain() {
  let pythonscript = "/api/params"
  const gobutt = document.getElementById("go-button")
  const resbutt = document.getElementById("result")
  resbutt.disabled=true;
  const onClickButton = () => {
      gobutt.innerText = "Running..."
      console.log("Skript wurde gestartet!")
      const itype = document.getElementById("input")
      const inorm = document.getElementById("norm")
      const iit = document.getElementById("it_adj")
      const baselineindex = document.getElementById("baseline")
      let formdata = {input_type:itype.value, normal_method:inorm.value, it_adj:iit.value,base_index:baselineindex.value}
      dataasjson=JSON.stringify(formdata)
      alert('Running script')
      $.ajax({url:pythonscript,dataType: "json",contentType: 'application/json;charset=UTF-8', type:'POST',data:dataasjson, success: function(data) {
          if (data) {
            console.log("Returned:",data)}
            var formData = new FormData();
            formData.append('file', $('input[type=file]')[0].files[0]);
            $.ajax({
              type: 'POST',
              url: '/api/process',
              data: formData,
              contentType: false,
              cache: false,
              processData: false,
              success: function(data) {
                  resbutt.disabled=false;
                  gobutt.innerText="GO"
        }
        })
      }})
    }
  gobutt.addEventListener("click", onClickButton);
}

function tracer(data,length){
  var plotting = []
  let channels = data.columns
  for (var i = 1; i < length;i++){
    channel_name=channels[i]
    
    
    y0=data.iloc({columns:[String(i)]}).values.flat()
    var trace={y:y0, type:'box',boxpoints: false,name:channel_name}
    plotting.push(trace)
  
  }
  return plotting;
}

async function parse_data(data) {
  const TESTER = document.getElementById("tester")
  let df = await dfd.read_csv("/api/get_latest");
  df.describe().print();
  const channels_length = df.columns.length;
  data1=tracer(df,channels_length)
  var layout = {
    colorway : ['#f3cec9', '#e7a4b6', '#cd7eaf', '#a262a9', '#6f4d96', '#3d3b72', '#182844'],
    yaxis:{
      type:'log'
    }
  }
  Plotly.newPlot(TESTER,data1,layout)
  }





