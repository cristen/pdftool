console.log 'Starting app'

jQuery.event.props.push 'dataTransfer'
files_array = []

$(document).ready ->
  if window.File and window.FileReader and window.FileList and window.Blob
    # It works
    handleFileSelect = (evt) ->
      evt.stopPropagation()
      evt.preventDefault()
      files = evt.dataTransfer.files
      files_array.push(files)
      $('#drop').hide()
      $('#files').append '<p class="pdf_thumbnail">' + files[0].name + '</p>'
      output = []

    handleDragOver = (evt) ->
      evt.stopPropagation()
      evt.preventDefault()
      evt.dataTransfer.dropEffect = 'copy'

    startUpload = (evt) ->
      evt.stopPropagation()
      evt.preventDefault()
      data = new FormData()
      for el, i in files_array
        data.append('files[]', el[0])
      $.ajax
        url: $(@).data 'url'
        type: 'POST'
        cache: false
        processData: false
        contentType: false
        data: data
        beforeSend: () ->
          $('#loading').show()
        success: (data, textStatus, errors) ->
          byteCharacters = atob(data)
          byteNumbers = new Array(byteCharacters.length)
          for el, i in byteNumbers
            byteNumbers[i] = byteCharacters.charCodeAt(i)
          byteArray = new Uint8Array(byteNumbers)
          blob = new Blob([byteArray], {type: 'application/pdf'})
          url = window.URL.createObjectURL(blob)
          $("#url").attr 'href', url
          $("#url").show()
          $('#loading').hide()
  else
    alert('Your browser is outdated. Please consider upgrading to a newer one.')

  $('#files').bind 'dragover', handleDragOver
  $('#files').bind 'drop', handleFileSelect
  $('#upload-button').bind 'click', startUpload
