// formField ImageDroppableHiddenInput.
$(document).ready(function () {
    $(".droppableHiddenInput .droppable").droppable({ hoverClass: 'drophover',
        drop: function(event, ui) {
            var destImageSrc = $(this).find('img').attr("src");
            $(this).find('img').attr("src", ui.draggable.find('img').attr("src"));

            var destInput = $(this).parents('.droppableHiddenInput').find("input");
            if (ui.draggable.parents('.droppableHiddenInput').length == 1) { // swap.
                var sourceInput = ui.draggable.parents('.droppableHiddenInput').find("input");
                var newDestValue = sourceInput.val();
                var newSourceValue = destInput.val();
                sourceInput.val(destInput.val());
                var newDraggableSource = $('<div class="draggable"><img src="'+destImageSrc+'" /></div>');
                var draggableDroppable = ui.draggable.parent();
                ui.draggable.remove();
                draggableDroppable.append(newDraggableSource);
            } else { // Drop d'un élément extérieur.
                var sourceInput = ui.draggable.find("input");
                var newDestValue = sourceInput.val();
            }
            destInput.val(newDestValue);
        },
        accept: function(draggable) {
            if (draggable.parents('.droppable')[0] == $(this)[0]) return false;
            else if (draggable.find("input#_group").val() != $(this).parents(".droppableHiddenInput").siblings("input#_group").val()) return false;
            else return true
        }
    }); 
    $(".droppableHiddenInput .droppable .draggable").draggable({zindex: 20, revert: "invalid"}); 

    $(document).delegate(".droppableHiddenInput span.delete", 'click', function() { 
        var destInput = $(this).parents('.droppableHiddenInput').find("input").val("");
        var destImageSrc = $(this).parents('.droppableHiddenInput').find('img').attr("src", "");
    });
});
