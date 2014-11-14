(function() {

    MD_VIEWER = {
        textareaHeight : 500,
        width : null
    };

    var editor = function(input, preview)
    {
        this.update = function () {
            preview.innerHTML = markdown.toHTML(input.value);
        };
        input.editor = this;
        this.update();
    };

    var loadPreview = function() {
        new editor($("#data")[0], $("#live_preview")[0]);
    };

    // Live keyboard
    $("textarea#data").on("keyup", function() {
        loadPreview();
    });

    loadPreview();
})();
