$(document).ready(function(){
    // $("#id_desconto").attr('disabled',true);
    // $("#id_desconto").val($("#id_desconto").val()+'%');
    $("#id_desconto").width('100');
    $("#id_preco_inicial").width('100');
    $("#id_preco_final").width('100');
    $(".field-preco_inicial").width('300').css('float',"left");
    $(".field-preco_final").width('300').css('float',"left");

    $("#id_preco_inicial").maskMoney({thousands:'', decimal:','});
    $("#id_preco_final").maskMoney({thousands:'', decimal:','});

    var inicial = parseInt($("#id_preco_inicial").val().replace(',','.'));
    var pfinal = parseInt($("#id_preco_final").val().replace(',','.'));

    $(function() {
        $("#id_preco_inicial, #id_preco_final").keypress(function() {
            if ($("#id_preco_inicial").val() > $("#id_preco_final").val()){
                var result = parseInt(parseFloat($("#id_preco_final").val(), 10) * 100)/ parseFloat($("#id_preco_inicial").val(), 10);
                var result_str = result+'';
                // $('#id_desconto').val(result_str.substr(0,2)+'%');
                $('#id_desconto').val(result_str.substr(0,2));
            }else{
                $('#id_desconto').val('-');
            }
        })
    });
});