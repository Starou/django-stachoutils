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
});
