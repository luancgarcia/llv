$(document).ready(function(){
    var masks = ['(00) 00000-0000', '(00) 0000-00009'],
    maskBehavior = function(val, e, field, options) {
        return val.length > 14 ? masks[0] : masks[1];
    };

    $("#id_telefone").mask(maskBehavior, {onKeyPress:
       function(val, e, field, options) {
           field.mask(maskBehavior(val, e, field, options), options);
       }
    });

});