var targets = document.getElementsByClassName('standout');

function perspextive(x, y) {
	var reduction = 8,
		max = 7, 
		w = document.documentElement.clientWidth,
		h = document.documentElement.clientHeight,
		wmid = w / 2,
		hmid = h / 2,
		offsetX = (wmid - x) / reduction,
		offsetY = (hmid - y) / reduction,
		w100 = x / w * 100,
		y100 = y / h * 100;
		w100 = Math.round(w100);
		y100 = Math.round(y100);

		if (offsetX > max) offsetX = max;
		if (offsetY > max) offsetY = max;
		if (offsetX < -max) offsetX = -max;
		if (offsetY < -max) offsetY = -max;
console.log('y',y,'h',h,'Y',offsetY,'y100',y100);
	Array.prototype.forEach.call(targets, function(el) {
		el.setAttribute('style', 'text-shadow:'+offsetX+'px '+offsetY+'px 10px rgba(51, 51, 51, 0.2);background:radial-gradient(circle at '+w100+'% '+y100+'%, #7999d0, #003d6c);-webkit-background-clip: text;-webkit-text-fill-color: transparent');
	});
}

window.addEventListener('mousemove', function(e) {
	var x = e.pageX,
		y = e.pageY;

	perspextive(x, y);
});
window.addEventListener('devicemotion', function(e) {
	var x = e.accelerationIncludingGravity.x * 100;
    var y = e.accelerationIncludingGravity.y * 100;

	perspextive(x, y);
});