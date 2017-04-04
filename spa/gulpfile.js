// Generated on 2016-07-13 using generator-angular 0.15.1
'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var openURL = require('open');
var lazypipe = require('lazypipe');
var rimraf = require('rimraf');
var wiredep = require('wiredep').stream;
var runSequence = require('run-sequence');
var process = require('process');
var karma = require('karma');

var yeoman = {
  app: require('./bower.json').appPath || 'app',
  dist: 'dist'
};

var paths = {
  scripts: [yeoman.app + '/scripts/**/*.js'],
  styles: [yeoman.app + '/styles/**/*.scss'],
  views: {
    main: yeoman.app + '/index.html',
    files: [yeoman.app + '/views/**/*.html']
  }
};

////////////////////////
// Reusable pipelines //
////////////////////////

var lintScripts = lazypipe()
  .pipe($.jshint, '.jshintrc')
  .pipe($.jshint.reporter, 'jshint-stylish');

var styles = lazypipe()
  .pipe($.sass, {
    outputStyle: 'expanded',
    precision: 10
  })
  .pipe($.autoprefixer, 'last 1 version')
  .pipe(gulp.dest, '.tmp/styles');

///////////
// Tasks //
///////////

gulp.task('styles', function() {
  return gulp.src(paths.styles)
    .pipe(styles());
});

gulp.task('lint:scripts', function() {
  return gulp.src(paths.scripts)
    .pipe(lintScripts());
});

gulp.task('clean:tmp', function(cb) {
  rimraf('./.tmp', cb);
});

gulp.task('serve:prod', ['build'], function() {
  $.connect.server({
    root: [yeoman.dist],
    host: '0.0.0.0',
    port: 9000,
    fallback: yeoman.dist + '/index.html'
  });
});

// inject bower components
gulp.task('bower', function() {
  return gulp.src(paths.views.main)
    .pipe(wiredep({
      ignorePath: '..'
    }))
    .pipe(gulp.dest(yeoman.app));
});

///////////
// Build //
///////////

gulp.task('clean:dist', function(cb) {
  rimraf('./dist', cb);
});

gulp.task('client:build', ['html', 'styles'], function() {
  var jsFilter = $.filter('**/*.js');
  var cssFilter = $.filter('**/*.css');

  return gulp.src(paths.views.main)
    .pipe($.useref({
      searchPath: [yeoman.app, '.tmp']
    }))
    .pipe(jsFilter)
    .pipe($.ngAnnotate())
    .pipe(jsFilter.restore())
    .pipe(cssFilter)
    .pipe($.minifyCss({
      cache: true
    }))
    .pipe(cssFilter.restore())
    .pipe(gulp.dest(yeoman.dist));
});

gulp.task('html', function() {
  return gulp.src(yeoman.app + '/views/**/*')
    .pipe(gulp.dest(yeoman.dist + '/views'));
});

gulp.task('copy:extras', function() {
  return gulp.src(yeoman.app + '/*/.*', {
      dot: true
    })
    .pipe(gulp.dest(yeoman.dist));
});

gulp.task('copy:fonts', function() {
  return gulp.src(yeoman.app + '/fonts/**/*')
    .pipe(gulp.dest(yeoman.dist + '/fonts'));
});

gulp.task('build', ['clean:dist'], function() {
  runSequence(['copy:extras', 'copy:fonts', 'client:build']);
});

gulp.task('default', ['build']);
