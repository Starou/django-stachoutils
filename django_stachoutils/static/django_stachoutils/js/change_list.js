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
    // http://www.appelsiini.net/projects/jeditable
    var fields = [];
    $('table > thead > tr input.fieldname').each(function(i, elt) { fields.push($(elt).val()); });

    $("td.editable").editable($("input[name=inline_url]").val(), {
        indicator: 'Saving...',
        tooltip: 'Cliquer pour modifier',
        submitdata: function(value, settings){
            return  {
                'attr': fields[$(this).prevUntil().length-1],
                'id': $(this).siblings('td.pk').children().val()
            }
        }
    });
});
