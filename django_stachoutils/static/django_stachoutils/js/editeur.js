var editeur = {
    rxGraisse: /(\w\s*)((\[.*?)(\])){0,1}(.+?\.){0,1}(.*)/m,
    graissePhraseSuivante: function(texte) {
        var texte = texte.match(editeur.rxGraisse);
        texte.splice(0, 1);  // Supprime le premier item qui est le texte passé en paramètre.

        // La première phrase n'est pas en gras.
        if (texte[1] === undefined) {
            texte.splice(1, 1, "[");
            texte.splice(5, 0, "]");
        } else if (texte[4] === undefined) {
            return texte.input;  // Tout le texte est déjà en gras, on ne change rien.
        } else {
            texte.splice(1, 1);      // Supprime le texte en gras.
            texte.splice(2, 1);      // Supprime le "]"
            texte.splice(3, 0, "]"); // et le pose à la fin de la phrase suivante.
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
    });
});
