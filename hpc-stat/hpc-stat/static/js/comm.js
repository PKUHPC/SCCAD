function gotoTop(min_height){

    var gotoTop_html = '<div id="gotoTop"><i class="fa fa-angle-up fa-2x"></i></div>';

    $(gotoTop_html).insertBefore(".footer");
    $("#gotoTop").click(
        function(){$('html,body').animate({scrollTop:0},700);
    }).hover(
        function(){$(this).addClass("hover");},
        function(){$(this).removeClass("hover");
    });

    min_height ? min_height = min_height : min_height = 600;
    $(window).scroll(function(){
        var s = $(window).scrollTop();
        if( s > min_height){
            $("#gotoTop").fadeIn(100);
        }else{
            $("#gotoTop").fadeOut(200);
        };
    });
}

function showRandomSmImage(){
	var idx = Math.ceil(Math.random()*9);
	$(".introTitImg").css("background-image","url(/img/img_small"+idx+".jpg)");
}

function showRandomBigImage(){
	var idx = Math.ceil(Math.random()*30);
	$(".bouti-link-intro").css("background-image","url(/img/img_gxn1"+idx+".jpg)");
}

$(function(){
    $(".header .logo a:first-child").hover(function(){
    $(this).children("img").attr("src","/img/pkulogo_grey.png");
    },function(){$(this).children("img").attr("src","/img/pkulogo_red.png");});
	showRandomSmImage()
	showRandomBigImage()
        $("a.current").removeClass("current");
	if(location.pathname.substring(0,8) == "/achieve"){
		$("#achievement").addClass("current");
	}else{
		$("#stat").addClass("current");
	}

	if(location.pathname.substring(1,5) == "auth"){
		$("section.nav").html("")
		$("[href$='/hpclogin.jsp']").html("")
	} else {
		$(".ssubNav .navline").click(function(){
			if($("#mobileNav").css("display")=="none")
			{
				$("#navline_1").addClass("navline1");
				$("#navline_2").addClass("navline2");
				$("#navline_3").addClass("navline3");
			}else{
				$("#navline_1").removeClass("navline1");
				$("#navline_2").removeClass("navline2");
				$("#navline_3").removeClass("navline3");
			}
			$("#mobileNav").toggle(300);
		});
		$(".header .nav #nav li").hover(function(){
			$(this).children("ul").slideDown(200);
			},
			function(){
				$(this).children("ul").slideUp(200);
			}
		);
	}

	$("header a").each(function(){
		if($(this).attr("href").substring(0,4) != "http" && $(this).attr("href").substring(0,1) != "/"){
			$(this).attr("href","/"+$(this).attr("href").replace(" ",""))
		}
	})
	gotoTop();
})
