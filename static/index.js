// <-----------------Hide the help text not required in form --------------------->
var x =   document.getElementsByClassName("helptext")



console.log("working");
// <-------------------------  Handling the due date logic  --------------------->  




var submit_btn = document.getElementById('add_task')
submit_btn.addEventListener('click', function(e){
    var duedate= document.getElementById('id_due_date').value
    var duedatas= new Date(duedate)
  var date = new Date()
if(duedatas <= date){
    e.preventDefault()
    alert('Due date cant be less than current date ')
}
if(duedatas===null){
  e.preventDefault()
  alert("Enter due date ")
}
})