function not_empty(val) {
    return (val !== "");
}


$(document).ready(function() {
    /* fold/unfold inlines.
     * You need to add an hidden input in the change_form.html like:
     * <input type="hidden" name="myrelation_set_visible" value="0" />
     * where `myrelation_set' is the inline prefix in the html page.
     */
    $(".inline-group").on("click", ".toggle", function(){
        var h3 = $(this).parent("h3");
        var name_and_index = $(this).parents(".inline-related").attr("id").split("-");
        var visibles_input_name = name_and_index[0];
        var current_index = name_and_index[1];
        visibles_input_name = visibles_input_name + "_visible";
        var visibles_input = $("input[name='" + visibles_input_name + "']");
        var visibles_input_values = visibles_input.val().split(",");
        var array_index_of_current = visibles_input_values.indexOf(current_index);
        h3.toggleClass("closed");


        // Update valeur champ caché.
        if (h3.hasClass("closed")) {
            if (array_index_of_current !== -1) {
                visibles_input_values.splice(array_index_of_current, 1);
            }
        } else {
            if (array_index_of_current === -1) {
                visibles_input_values.push(current_index);
            }
        }
        visibles_input.val(visibles_input_values.filter(not_empty).join(","));

        $(this).parents(".inline-related").children(".fieldsets-group").toggle("1000");
    });

    // Déplie automatiquement tout nouvel inline ajouté.
    $(".add-row").click(function(e) {
        $(this).parent().find(".inline-related.last-related:visible:last").find("a.toggle").click();
    });
});

