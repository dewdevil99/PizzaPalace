function topping_change(sel, pizza_id, topping) {
	var current_topping=sel.value;
	console.log(current_topping)
	if(topping=='topping1' || topping=='topping2'){
		var id1='';
		if(topping=='topping1'){
			id1='topping2'.concat(pizza_id);
		}
		else if(topping=='topping2'){
			id1='topping1'.concat(pizza_id);
		}
		var val1=document.getElementById(id1).value;
		var op1=document.getElementById(id1).getElementsByTagName('option');
		var id2='topping3'.concat(pizza_id);
		if(document.getElementById(id2)){
			var val2=document.getElementById(id2).value;
			var op2=document.getElementById(id2).getElementsByTagName('option');
			for (var i = 1; i < op2.length; i++) {
				if(String(op2[i].value)==String(current_topping) || String(op2[i].value)==String(val1)){
					op2[i].disabled=true;
				}
				else{
					op2[i].disabled=false;
				}
			}
			for (var i = 1; i < op1.length; i++) {
				if(String(op1[i].value)==String(current_topping) || String(op1[i].value)==String(val2)){
					op1[i].disabled=true;
				}
				else{
					op1[i].disabled=false;
				}
			}
		}
		else{
			for (var i = 1; i < op1.length; i++) {
				if(String(op1[i].value)==String(current_topping)){
					op1[i].disabled=true;
				}
				else{
					op1[i].disabled=false;
				}
			}
		}
		
	}
	else if(topping=='topping3'){
		var id1='topping1'.concat(pizza_id);
		var val1=document.getElementById(id1).value;
		var id2='topping2'.concat(pizza_id);
		var val2=document.getElementById(id2).value;
		var op1=document.getElementById(id1).getElementsByTagName('option');
		var op2=document.getElementById(id2).getElementsByTagName('option');
		for (var i = 1; i < op1.length; i++) {
			if(String(op1[i].value)==String(current_topping) || String(op1[i].value)==String(val2)){
				op1[i].disabled=true;
			}
			else{
				op1[i].disabled=false;
			}
		}
		for (var i = 1; i < op2.length; i++) {
			if(String(op2[i].value)==String(current_topping) || String(op2[i].value)==String(val1)){
				op2[i].disabled=true;
			}
			else{
				op2[i].disabled=false;
			}
		}
	}
}

function quantity_change(sel, cart_object_id) {
	var fd=new FormData();
	fd.append('new_quantity', sel.value);
	fd.append('cart_item_id', Number(cart_object_id));
	const request=new XMLHttpRequest();
	request.open('POST', '/quantity_update');
	request.onreadystatechange = () => {
		if(request.readyState==4 && request.status==200) {
			window.location.reload();
			return false;
		}
	};
	request.send(fd);
}

function delete_item(cart_object_id) {
	var fd=new FormData();
	fd.append('cart_item_id', Number(cart_object_id));
	const request=new XMLHttpRequest();
	request.open('POST', '/delete_item');
	request.onreadystatechange = () => {
		if(request.readyState==4 && request.status==200) {
			window.location.reload();
			return false;
		}
	};
	request.send(fd);
}