function setStyleInvalidRows(static_url, rxStatus) {
    rxStatus = rxStatus || /Valide/ ;
    var indexColStatus = null ;
    // Recherche du numero de la colonne "statut".
    $('body.change-list table').find("thead").find("th").each( function(i, elt) {
        if( rxStatus.test($(elt).html()) ) {
            indexColStatus = i;
            return false;
        }
    });
    if (indexColStatus) { // Màj du style des lignes d'items annulés.
        $('table').find("tbody").find("tr").each( function() {
            var imgStatus = $($(this).children()[indexColStatus]).find("img");
            if ( imgStatus.attr('alt') == "False" || imgStatus.attr('alt') == "0" ) {
                $(this).addClass("disabled");
                $(this).find("a").each(function(){ // Disable des liens de la ligne.
                    $(this).attr('title', $(this).attr('href')).removeAttr('href').removeAttr('onclick').unbind('click');
                });
                $(this).find("img").each(function(){ // desat des img d'attributs booléens.
                    var srcImg = $(this).attr("src");
                    if ( /icon-yes\.gif/.test(srcImg) || /icon-no\.gif/.test(srcImg) ) {
                        var srcInactiveImg = srcImg.replace(/.*icon/, static_url + "django_stachoutils/img/icon-inactive");
                        $(this).attr("src", srcInactiveImg);
                    }
                });
            }
        });
    }
}

$(document).ready(function () {
    // http://vitalets.github.io/x-editable/index.html
    var url = $("input[name='edit_inline_url']").val();
    $("td.editable").editable({
        type: 'text',
        pk: 0,  // overriden in params but must be initialized here to fire the ajax call.
        url: url,
        params: function(params) {
            return {
                name: $('table > thead > tr > th:nth-child(' + ($(this).index() + 1) + ') > input.fieldname').val(),
                pk: $(this).siblings(".pk").find("input").val(),
                value: params.value
            };
        },
        success: function(response, newValue) {
            if(!response.success) return response.errors.toString();
        }
    });
});
