$(function(){


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
		}, ".mask");

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
		})

})