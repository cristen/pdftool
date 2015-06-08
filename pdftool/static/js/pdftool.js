var files_array, pages_array;

$.event.props.push('dataTransfer');

files_array = [];

pages_array = [];

$(document).ready(function() {
  var backwardUpload, handleDragOver, handleFileSelect, handleImgClick, handleRemove, handleRotation, startUpload, updatePagesPosition;
  if (window.File && window.FileReader && window.FileList && window.Blob) {
    backwardUpload = function(e) {
      return $('#hidden-uploader').click();
    };
    handleImgClick = function(e) {
      var img, src;
      src = $(e.target).attr('src');
      img = e.target.cloneNode(true);
      img = $(img).removeClass('thumbnail')[0];
      return $(e.target).magnificPopup({
        items: {
          src: "<div class='centered'>" + img.outerHTML + "</div>",
          type: 'inline'
        },
        closeBtnInside: true
      });
    };
    handleRemove = function() {
      return $("#sortable").on('click', ".fa-minus-square", function() {
        if (confirm("Êtes-vous certain de vouloir supprimer cette page ?")) {
          $(this).parent().remove();
          return updatePagesPosition();
        }
      });
    };
    updatePagesPosition = function() {
      var element, i, _i, _len, _ref, _results;
      pages_array = [];
      _ref = $('#sortable li');
      _results = [];
      for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
        element = _ref[i];
        _results.push(pages_array.push({
          filename: $(element).data('filename'),
          page: $(element).data('pagenum'),
          rotation: $(element).data('rotation') || 0
        }));
      }
      return _results;
    };
    handleRotation = function() {
      $('#sortable').on('click', '.fa-undo', function() {
        var rotation;
        rotation = $(this).parent().data('rotation') || 0;
        rotation -= 90;
        $(this).parent().data('rotation', rotation);
        $(this).siblings('img').css({
          "-webkit-transform": "rotate(" + rotation + "deg)",
          "-moz-transform": "rotate(" + rotation + "deg)",
          "-ms-transform": "rotate(" + rotation + "deg)",
          "transform": "rotate(" + rotation + "deg)"
        });
        return updatePagesPosition();
      });
      return $('#sortable').on('click', '.fa-repeat', function() {
        var rotation;
        rotation = $(this).parent().data('rotation') || 0;
        rotation += 90;
        $(this).parent().data('rotation', rotation);
        $(this).siblings('img').css({
          "-webkit-transform": "rotate(" + rotation + "deg)",
          "-moz-transform": "rotate(" + rotation + "deg)",
          "-ms-transform": "rotate(" + rotation + "deg)",
          "transform": "rotate(" + rotation + "deg)"
        });
        return updatePagesPosition();
      });
    };
    handleFileSelect = function(evt) {
      var files, _ref;
      evt.stopPropagation();
      evt.preventDefault();
      files = ((_ref = evt.dataTransfer) != null ? _ref.files : void 0) || this.files;
      $('#drop').remove();
      $('#sortable').sortable({
        placeholder: 'ui-sortable-placeholder',
        start: function(e, ui) {
          return $(this).attr('data-previndex', ui.item.index());
        },
        update: function(e, ui) {
          return updatePagesPosition();
        }
      });
      return $.each(files, function(index, value) {
        var data, filename;
        data = new FormData();
        data.append('file', files[index]);
        filename = files[index].name;
        $.ajax({
          url: $("#upload-button").data('preview-url'),
          type: 'POST',
          cache: false,
          processData: false,
          contentType: false,
          data: data,
          xhrFields: {
            onprogress: function(e) {
              if (e.lengthComputable) {
                return $('#completion').progressbar({
                  value: e.loaded / e.total * 100,
                  change: $('#progress-label').text("" + (e.loaded / e.total * 100) + " %")
                });
              }
            }
          },
          success: function(data, textStatus, errors) {
            var blob, byteArray, byteCharacters, byteNumbers, bytes, el, i, url, _i, _len;
            for (index in data) {
              bytes = data[index];
              byteCharacters = atob(bytes);
              byteNumbers = new Array(byteCharacters.length);
              for (i = _i = 0, _len = byteNumbers.length; _i < _len; i = ++_i) {
                el = byteNumbers[i];
                byteNumbers[i] = byteCharacters.charCodeAt(i);
              }
              byteArray = new Uint8Array(byteNumbers);
              blob = new Blob([byteArray], {
                type: 'application/pdf'
              });
              url = window.URL.createObjectURL(blob);
              $('#files ul').append(("<li class='pdf_thumbnail' data-filename='" + filename + "' data-pagenum='" + index + "'>") + ("<img src='" + url + "' class='thumbnail'/>") + '<i class="fa fa-minus-square"></i>' + '<i class="fa fa-undo"></i>' + '<i class="fa fa-repeat"></i>' + '</li>');
            }
            $('#completion').fadeOut();
            return updatePagesPosition();
          }
        });
        return files_array.push(files[index]);
      });
    };
    handleDragOver = function(evt) {
      evt.stopPropagation();
      evt.preventDefault();
      return evt.dataTransfer.dropEffect = 'copy';
    };
    startUpload = function(evt) {
      var data, el, i, _i, _j, _len, _len1;
      evt.stopPropagation();
      evt.preventDefault();
      data = new FormData();
      for (i = _i = 0, _len = files_array.length; _i < _len; i = ++_i) {
        el = files_array[i];
        data.append('files[]', el);
      }
      for (i = _j = 0, _len1 = pages_array.length; _j < _len1; i = ++_j) {
        el = pages_array[i];
        data.append("pages[" + i + "]['filename']", el.filename);
        data.append("pages[" + i + "]['pagenum']", el.page);
        data.append("pages[" + i + "]['rotation']", el.rotation);
      }
      return $.ajax({
        url: $(this).data('url'),
        type: 'POST',
        cache: false,
        processData: false,
        contentType: false,
        data: data,
        beforeSend: function() {
          $('#url').hide();
          $('#url').css('margin-bottom', "-100px");
          return $('.loading').show();
        },
        success: function(data, textStatus, errors) {
          var blob, byteArray, byteCharacters, byteNumbers, url, _k, _len2;
          if (data) {
            byteCharacters = atob(data);
            byteNumbers = new Array(byteCharacters.length);
            for (i = _k = 0, _len2 = byteNumbers.length; _k < _len2; i = ++_k) {
              el = byteNumbers[i];
              byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            byteArray = new Uint8Array(byteNumbers);
            blob = new Blob([byteArray], {
              type: 'application/pdf'
            });
            url = window.URL.createObjectURL(blob);
            $("#url").attr('href', url);
            $('#url').show();
            $("#url").animate({
              'margin-bottom': '0'
            }, 500);
          }
          return $('.loading').hide(1000);
        }
      });
    };
  } else {
    alert('Your browser is outdated. Please consider upgrading to a newer one.');
  }
  $('#files').bind('dragover', handleDragOver);
  $('#files').bind('drop', handleFileSelect);
  $('#files').bind('click', backwardUpload);
  $('#upload-button').bind('click', startUpload);
  $('#hidden-uploader').bind('change', handleFileSelect);
  $('#files').on('click', '*', function(e) {
    return e.stopPropagation();
  });
  $('#files').on('click mouseenter', '.thumbnail', handleImgClick);
  handleRemove();
  return handleRotation();
});

//# sourceMappingURL=pdftool.js.map
