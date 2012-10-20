
var FGx = {};
FGx.msgCt = null;

FGx.createBox = function (t, s){
	return ['<div class="msg">',
			'<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
			'<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc"><h3>', t, '</h3>', s, '</div></div></div>',
			'<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
			'</div>'].join('');
}

FGx.msg = function(title, body, tim){
	// @todo: pete
	return;
	if(!FGx.msgCt){
		FGx.msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
	}
	FGx.msgCt.alignTo(document, 't-t');
	//var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
	var m = Ext.DomHelper.append(FGx.msgCt, {html: FGx.createBox(title, body)}, true);
	var Timmy = tim > 0 ? tim : 3;
	m.slideIn('t', {duration: 500}).pause(Timmy * 1000).ghost("t", {remove:true});
}


var VP;

function display_map(){
		
	VP = new FGx.MainViewport();
	//console.log("VP");
	
}


