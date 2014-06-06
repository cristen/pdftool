var files_array;

console.log('Starting app');

jQuery.event.props.push('dataTransfer');

files_array = [];

$(document).ready(function() {
  var handleDragOver, handleFileSelect, startUpload;
  if (window.File && window.FileReader && window.FileList && window.Blob) {
    handleFileSelect = function(evt) {
      var files, output;
      evt.stopPropagation();
      evt.preventDefault();
      files = evt.dataTransfer.files;
      files_array.push(files);
      $('#drop').remove();
      $('#files ul').append('<li class="pdf_thumbnail">' + files[0].name + '</li>');
      $('#sortable').sortable({
        placeholder: 'ui-sortable-placeholder',
        start: function(e, ui) {
          return $(this).attr('data-previndex', ui.item.index());
        },
        update: function(e, ui) {
          var newIndex, oldIndex, _ref;
          newIndex = ui.item.index();
          oldIndex = $(this).attr('data-previndex');
          _ref = [files_array[newIndex], files_array[oldIndex]], files_array[oldIndex] = _ref[0], files_array[newIndex] = _ref[1];
          return $(this).removeAttr('data-previndex');
        }
      });
      return output = [];
    };
    handleDragOver = function(evt) {
      evt.stopPropagation();
      evt.preventDefault();
      return evt.dataTransfer.dropEffect = 'copy';
    };
    startUpload = function(evt) {
      var data, el, i, _i, _len;
      evt.stopPropagation();
      evt.preventDefault();
      data = new FormData();
      for (i = _i = 0, _len = files_array.length; _i < _len; i = ++_i) {
        el = files_array[i];
        data.append('files[]', el[0]);
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
          return $('#loading').show();
        },
        success: function(data, textStatus, errors) {
          var blob, byteArray, byteCharacters, byteNumbers, url, _j, _len1;
          byteCharacters = atob(data);
          byteNumbers = new Array(byteCharacters.length);
          for (i = _j = 0, _len1 = byteNumbers.length; _j < _len1; i = ++_j) {
            el = byteNumbers[i];
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          byteArray = new Uint8Array(byteNumbers);
          blob = new Blob([byteArray], {
            type: 'application/pdf'
          });
          url = window.URL.createObjectURL(blob);
          $("#url").attr('href', url);
          $("#url").show();
          return $('#loading').hide();
        }
      });
    };
  } else {
    alert('Your browser is outdated. Please consider upgrading to a newer one.');
  }
  $('#files').bind('dragover', handleDragOver);
  $('#files').bind('drop', handleFileSelect);
  return $('#upload-button').bind('click', startUpload);
});

//# sourceMappingURL=pdftool.js.map
