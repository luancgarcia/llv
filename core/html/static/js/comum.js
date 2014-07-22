var largura_window = $(window).width();

$(function(){

	var isiDevice = /ipad|iphone|ipod|android/i.test(navigator.userAgent.toLowerCase());


	$("#ico-menu").on({
		click: function(){
			var ico = $(this);
			var html_body = $("html,body");
			var header = $("#Header");
			var banner = $("#Header .head-mob");
			var menu = $("#Menu");

			var altura_window = $(window).height();

			if(ico.hasClass("ativo")) {
				ico.removeClass("ativo");
				html_body.removeAttr("style");

				banner.animate({
					marginLeft: "0"
				})

				ico.animate({
					marginLeft: "0"
				})

				menu.animate({
					left: "-275px"
				});

				$(".mask").remove();
				return false;

			}

			ico.addClass("ativo");



			html_body.css({
				"overflow":"hidden",
				"height": altura_window+"px"
			});

			banner.animate({
				marginLeft: "265px"
			})

			ico.animate({
				marginLeft: "265px"
			})

			menu.animate({
				left: "0px"
			});

			header.append("<div class='mask'></div>")
		}
	});

	$(document.body).on({
		tap: function(){
			var ico = $("#ico-menu");
			ico.trigger("click");
		}
	}, ".maskmenu");

	$(".item-menu .lnk").on({
		click: function(){
			var link = $(this);
			var item = link.parent();
			var submenu = $(".submenu", item);
			var all_subs = $(".item-menu .submenu");
			var all_link = $(".item-menu .lnk");


			if(link.hasClass("ativo")) {
				link.removeClass("ativo");
				submenu.slideUp();

				return false;
			}

			all_subs.slideUp();
			all_link.removeClass("ativo");

			link.addClass("ativo");
			submenu.slideDown();
		}
	});

	disparaModalRequest("modais/produto.html","786","");
	//disparaModalRequest("modais/destaque.html","786","");
	// disparaModalRequest("modais/evento.html","560","");

	//abre modal

	$("[rel='modal']").on({
		click: function(){
			var tamanho = $(this).attr('data-param');
			var qualclasse = $(this).attr("data-class");



			disparaModalRequest($(this).attr("href"), tamanho, qualclasse);
		}
	});

	//fechar modal
	$(document.body).on({
		click: function(){
			fechaModal();
		}
	}, "[data-param='closemodal']");

});



//FUNCAO PRA ABRIR O LIGHTBOX POR AJAX
function exibirConteudo(conteudo, tamanho, qualclasse) {



	$('body').append("<div id='lightbox' class="+qualclasse+">"
	+"  <div class='mask' data-param='closemodal'></div>"
	+       "<div class='lightbox' style='width:"+ tamanho +"px; margin-left:-"+ tamanho/2 +"px;'>"
	+"          <a href='javascript:;' class='fechar_modal rpl' data-param='closemodal' title='fechar'>fechar</a>"
	+"          <div id='ligbtox_content' class='fix'></div>"
	+"      </div>"
	+"  </div>");

	$('#ligbtox_content').append(conteudo);
}

/*Usado para carregar o lightbox a partir de uma url*/

// PASSA UMA URL PRO LIGHTBOX ABRIR
function disparaModalRequest(url, tamanho, qualclasse) {
	// console.log("disparaModalRequest: "+url+"|"+tamanhp);

	if(largura_window <= 480){
				tamanho = "320";
			}
	$.ajax({
		url: url,
		data:'html',
		beforeSend: function(){
			$('body').append("<div class='lightbox preloading'><p class='loading-modal'><img src='/static/"+static_url+"loader-bgescuro.gif' alt='' class='fl' /> <span class='fl'>Carregando</span></p></div>");
			// return false;
		},
		success: function(conteudo){
			$(".lightbox").remove();
			$("body, html").css("overflow","hidden");
			exibirConteudo(conteudo, tamanho, qualclasse);
		}
	});

	return false;
}

// FECHA O MODAL AJAX
function fechaModal() {
	$("body").find("#lightbox").fadeTo("normal", 0, function(){
		$(this).remove().hide();
		$("body, html").removeAttr("style");
	});
}