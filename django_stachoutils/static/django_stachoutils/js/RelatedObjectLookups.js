/* Charger ce fichier en dernier pour écraser les fonctions de l'admin.
 *
 * */

// Fonction de l'admin réecrite pour declencher le onchange sur le 
// champ caché qui est modifié et appeler la màj du label.
// Doit être loadé après 'RelatedObjectLookups.js' de l'admin.
function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = $('#'+name);
    elem.val(chosenId).change(); // Provoque appel onForeignKeyChanged si utilisé avec le widget ForeignKeyRawIdHiddenWidget.
    win.close();
}

function showRelatedObjectPopup(triggeringLink) {
    var name = triggeringLink.parentNode.id.replace(/^view_lookup_/, '');
    name = id_to_windowname(name);
    return openPopupWindow(triggeringLink.href, '_popup', name);
} 

function clearRawId2(triggeringLink) { 
    $(triggeringLink).parent().prevAll('.vForeignKeyRawIdAdminField').val('').change();
    $(triggeringLink).parent().find('.label').html('Choisissez une valeur');
    return false;
} 

function openPopupWindow(href, popup_var, name, width, height) {
    if (href.indexOf('?') == -1) {
        href += '?';
    } else {
        href += '&';
    }
    href += popup_var + '=1';
    if (!width) width = '800';
    if (!height) height = '600';
    var win = window.open(href, name, ('height='+height+',width='+width+',resizable=yes,scrollbars=yes'));
    win.focus();
    return false;
} 
