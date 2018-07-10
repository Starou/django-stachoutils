var editeur = {
    rxGraisse: /((\[.*?)(\])){0,1}(.+?\.){0,1}(.*)/m,
    graissePhraseSuivante: function(texte) {
        var texte = texte.match(editeur.rxGraisse);
        texte.splice(0, 1);  // Supprime le premier item qui est le texte passé en paramètre.

        // La première phrase n'est pas en gras.
        if (texte[0] === undefined) {
            texte.splice(0, 1, "[");
            texte.splice(4, 0, "]");
        } else if (texte[3] === undefined) {
            return texte.input;  // Tout le texte est déjà en gras, on ne change rien.
        } else {
            texte.splice(0, 1);      // Supprime le texte en gras.
            texte.splice(1, 1);      // Supprime le "]"
            texte.splice(2, 0, "]"); // et le pose à la fin de la phrase suivante.
        }
        return texte.join('');
    }
};

$(document).ready(function () {
    $(".editeur").each(function () {
        var textArea = $(this).find("textarea");
        $(this).children(".toolbar").children("button.gras_phrases").click(function() {
            textArea.val(editeur.graissePhraseSuivante(textArea.val()));
        });
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
