document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded:", document.readyState)
    TESTER = document.getElementById('tester');
	
    $.ajax({url:"/api/get_latest",
    dataType: "json",
    contentType: 'application/json;charset=UTF-8',
    type:'GET', 
    success: function(data) {
        if (data) {
            console.log(data);
        }
    }
})
        }
    );




