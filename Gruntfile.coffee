module.exports = (grunt) ->
  coffees = 'coffees/**/*.coffee'

  grunt.initConfig
    pkg: grunt.file.readJSON('package.json')

    uglify:
      options:
        banner: '/*! <%= pkg.name %>
          <%= grunt.template.today("yyyy-mm-dd") %> */\n'

      pdftool:
        files:
          'pdftool/static/js/pdftool.min.js': ['pdftool/static/js/pdftool.js']

    coffee:
      pdftool:
        options:
          bare: true
          join: true
          sourceMap: true

        files:
          'pdftool/static/js/pdftool.js': coffees

    coffeelint:
      options:
        no_backticks:
          level: 'ignore'

      pdftool: coffees

    watch:
      options:
        livereload: true

      coffee:
        files: ['Gruntfile.coffee'].concat(coffees)
        tasks: ['coffeelint', 'coffee']

  grunt.loadNpmTasks 'grunt-coffeelint'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  grunt.registerTask 'js', ['coffeelint','coffee', 'uglify:pdftool']
  grunt.registerTask 'dev', ['coffeelint', 'coffee', 'uglify:pdftool', 'watch']
