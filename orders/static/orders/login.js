document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('#main_window').style.height=window.innerHeight-60 + "px";
	console.log(window.innerHeight);
});

window.addEventListener("resize", () => {
	document.querySelector('#main_window').style.height=window.innerHeight-60 + "px";
	console.log(window.innerHeight);
},false);