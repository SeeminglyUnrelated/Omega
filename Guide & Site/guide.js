/* Set the width of the side navigation to 250px */

function openNav(e = null) {
	if (!e || (e && e.keyCode === 13)){
  	document.getElementById("mySidenav").style.width = "250px";
  	document.getElementById("main").style.marginLeft = "250px";
  }
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

function popup(text) {
  var popup = document.getElementById(text);
  popup.classList.toggle("show");
}