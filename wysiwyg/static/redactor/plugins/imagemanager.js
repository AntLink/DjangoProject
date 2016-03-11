if (!RedactorPlugins) var RedactorPlugins = {};

(function ($) {
    RedactorPlugins.imagemanager = function () {
        return {
            init: function () {
                if (!this.opts.imageManagerJson) return;

                this.modal.addCallback('image', this.imagemanager.load);
            },
            load: function () {
                var $modal = this.modal.getModal();
                this.modal.createTabber($modal);
                this.modal.addTab(1, 'Upload', 'active');
                this.modal.addTab(2, 'Choose');

                $('#redactor-modal-image-droparea').addClass('redactor-tab redactor-tab1');

                var $box = $('<div id="redactor-image-manager-box" style="" class="redactor-tab redactor-tab2"><div id="img-slim-scroll">').hide();
                $modal.append($box);
                $('#img-slim-scroll').slimScroll({
                    height: '304px',
                    alwaysVisible: true
                });
                $.ajax({
                    dataType: "json",
                    cache: false,
                    url: this.opts.imageManagerJson,
                    success: $.proxy(function (data) {
                        $.each(data, $.proxy(function (key, val) {
                            // title
                            var thumbtitle = '';
                            if (typeof val.title !== 'undefined') thumbtitle = val.title;

                            var img = $('<img src="' + val.thumb + '" rel="' + val.image + '" title="' + thumbtitle + '" style="padding:5px 10px 5px 0px; width: 102px; height: 102px; cursor: pointer;" />');
                            $('#img-slim-scroll').append(img);
                            $(img).click($.proxy(this.imagemanager.insert, this));

                        }, this));


                    }, this)
                });


            },
            insert: function (e) {
                this.image.insert('<img class="img-responsive" src="' + $(e.target).attr('rel') + '" alt="' + $(e.target).attr('title') + '">');
            }
        };
    };
})(jQuery);