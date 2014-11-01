$(document).ready(function(){
    $('p.file-upload a').attr('target', '_blank');

    // codigo para campo de Chamada promocional
    $("#id_texto_promocional").keyup(function() {
        var campo = $(this);
        var texto = "Limite 25 caracteres.";
        var total_caracteres = campo.val().length;
        var novo = texto+" Você já digitou "+total_caracteres+" caracteres.";
        if (total_caracteres == 0){
            campo.siblings(".help-block").text(texto);
        }else{
            campo.siblings(".help-block").text(novo);
        }
    });

    if($("#id_shopping").length == 1){
        $('select[name="shopping"] option:eq(1)').attr('selected', 'selected');
    }

});