

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded:", document.readyState)

  })
let pythonscript = "/api/function1"
const gobutt = document.getElementById("go-button")
const onClickButton = () => {
    gobutt.innerText = "Running...";
    console.log("Skript wurde gestartet!");
    console.log(JSON.stringify($('#inputParams').serialize()));
    alert('Running script');
    $.ajax({url: pythonscript, type: 'POST', success: function(data) {
        console.log("python running")
        if (data) {
          console.log("Returned:", data);
        }

     }})
  }

gobutt.addEventListener("click", onClickButton)

