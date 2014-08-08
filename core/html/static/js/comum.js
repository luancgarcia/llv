largura_window = $(window).width();

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

				$(".maskmenu").remove();
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

			header.append("<div class='maskmenu'></div>")
		}
	});

	$("#ico-brs").on({
		click: function(){
			var ico = $(this);
			var ico_menu = $("#ico-menu");
			var html_body = $("html,body");
			var header = $("#Header");
			var banner = $("#Header .head-mob");
			var menu_shp = $("#menu-shoppings");

			var altura_window = $(window).height();

			if(ico.hasClass("ativo")) {
				ico.removeClass("ativo");
				html_body.removeAttr("style");

				banner.animate({
					marginLeft: "0"
				});

				ico_menu.animate({
					marginLeft: "0"
				});

				menu_shp.animate({
					right: "-276px"
				});

				$(".maskmenushp").remove();
				return false;

			}

			ico.addClass("ativo");

			html_body.css({
				"overflow":"hidden",
				"height": altura_window+"px"
			});

			banner.animate({
				marginLeft: "-266px"
			});

			ico_menu.animate({
				marginLeft: "-266px"
			});

			menu_shp.animate({
				right: "0px"
			});

			header.append("<div class='maskmenushp'></div>")
		}
	});

	$(document.body).on({
		tap: function(){
			var ico = $("#ico-menu");
			ico.trigger("click");
		}
	}, ".maskmenu");

	$(document.body).on({
		tap: function(){
			var ico = $("#ico-brs");
			ico.trigger("click");
		}
	}, ".maskmenushp");

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

	// disparaModalRequest("modais/produto","786","");
	// disparaModalRequest("modais/destaque","786","");
	// disparaModalRequest("modais/evento","560","");
	// disparaModalRequest("modais/share","786","share_produto");
	// disparaModalRequest("modais/produto.html","786","");
	//disparaModalRequest("modais/destaque.html","786","");
	// disparaModalRequest("modais/evento.html","560","");

	//abre modal

	$("[rel='modal']").on({
		click: function(){
			var tamanho = $(this).attr('data-param');
			var qualclasse = $(this).attr("data-class");
			var url = $(this).attr('data-href')
			// disparaModalRequest($(this).attr("href"), tamanho, qualclasse);
			disparaModalRequest(url, tamanho, qualclasse);
		}
	});

	// chama modal a partir de outro modal
	$(document.body).on({
		click: function(){
			var tamanho = $(this).attr('data-param');
			var qualclasse = $(this).attr("data-class");
			var url = $(this).attr('data-href')
			fechaModal();
			disparaModalRequest(url, tamanho, qualclasse);
		}
	}, "a.share-modal");

	//fechar modal
	$(document.body).on({
		click: function(){
			fechaModal();
		}
	}, "[data-param='closemodal']");

	// curtir
	$("a.like").on({
		click: function(){
			var link = $(this);
			var id_item = link.attr("data-id");
			$.ajax({
	            type: "POST",
	            url: 'curtir/',
	            dataType: "json",
	            data: {id_item: id_item},
	            beforeSend: function(){
	                // console.log("before send");
	            },
	            success: function(data) {
	                link.text(data.total);
	            },
	            error: function(){
	                console.log("erro curtir");
	            }
	       });
	       return false;
		}
	});

	$(document.body).on({
		click: function(){
			var link = $(this);
			var id_item = link.attr("data-id");
			$.ajax({
	            type: "POST",
	            url: 'curtir/',
	            dataType: "json",
	            data: {id_item: id_item},
	            beforeSend: function(){
	                // console.log("before send");
	            },
	            success: function(data) {
	                link.text(data.total+" pessoas curtiram essa oferta");
	            },
	            error: function(){
	                console.log("erro curtir");
	            }
	       });
	       return false;
		}
	}, "p.curtidas span");

	$(document.body).on({
		click: function(){
			var thumb = $(this);
			var url_thumb = thumb.attr("data-img");
			var img_gde = $("#fotoProduto img");

			img_gde.attr("src", url_thumb);

			return false;
		}
	}, ".thumbs-list  a[data-img]");


	//muda as abas do share
	$(document.body).on({
		click: function(){
			var aba = $(this);
			var qualaba = aba.attr("data-aba");

			var box_aba = $("#ShareProduto .col-opcoes .content-opcoes ul");
			var box_certo = $("#ShareProduto .col-opcoes .content-opcoes ul[data-box='"+qualaba+"']");


			if(largura_window <=480) {
				var qtd_itens = box_certo.children("li").length;
				var largura_itens = box_certo.children("li").outerWidth(true);

				box_certo.width(qtd_itens*largura_itens+10);
			}


			$("#ShareProduto .col-opcoes .abas li").removeClass("ativo");
			aba.parent().addClass("ativo");

			box_aba.hide();
			box_certo.show();

			return false;
		}
	}, "#ShareProduto .col-opcoes .abas li a");

	//poe a foto por cima
	$(document.body).on({
		click: function(){
			var foto = $(this);
			var foto_gd = foto.attr("data-src");
			var foto_id = foto.attr("data-mask");
			var box_foto = $("#foto-share .sec");

			$("#ShareProduto .col-opcoes .content-opcoes li a").removeClass("ativo");
			foto.addClass("ativo");

			$("#foto-share .sec").remove();

			$("#foto-share  div").append("<img src='"+foto_gd+"' class='sec'>");

			$(".bt-share").attr("data-mask",foto_id);

			box_foto.attr("src", foto_gd).show();

			return false;
		}
	}, "#ShareProduto .col-opcoes .content-opcoes li a");

	// limpar foto share
	$(document.body).on({
		click: function(){
			var foto_clear = $("#foto-share .sec");

			foto_clear.remove();

			$(".bt-share").attr("data-mask","");

			return false;
		}

	}, '#ShareProduto .bt-reset');

	// Compartilhar
	$(document.body).on({
		click: function(){
			var botao_share = $('#ShareProduto .bt-share');
			var imagem_id = botao_share.attr("data-base");
			var mascara_id = botao_share.attr("data-mask");
			var id_item = botao_share.attr("data-id");

			$.ajax({
	            type: "POST",
	            url: 'mesclar/',
	            dataType: "json",
	            data: {id_item: id_item, imagem_id: imagem_id, mascara_id: mascara_id},
	            beforeSend: function(){
	                // console.log("before send");
	            },
	            success: function(data) {
	                FB.ui({
					  method: 'feed',
					  // link: "https://apps.facebook.com/llv-dev/",
					  link: "https://jonatascd.pythonanywhere.com/",
					  caption: data.titulo,
					  description: data.descricao,
					  picture: data.imagem,
					  image: data.imagem,
					}, function(response){});
					fechaModal();
	                return false;
	            },
	            error: function(){
	                console.log("erro mesclar");
	            }
	       });
	       return false;
		}

	}, '#ShareProduto .bt-share');

});

$( document ).ready(function() {
	$(window).scroll(function() {
		if($(window).scrollTop() + $(window).height() == $(document).height()) {
			var container = $('.cl.final');
			var ultimo_destaque = container.attr('data-destaque');
			var ultimo_evento = container.attr('data-evento');
			var ultima_oferta = container.attr('data-oferta');
			// console.log(ultimo_destaque,ultimo_evento,ultima_oferta);
			$.ajax({
	            type: "POST",
	            url: 'mais_ofertas/',
	            dataType: "html",
	            data: {ultimo_destaque:ultimo_destaque,ultimo_evento:ultimo_evento,ultima_oferta:ultima_oferta},
	            beforeSend: function(){
	                // console.log("before send");
	            },
	            success: function(data) {
	                $(".grid:last").after(data);
	            },
	            error: function(){
	                console.log("erro enviar");
	            }
	       });
	       return false;
		}
	});
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
			$('body').append("<div class='lightbox preloading'><p class='loading-modal'><img src='static/"+static_url+"/loader-bgescuro.gif' alt='' class='fl' /> <span class='fl'>Carregando</span></p></div>");
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