// TODO Faire un namespace Adencf.

function onForeignKeyChanged(elem, callback, get_label_url) {
    var app_label = elem.siblings('.related_app_name').val();
    var model_label = elem.siblings('.related_model_name').val();
    var show_related_lookup = elem.siblings('.show_related_lookup').val();
    var onclick  = 'return false;';
    if (show_related_lookup == '1') onclick = "return showRelatedObjectPopup(this);";
    if (elem.val() && get_label_url) {
        var url = get_label_url;
        url = url + '?pk='+elem.val();
        $.getJSON(url, {}, function(data) { // màj du label > lien vers la fk.
            var link = $('<a class="preview" href="'+data['URL']+'" onclick="'+onclick+'">'+data['LABEL']+'</a>');
            if (data.PREVIEW_URL) {
                var preview = $('<img src="'+data.PREVIEW_URL+'" />');
                preview.appendTo(link);
            }
            elem.siblings('div.label_container').find('strong.label').html(link);
            if (callback) callback(elem); 
        });
    } else if (callback) callback(elem);  // Clear du rawId.
    else elem.parent().find('.label').html('&nbsp;');
}

$(document).ready(function () {
    $(".editeur").each(function () {
        var textArea = $(this).find("textarea");
        $(this).children(".toolbar").children("button.gras").click(function() {
            var selection = textArea.getSelection().text;
            textArea.replaceSelection("[" + selection + "]", true);
        });
        $(this).children(".toolbar").children("button.sup").click(function() {
            var selection = textArea.getSelection().text;
            textArea.replaceSelection("{" + selection + "}", true);
        });
        $(this).children(".toolbar").children("button.bas").click(function() {
            var selection = textArea.getSelection().text;
            textArea.replaceSelection(selection.toLowerCase(), true);
        });
    });

    $(".titre-box button.bas").click(function() {
        var input = $(this).parent().find("input:text");
        var selection = input.getSelection().text;
        input.replaceSelection(selection.toLowerCase(), true);
    });
    
    /* Initialise la position des preview à côté du lien pour le mouseover. */
    $(document).delegate('.field-box p.preview a, a.preview', 'mouseover', function(){
        var pos = $(this).position();    
        var left = (pos.left + 5) + "px";
        var top = (pos.top - 55)+ "px";
        $(this).children().css({ left: left, top: top});
    });
});
