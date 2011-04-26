window.onload = function() {
	$('#middle-column').find(".picture").find("a").remove();

	var tabela = $('#layout-table');
	var lc = $('#left-column');
	var mc = $('#middle-column');
	var rc = $('#right-column');
	var nav = $('.navbar');
	if (lc.length!=0 && mc.length!=0) {
		var nl = '240';
		var lside = $(lc).find('.sideblock');
		var rside = $(rc).find('.sideblock');

		if (lside.length==1 && $(lside).filter('.tempblockhandler').length!=0) {
			//shrink empty left column
			nl = '50';
			$(lc).css({'width':nl+'px','paddingRight':'0px'});
		}
		if (rside.length==1 && $(rside).filter('.tempblockhandler').length!=0) {
			//shrink empty right column
			$(rc).css({'width':'50px','paddingLeft':'0px'});
		}

		$(tabela).css({'marginTop':'-43px'});
		$(mc).css('paddingTop','50px');
		$(nav).css({'marginLeft':nl+'px','position':'relative','z-index':'100'});
		if (rc.length!=0) {
			$(rc).css('paddingTop','57px');
		}
	}
	if (lc.length==0 && mc.length!=0) {
		$(tabela).css('marginTop','5px');
		if (rc.length!=0) {
			$(rc).css('paddingTop','7px');
		}
	}

	$(".forumpost").each(function(){
		var data = $(".author", this).text().split(",")[1].replace(/[\ ]+/, " ").split(" ");
		var daydiv = document.createElement('div');
		daydiv.setAttribute('class',"day");
		if(data[1].length==1)
		{
			data[1]="0"+data[1];
		}
		daydiv.innerHTML = data[1];
		var monthdiv = document.createElement('div');
		monthdiv.setAttribute('class',"month");
		monthdiv.innerHTML = data[2];
		var avatar = $(".picture",this);
		avatar.append(daydiv);
		avatar.append(monthdiv);
	});
};
