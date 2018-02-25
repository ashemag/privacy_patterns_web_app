var button = document.getElementById('check_all')
button.onclick = function(e) {
  console.log("button clicked"); 
  document.getElementsByTagName("input").checked = true; 
}
