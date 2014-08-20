$(document).ready(function(){
    // $("#id_desconto").attr('disabled',true);
    // $("#id_desconto").val($("#id_desconto").val()+'%');
    $("#id_desconto").width('100');
    $("#id_preco_inicial").width('100');
    $("#id_preco_final").width('100');
    $(".field-preco_inicial").width('300').css('float',"left");
    $(".field-preco_final").width('300').css('float',"left");

    $("#id_preco_inicial").maskMoney({thousands:'.', decimal:','});
    $("#id_preco_final").maskMoney({thousands:'.', decimal:','});

    $(function() {
        $("#id_preco_inicial, #id_preco_final").keypress(function() {
            var inicial = parseFloat($("#id_preco_inicial").val().replace('.','').replace(',','.'));
            var pfinal = parseFloat($("#id_preco_final").val().replace('.','').replace(',','.'));

            if (inicial && pfinal){
                if (inicial > pfinal){
                    var result = parseInt((pfinal * 100)/ inicial);
                    var result_str = result+'';
                    // $('#id_desconto').val(result_str.substr(0,2)+'%');
                    // $('#id_desconto').val(result_str.substr(0,2));
                    $('#id_desconto').val(result);
                }else{
                    $('#id_desconto').val('-');
                }
            }else{
                $('#id_desconto').val('0');
            }
        })
    });
});