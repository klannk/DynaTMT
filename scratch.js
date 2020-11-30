document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded:", document.readyState)
    
  })
let pythonscript = "http://127.0.0.1:5000/"
const gobutt = document.getElementById("go-button")
const onClickButton = () => {
    gobutt.innerText = "Running..."
    console.log("Skript wurde gestartet!")
    alert('Running script')
    $.ajax({url:pythonscript, type:'POST',success: function(data) {
        console.log("python running")
        if (data) {
          console.log("Returned:",data)}
        
     }})
  }

gobutt.addEventListener("click",onClickButton)

