document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded:", document.readyState)
    
  })
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

    let formdata = {input_type:itype.value, normal_method:inorm.value, it_adj:iit.value}
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
                window.result_data = data;
                
      }
      })  
     }})
    
   
  }



gobutt.addEventListener("click",onClickButton)
