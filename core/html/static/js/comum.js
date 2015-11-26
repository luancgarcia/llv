largura_window = $(window).width();
url_connect = (window.location != window.parent.location) ? document.referrer: document.location;
var url_hash = window.location.hash;
url_slug = url_hash.replace('#', '');

logado_fb = false;
negado_fb = false;

function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++) {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name) {
            return unescape(y);
        }
    }
    return undefined;
}

function setCookie(c_name,value) {
    if (typeof(value) != "undefined") {
//        document.cookie=c_name + "=" + value + ";domain="+site_url+";path=/";
        document.cookie=c_name + "=" + value + ";path=/";
    } else {
        document.cookie=c_name + "='';expires=01-Jan-1970 00:00:01 GMT;path=/";
    }
}

function validaEmail(email) {
    if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))) {
        return false;
    }else {
        return true;
    }
}

function validaCampo(campo){
    if(campo.val() =="") {
        return false;
    }else {
        return true;
    }
}

function fecharTutorial() {
    setCookie("gettutorial","1");
	$("#TutorialMob").remove();
}

function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.log('Query variable %s not found', variable);
}
//console.log(getQueryVariable('code'));

function logadoFacebook(){
//    console.log(navigator.userAgent);
    if (!logado_fb) {
        if (window.name.indexOf('app_runner_fb') >= 0) {
            FB.login(function (response) {
                if (response.authResponse) {
                    console.log('Welcome!  Fetching your information.... ');
                    FB.api('/me', function (response) {
                        console.log('Good to see you, ' + response.name + '.');
		        fb_user_id = response.id;
                        //$('p.user span').text(response.name);
                        // $('p.user img').attr('src','https://graph.facebook.com/'+response.id+'/picture?type=small');
                    });
                    logado_fb = true;
                } else {
                    console.log('User cancelled login or did not fully authorize.');
                }
            }, {
                scope: 'publish_actions',
                return_scopes: true
            });
        } else {
            if (navigator.userAgent.match('CriOS') || /windows phone|lumia/i.test(navigator.userAgent.toLowerCase())) {
                //        window.open('https://www.facebook.com/dialog/oauth?client_id=705413109545842&redirect_uri='+ document.documentURI +'', '', null);
                console.log('siiiimmmmmmm windows phone');
                disparaModalRequest("/modal_fb_login_chrome_ios", "300", "");
            } else {
                FB.getLoginStatus(function (response) {
                    if (response.status === 'connected') {
                        //var uid = response.authResponse.userID;
                        //var accessToken = response.authResponse.accessToken;
                        console.log('siiiimmmmmmm chrome');
                        logado_fb = true;
                        return true;
                    } else if (response.status === 'not_authorized') {
                        negado_fb = true;
                        logado_fb = true;
                        //              console.log('User logged in, but not autorized');
                        return false;
                    } else {
                        return false;
                        disparaModalRequest("/modal_fb_login", "300", "");
                        //          console.log('nao');
                    }
                });
            }
        }
    }
}

function acionaloginFacebook(){
    //document.location = fb_url = "https://www.facebook.com/dialog/oauth?client_id=705413109545842&redirect_uri="+document.documentURI+"&output=embed";
    document.location = fb_url = "https://www.facebook.com/dialog/oauth?client_id=705413109545842&redirect_uri="+url_connect+"&output=embed&scope=publish_actions";
}

function verificacookies(){
    var pickmall = getCookie('pickmall');
    var gettutorial = getCookie('gettutorial');
    if (pickmall && pickmall != 'undefined'){
        $("#EscolherShoppingMob").remove();
        if (gettutorial && gettutorial != 'undefined'){
            fecharTutorial();
        }else{
            setCookie("gettutorial","1");
        }
    }else{
        setCookie("pickmall","1");
    }

    $("#TutorialMob a").on({
        click: function(){
            fecharTutorial();
        }
    });
}

$(function(){
    $("#TutorialMob a").on({
        click: function(){
            fecharTutorial();
        }
    });
    var gettutorial = getCookie('gettutorial');
    if (gettutorial && gettutorial != 'undefined'){
        fecharTutorial();
    }else{
        setCookie("gettutorial","1");
    }

    var isiDevice = /ipad|iphone|ipod|android/i.test(navigator.userAgent.toLowerCase());

    if(isiDevice || largura_window > 900) {
        $("body").attr("id","TabletSmart");

        // define cookie para ocultar splash
        // $("#EscolherShoppingMob .escolher-shopping").change(function(){
        // 	var url = $('option:selected', this).val();

        // 	if(url == "") {
        // 		return false;
        // 	}
        // 	window.location.href = url;
        // });
    }
	//else{$("body").attr("id","TabletSmart");}
	

//    $(document.body).on({
//        click: function(){
//            if (logadoFacebook()){
//                return true;
//            }else{
//                disparaModalRequest("/modal_fb_login","300","");
//                return false;
//            }
//        }
//    }, ".checkfb");

	$("#ico-menu").on({
		click: function(){
			var ico = $(this);
			var html_body = $("html,body");
			var header = $("#Header");
			var banner = $("#Header .head-mob");
			var menu = $("#Menu");

			var altura_window = $(window).height();

			fecharTutorial();

			if(ico.hasClass("ativo")) {
				ico.removeClass("ativo");
				html_body.removeAttr("style");

				banner.animate({
					marginLeft: "0"
				})

				ico.animate({
					// zIndex: "0",
					marginLeft: "0"					
				})

				menu.animate({
					left: "-275px"
				});

				setTimeout(function(){
					$(".maskmenu").remove();
				},400);

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
				marginLeft: "275px",
				zIndex: "9999"
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

			fecharTutorial();

			var altura_window = $(window).height();

			if(ico.hasClass("ativo")) {
				ico.removeClass("ativo");
				html_body.removeAttr("style");

				banner.animate({
					marginLeft: "0"
				});

				ico.animate({
					right: "0"
				})

				ico_menu.animate({
					marginLeft: "0"
				});

				menu_shp.animate({
					right: "-276px"
				});
				setTimeout(function(){
					$(".maskmenushp").remove();
				},400);

				return false;

			}

			ico.addClass("ativo");

			html_body.css({
				"overflow":"hidden",
				"height": altura_window+"px"
			});

			ico.animate({
				right: "276px"
			})

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

//	$("[rel='modal']").on({
//		click: function(){
//			var tamanho = $(this).attr('data-param');
//			var qualclasse = $(this).attr("data-class");
//			var url = $(this).attr('data-href')
//			// disparaModalRequest($(this).attr("href"), tamanho, qualclasse);
//			disparaModalRequest(url, tamanho, qualclasse);
//		}
//	});

    $(document.body).on({
		click: function(){
            var tamanho = $(this).attr('data-param');
            var qualclasse = $(this).attr("data-class");
            var url = $(this).attr('data-href');
            // disparaModalRequest($(this).attr("href"), tamanho, qualclasse);
            disparaModalRequest(url, tamanho, qualclasse);
		}
	}, "[rel='modal']");

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
//	$("a.like:not(.ativo)").on({
//		click: function(){
//			var link = $(this);
//			var id_item = link.attr("data-id");
//			$.ajax({
//	            type: "POST",
//	            url: '/curtir/',
//	            dataType: "json",
//	            data: {id_item: id_item},
//	            beforeSend: function(){
//	                // console.log("before send");
//	            },
//	            success: function(data) {
//	                link.text(data.total);
//                    link.addClass('ativo');
//	            },
//	            error: function(){
//	                console.log("erro curtir");
//	            }
//	       });
//	       return false;
//		}
//	});

	if (window.location.search.indexOf('code') >= 0){
		logado_fb = true;
	}

    $(document.body).on({
		click: function(){
            logadoFacebook();
             if (logado_fb || window.name.indexOf('app_runner_fb') >= 0){
                var link = $(this);
                var id_item = link.attr("data-id");
                $.ajax({
                    type: "POST",
                    url: '/curtir/',
                    dataType: "json",
                    data: {id_item: id_item},
                    beforeSend: function(){
    //	                console.log("before send");
                    },
                    success: function(data) {
                        link.text(data.total);
                        link.addClass('ativo');
                        acrescenta_curtidas('minhas_curtidas', id_item);
                        FB.api(
                            "/me/photos",
                            "POST",
                            {
                                "url": data.imagem,
                                "message": data.mensagem
                            },
                            function (response) {
    //                          console.log(response);
                              if (response && !response.error) {
    //                            console.log(response.error);
                              }
                            }
                        );
                    },
                    error: function(){
                        console.log("erro curtir");
                    }
               });
               return false;
            }else{
                disparaModalRequest("/modal_fb_login","300","");
            }
		}
	}, "a.like:not(.ativo)");

	$(document.body).on({
		click: function(){
			var link = $(this);
			var id_item = link.attr("data-id");
			var total_atual = parseInt(link.text());
            $.ajax({
	            type: "POST",
	            url: '/descurtir/',
	            dataType: "json",
	            data: {id_item: id_item, total_atual: total_atual},
	            beforeSend: function(){
	                // console.log("before send");
	            },
	            success: function(data) {
	                link.text(data.total);
	                link.removeClass('ativo');
	                decresce_curtidas('minhas_curtidas', id_item);
	            },
	            error: function(){
	                console.log("erro curtir");
	            }
	        });
	        return false;
		}
	}, "a.like.ativo");

	$(document.body).on({
		click: function(){
            logadoFacebook();
            if (logado_fb || window.name.indexOf('app_runner_fb') >= 0){
                var link = $(this);
                var id_item = link.attr("data-id");
                $.ajax({
                    type: "POST",
                    url: '/curtir/',
                    dataType: "json",
                    data: {id_item: id_item},
                    beforeSend: function(){
                        // console.log("before send");
                    },
                    success: function(data) {
                        var seletor = "*[data-id="+id_item+"]";
                        $(seletor).text(data.total);
                        $(seletor).addClass("ativo");
                        if (data.total == '1'){
                            link.text(data.total + " pessoa curtiu essa oferta");
                        }else {
                            link.text(data.total + " pessoas curtiram essa oferta");
                        }
                        link.parents("p.curtidas").addClass('ativo');
                        acrescenta_curtidas('minhas_curtidas', id_item);
                        FB.api(
                            "/me/photos",
                            "POST",
                            {
                                "url": data.imagem,
                                "message": data.mensagem
                            },
                            function (response) {
                              //console.log(response);
                              if (response && !response.error) {
                                console.log(response.error);
                              }
                            }
                        );
                    },
                    error: function(){
                        console.log("erro curtir");
                    }
               });
               return false;
		    }else{
                disparaModalRequest("/modal_fb_login","300","");
            }
		}
	}, "p.curtidas:not(.ativo) span");

	$(document.body).on({
		click: function(){
			var link = $(this);
			var id_item = link.attr("data-id");
            var texto = link.text();
            var total_atual = parseInt(texto.split(" ")[0]);
			$.ajax({
	            type: "POST",
	            url: '/descurtir/',
	            dataType: "json",
	            data: {id_item: id_item, total_atual: total_atual},
	            beforeSend: function(){
	                // console.log("before send");
	            },
	            success: function(data) {
	                link.text(data.total+" pessoas curtiram essa oferta");
	                link.parents("p.curtidas").removeClass('ativo');
	                decresce_curtidas('minhas_curtidas', id_item);
	            },
	            error: function(){
	                console.log("erro curtir");
	            }
	       });
	       return false;
		}
	}, "p.curtidas.ativo span");

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

    $(document.body).on({
        click: function(){
            console.log('era pra acionar, mas ta desativado');
            acionaloginFacebook();
        }
    }, '.conectar_fb');

	// Compartilhar
	$(document.body).on({
		click: function(){
            logadoFacebook();
            if (logado_fb || window.name.indexOf('app_runner_fb') >= 0){
                var botao_share = $('#ShareProduto .bt-share');
                var imagem_id = botao_share.attr("data-base");
                var mascara_id = botao_share.attr("data-mask");
                var id_item = botao_share.attr("data-id");

                $.ajax({
                    type: "POST",
                    url: '/mesclar/',
                    dataType: "json",
                    data: {id_item: id_item, imagem_id: imagem_id, mascara_id: mascara_id},
                    beforeSend: function(){
//                        console.log("before send");
                    },
                    success: function(data) {
			console.log(data.imagem);
                        FB.api(
                            "/me/photos",
                            //"/"+fb_user_id+"/photos",
			    //"/"+fb_user_id+"/feed",
                            "POST",
                            {
                                "url": data.imagem,
                                "message": data.mensagem
                            },
                            function (response) {
                              if (response && !response.error) {
                                console.log(response);
                              }
                              console.log(response.error);
                            }
                        );
                        fechaModal();
                        return false;
                    },
                    error: function(){
                        console.log("erro mesclar");
                    }
               });
               return false;
            }else{
                disparaModalRequest("/modal_fb_login","300","");
            }
		}

	}, '#ShareProduto .bt-share');

});

$( document ).ready(function() {
    if (url_slug && url_slug != "_=_"){
        if (url_slug.split('?')[0] === 'evento'){
            var largura = '560';
        }else{
            var largura = '786';
        }
        var url_item = '/modal/'+url_slug.replace('?', '/')+'/';
        disparaModalRequest(url_item,largura,"");
    }
	$(window).scroll(function() {
		if($(window).scrollTop() + $(window).height() == $(document).height()) {
			var container = $('.cl.final');
			var ultimo_destaque = container.attr('data-destaque');
			var ultimo_evento = container.attr('data-evento');
			var ultima_oferta = container.attr('data-oferta');
			var filtro = container.attr('data-filtro');
			if (filtro){
				var url = '?mais_ofertas=sim';
			}else{
				var url = '/mais_ofertas/';
			}

			// depois de guardar os valores em variaveis,
			// remove elemento para ajustar paginacao
			container.remove();
			if (!ultima_oferta && !ultimo_evento && !ultimo_destaque){
				return false;
			}
			$.ajax({
	            type: "POST",
	            url: url,
	            dataType: "html",
	            data: {ultimo_destaque:ultimo_destaque,ultimo_evento:ultimo_evento,ultima_oferta:ultima_oferta},
	            beforeSend: function(){
	                // console.log("before send");
                        $('.container:first').append('<br class="cl"><img src="https://www.liquidacaolapisvermelho.com.br/static/img/loading-llv.gif" class="img-loading-mais">');
	            },
	            success: function(data) {
	                $(".img-loading-mais").after(data);
	                $(".img-loading-mais").remove();
	            },
	            error: function(){
	                console.log("erro enviar");
	            }
	       });
	       return false;
		}
	});

	// abre splash
	$(".splash-menu a").on({
		click: function(){
			$("#Splash").show();
		}
	});

	$(".close-splash").on({
		click: function(){
			$("#Splash").hide();
		}
	});

	$("form#SplashForm").submit(function(){
		var erro = false;
        var formulario = $(this);
        var email = $(".valida_email");
        var valida_campo = $(".valida");

		if(!validaCampo(valida_campo)){
			$(valida_campo).parents('.campo').children(".error").remove();
            $(valida_campo).parents('.campo').append("<span class='error>Campo obrigatório</span>");

            erro = true;
        } else {
            $(valida_campo).parents('.campo').children(".error").remove();
        }

        if(!validaCampo(email)){
            $(email).parents('.campo').children(".error").remove();
            $(email).parents('.campo').append("<span class='error>Campo obrigatório</span>");

            erro = true;
        }else if(!validaEmail(email.val())) {
            $(email).parents('.campo').children(".error").remove();
            $(email).parents('.campo').append("<span class='error>Insira um email válido.</span>");

            erro = true;
        }else {
            $(email).parents('.campo').children(".error").remove();
        }

        if(erro == true) {
            return false;
        } else {
        	var nome = $("[name=nome]").val();
        	var email = $("[name=email]").val();
        	var loja = $("[name=loja]").val();
        	// console.log(nome, email, loja);
        	$.ajax({
	            type: "POST",
	            url: '/solicitar_loja/',
	            dataType: "json",
	            data: {nome:nome,email:email,loja:loja},
	            beforeSend: function(){
	                // console.log("before send");
	                $("#SplashForm :submit").val("Enviando...");
	            },
	            success: function(data) {
	                $("#SplashForm :submit").val("Enviado. Obrigado.");
	                setTimeout(function() {$("#Splash").remove();}, 3000);
	            },
	            error: function(){
	                console.log("erro enviar");
	            }
	        });
        	return false;
        }


	});
    marca_minhas_curtidas();

    var verifica_splash = getCookie('nosplash');
    if (verifica_splash && verifica_splash != 'undefined'){
        $("#Splash").hide();
    }else{
        window.setTimeout('$("#Splash").show()', 120000);
    }
    // define cookie para ocultar splash
    document.cookie = "nosplash=1; ; max-age=" + 60 * 10;
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
			$('body').append("<div class='lightbox preloading'><p class='loading-modal'><img src='https://www.liquidacaolapisvermelho.com.br/static/img/loader-bgescuro.gif' alt='' class='fl' /> <span class='fl'>Carregando</span></p></div>");
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

function acrescenta_curtidas(nome_cookie, id_item) {
    var cookieatual = getCookie(nome_cookie);
    var novo_valor = 'i'+id_item;
    if (cookieatual){
        var cookie = cookieatual + novo_valor;
    }else{
        var cookie = novo_valor
    }
    setCookie(nome_cookie,cookie);
}

function decresce_curtidas(nome_cookie, id_item) {
    var cookieatual = getCookie(nome_cookie);
    var novo_valor = 'i'+id_item;
    if (cookieatual){
        var curtidas_ids = cookieatual.split("i");
        var posicao = jQuery.inArray(id_item, curtidas_ids);
        if (posicao >= -1){
            curtidas_ids.splice(posicao, 1);
        }
        var cookie = curtidas_ids.join('i');
        setCookie(nome_cookie,cookie);
    }
}

function marca_minhas_curtidas() {
    var minhas_curtidas = getCookie("minhas_curtidas");
    if(minhas_curtidas){
        var meus_curtidas_ids = minhas_curtidas.split("i");
        for (item in meus_curtidas_ids ) {
            $('a.like[data-id="'+meus_curtidas_ids[item]+'"]').addClass('ativo');
            $('p.curtidas span[data-id="'+meus_curtidas_ids[item]+'"]').parents("p.curtidas").addClass("ativo");
        }
    }
}
