if (!RedactorPlugins) var RedactorPlugins = {};

RedactorPlugins.images = function () {
    return {
        getTemplate: function () {
            return String()
                + '<section id="redactor-modal-images">'
                + '<div class="row">'
                + '<div class="col-sm-12">'
                + '<ul class="nav nav-tabs" style="margin-bottom: 10px;">'
                + '<li class="active" id="tab-1"><a href="#demo-tabs-box-1" data-toggle="tab" aria-expanded="true">' + this.lang.get('image_library') + '</a></li>'
                + '<li class="" id="tab-2"><a href="#demo-tabs-box-2" data-toggle="tab" aria-expanded="false">' + this.lang.get('upload_image') + '</a></li>'
                + '</ul>'
                + '</div>'
                + '</div>'

                + '<div class="tab-content">'

                + '<div class="tab-pane fade in active" id="demo-tabs-box-1">'
                + '<div class="row">'
                + '<div class="col-sm-9">'
                + '<div id="slim-scroll">'
                + '<div data-page="1" class="dropzone" id="dropzone" style="padding:0px 7px 0px 7px;">'
                + '</div>'
                + '</div>'
                + '</div>'
                + '<div class="col-sm-3">'

                + '<div id="img-detail">'
                    //+ '<img class="img-responsive thumbnail" src="/media/image/thumbnail/512x288/7f91d2dd-7047-40b5-98d8-7006f200b540.jpg">'
                    //+ '<hr>'
                + '</div>'
                + '</div>'

                + '</div>'
                + '</div>'

                + '<div class="tab-pane fade" id="demo-tabs-box-2" > '
                + '<div class="row">'
                + '<div class="col-sm-12" style="height: 424px;">'
                + '<form class="dropzone dz-clickable" id="add-image" >'
                + '<div class="dz-default dz-message">'
                + '<div class="dz-icon icon-wrap icon-circle icon-wrap-md">'
                + '<i class="fa fa-cloud-upload fa-3x"></i>'
                + '</div>'
                + '<div>'
                + '<p class="dz-text">' + this.lang.get('drop_image_to_upload') + '</p>'
                + '<p class="text-muted">' + this.lang.get('or_click_to_pick_manual') + '</p>'
                + '</div>'
                + '</div>'
                + '</form>'
                + '</div>'
                + '</div>'
                + '</div>'

                + '</div>'
                + '</section>';
        },
        init: function () {
            if (!this.opts.imagesUrlLoadJson) return;
            var button = this.button.add('image', 'Images Manager');
            this.button.addCallback(button, this.images.show);
            this.button.addCallback(button, this.images.load);
            //this.button.addCallback(button, this.images.freewallReload);
        },

        freewallReload: function () {
            var wall = new freewall('#dropzone');
            wall.reset({
                selector: '.dz-preview',
                animate: true,
                gutterX: 6,
                gutterY: 6,
                cellW: 100,
                cellH: 100,
                onResize: function () {
                    wall.fitWidth();
                },
                onComplete: function () {
                }
            });
            return wall.fitWidth();
        },
        freewallReloadImageGallery: function () {
            var wall = new freewall('#image-gallery');
            wall.reset({
                selector: '.dz-preview',
                animate: true,
                gutterX: 6,
                gutterY: 6,
                cellW: 100,
                cellH: 100,
                onResize: function () {
                    wall.fitWidth();
                },
                onComplete: function () {
                }
            });
            return wall.fitWidth();
        },
        dropzoneUpload: function () {
            var ob = this;
            var csrftoken = this.images.getCookie('csrftoken');
            $("#add-image").dropzone({
                url: ob.opts.imagesUrlupload,
                addRemoveLinks: false,
                previewsContainer: '#dropzone',
                acceptedFiles: ".jpeg,.jpg,.png,.gif",
                maxFilesize: 512,
                thumbnailWidth: 115,
                thumbnailHeight: 115,
                previewTemplate: '' +
                '<div class="dz-preview" >' +
                '<img data-dz-thumbnail />' +
                '<div class="dz-progress" style="height: 15px; border-radius: 50px">' +
                '<div class="progress progress-striped active" style="height: 15px; border-radius: 50px">' +
                '<div data-dz-uploadprogress class="progress-bar progress-bar-success">' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>',

                success: function (file, response) {
                    file.previewElement.classList.add("dz-preview");
                    $(file.previewTemplate).find('.dz-progress').remove();
                    $(file.previewTemplate).find('img').attr('style', 'cursor: pointer');
                    $(file.previewTemplate).find('img').attr('src', '/media/image/thumbnail/100x100/' + response.uniquename);
                    $(file.previewTemplate).find('img').attr('rel', '/media/image/' + response.uniquename);
                    $(file.previewTemplate).find('img').attr('title', response.filename);
                    $(file.previewTemplate).find('img').attr('data-id', response.imgid);
                    $(file.previewTemplate).find('img').attr('data-uniquename', response.uniquename);

                },
                error: function (file, response) {
                    file.previewElement.classList.add("dz-error");
                },
                sending: function (file, xhr, formData) {
                    $('#demo-tabs-box-2').attr('class', 'tab-pane fade');
                    $('#demo-tabs-box-1').attr('class', 'tab-pane fade active in');
                    $('#tab-1').attr('class', 'active');
                    $('#tab-2').attr('class', '');
                    ob.images.freewallReload();
                    var img = $(file.previewTemplate).find('img');
                    $(img).on('click', function () {
                        var imgd = '<img class="img-responsive thumbnail" src="/media/image/thumbnail/512x288/' + $(img).attr('data-uniquename') + '" data-id="' + $(img).attr('data-id') + '" data-uniquename="' + $(img).attr('data-uniquename') + '"' + ' title="' + $(img).attr('title') + '">';
                        var formd = '<hr>' +
                            '<form class="form-horizontal" id="form-img-detail">' +
                            '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">' +
                            '<input type="hidden" name="id" value="' + $(img).attr('data-id') + '">' +
                            '<input type="text" name="name" value="' + $(img).attr('title') + '" placeholder="Title" class="form-control">' +
                            '<textarea name="description" style="height: 95px;" placeholder="Description" rows="13" class="form-control"></textarea>' +
                            '</form>';
                        $('#img-detail').html(imgd + formd);
                    });
                },

            });

        },
        imageScroll: function () {
            var ob = this;
            var csrftoken = this.images.getCookie('csrftoken');
            $('#slim-scroll').slimScroll({
                height: '424px',
                alwaysVisible: true
            }).bind('slimscroll', function (e, pos) {
                var page = $('#dropzone').attr('data-page');
                if (pos == "bottom") {
                    $.ajax({
                        dataType: "json",
                        cache: false,
                        url: ob.opts.imagesUrlLoadJson,
                        data: {'page': page},
                        success: $.proxy(function (data) {
                            $.each(data[0].store, $.proxy(function (key, val) {
                                // title
                                var thumbtitle = '';
                                if (typeof val.title !== 'undefined') thumbtitle = val.title;
                                var img = $('<div class="dz-preview" ><img data-id="' + val.imgid + '" data-uniquename="' + val.uniquename + '" src="' + val.thumb + '" rel="' + val.image + '" title="' + thumbtitle + '" style="cursor: pointer;" ></div>');
                                $(img).on('click', function () {
                                    var imgd = '<img class="img-responsive thumbnail" src="/media/image/thumbnail/512x288/' + val.uniquename + '" data-id="' + val.imgid + '" data-uniquename="' + val.uniquename + '"' + ' title="' + thumbtitle + '"  data-description="' + val.description + '">';
                                    var formd = '<hr>' +
                                        '<form class="form-horizontal" id="form-img-detail">' +
                                        '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">' +
                                        '<input type="hidden" name="id" value="' + val.imgid + '">' +
                                        '<input type="text" name="name" value="' + thumbtitle + '" placeholder="Title" class="form-control">' +
                                        '<textarea name="description" style="height: 95px;" placeholder="Description" rows="13" class="form-control">' + val.description + '</textarea>' +
                                        '</form>';
                                    $('#img-detail').html(imgd + formd);
                                });
                                $('#dropzone').append(img)
                            }, ob));
                            $('#dropzone').attr('data-page', data[0].page);
                            ob.images.freewallReload()
                        }, ob)
                    });
                }
            });
        },
        getCookie: function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        load: function () {
            var csrftoken = this.images.getCookie('csrftoken');
            //Load Image
            $.ajax({
                dataType: "json",
                cache: false,
                url: this.opts.imagesUrlLoadJson,
                data: {'page': 1},
                success: $.proxy(function (data) {
                    $.each(data[0].store, $.proxy(function (key, val) {
                        var thumbtitle = '';
                        if (typeof val.title !== 'undefined') thumbtitle = val.title;
                        var img = $('<div class="dz-preview" ><img data-id="' + val.imgid + '" data-uniquename="' + val.uniquename + '" src="' + val.thumb + '" rel="' + val.image + '" title="' + thumbtitle + '"  data-description="' + val.description + '" style="cursor: pointer;" ></div>');
                        $(img).on('click', function () {
                            var imgd = '<img class="img-responsive thumbnail" src="/media/image/thumbnail/512x288/' + val.uniquename + '" data-id="' + val.imgid + '" data-uniquename="' + val.uniquename + '"' + ' title="' + thumbtitle + '"  data-description="' + val.description + '">';
                            var formd = '<hr>' +
                                '<form class="form-horizontal" id="form-img-detail">' +
                                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">' +
                                '<input type="hidden" name="id" value="' + val.imgid + '">' +
                                '<input type="text" name="name" value="' + thumbtitle + '" placeholder="Title" class="form-control">' +
                                '<textarea name="description" style="height: 95px;" placeholder="Description" rows="13" class="form-control">' + val.description + '</textarea>' +
                                '</form>';
                            $('#img-detail').html(imgd + formd);
                        });
                        $('#dropzone').append(img);
                    }, this));
                    $('#dropzone').attr('data-page', data[0].page);
                    this.images.freewallReload();
                }, this)
            });
            //End Load Image

            $('#img-detail').slimScroll({
                height: '424px',
                alwaysVisible: false
            });

            // Start Scroll Image
            this.images.imageScroll();
            this.images.dropzoneUpload();
        },

        show: function () {
            this.modal.addTemplate('images', this.images.getTemplate());
            this.modal.load('images', this.lang.get('images_manager'), 1250);
            this.modal.createCancelButton();
            var button = this.modal.createActionButton(this.lang.get('insert'));
            button.on('click', this.images.insert);
            this.selection.save();
            this.modal.show();

            //$('#mymodal-textarea').focus();
        },
        imageShow: function () {
            this.modal.addTemplate('images', this.images.getTemplate());
            this.modal.load('images', this.lang.get('images_manager'), 1250);
            this.modal.createCancelButton();
            var button = this.modal.createActionButton(this.lang.get('insert'));
            button.on('click', this.images.addImage);
            this.selection.save();
            this.modal.show();
        },
        addImageShow: function () {
            this.images.imageShow();
            this.images.dropzoneUpload();
            this.images.load();
            this.images.imageScroll();
        },
        removeImageGallery: function () {
            var ob = this;
            $('#image-gallery').find('.img-g').on('click', function () {
                var p = $(this).parent();
                var imgname = $(p).find('img').attr('data-image');
                var g = $('#id_gallery').attr('value');
                var newg = g.split(',');
                d = [];
                for (i = 0; i < newg.length; i++) {
                    if (imgname != newg[i]) {
                        d.push(newg[i]);
                    }
                }
                console.log(d.toString());
                $('#id_gallery').attr('value', d.toString());
                $(p).remove();
                ob.images.freewallReloadImageGallery();
            });
        },
        addImage: function () {
            var name = $('#img-detail > img').attr('data-uniquename');
            var title = $('#img-detail > img').attr('title');

            var ob = this;
            if (title != null && name != null) {

                var data = $('#form-img-detail').serialize();
                $.ajax({
                    dataType: "json",
                    cache: false,
                    url: ob.opts.imagesUrlJsonUpdate,
                    data: data,
                    method: 'POST',
                    success: $.proxy(function (data) {
                        ob.modal.close();
                        var html = '<img  class="img-responsive" src="/media/image/thumbnail/512x288/' + name + '" alt="' + data[0].name + '">';
                        var thumb = '<div class="dz-preview" ><label style="position: absolute; margin-left: 2px;cursor: pointer; color: #ea4335" class="img-g"><i class="fa fa-times-circle-o"></i></label><img  data-image="' + name + '" src="/media/image/thumbnail/100x100/' + name + '" alt="' + data[0].name + '"></div>';
                        $('#id_image').attr('value', name);
                        var d = $('#id_image').attr('value');
                        if (addImage == 'imagefeature') {
                            $('#image-feature').html(html);
                        }
                        if (addImage == 'imagegallery') {
                            $('#image-gallery').append(thumb);
                            ob.images.freewallReloadImageGallery();
                            var gval = $('#id_gallery').attr('value');
                            if (gval == undefined || gval == '') {
                                data = d;
                            } else {
                                data = gval + ',' + d;
                            }
                            $('#id_gallery').val(data)
                        }
                        ob.images.removeImageGallery();
                    }, ob)
                });
            } else {
                $('#img-detail').html('<div class="alert alert-warning fade in">' + this.lang.get('select_image') + '</div>');
            }
        },
        insert: function (e) {
            var name = $('#img-detail > img').attr('data-uniquename');
            var title = $('#img-detail > img').attr('title');

            var ob = this
            if (title != null && name != null) {

                var data = $('#form-img-detail').serialize();
                $.ajax({
                    dataType: "json",
                    cache: false,
                    url: ob.opts.imagesUrlJsonUpdate,
                    data: data,
                    method: 'POST',
                    success: $.proxy(function (data) {
                        ob.modal.close();
                        var html = '<img  class="img-responsive" src="/media/image/' + name + '" alt="' + data[0].name + '">';
                        ob.insert.htmlWithoutClean(html);
                    }, ob)
                });
            } else {
                $('#img-detail').html('<div class="alert alert-warning fade in">' + this.lang.get('select_image') + '</div>');
            }

        }
    };
};