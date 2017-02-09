var gulp  = require('gulp');
var $     = require('gulp-load-plugins')();
var debug = require('gulp-debug');

var sassPaths = [
  'node_modules/foundation-sites/scss/',
  'node_modules/motion-ui/src/'
];

gulp.task('sass', function() {
    return gulp.src('scss/app.scss')
        .pipe($.sass({
            includePaths: sassPaths,
            outputStyle: 'compressed' // if css compressed **file size**
        })
            .on('error', $.sass.logError))
        .pipe($.autoprefixer({
            browsers: ['last 2 versions', 'ie >= 9']
        }))
    .pipe(gulp.dest('dist/css/'));
});

gulp.task('js', function() {
  return gulp.src(['node_modules/jquery/dist/jquery.js',
                    'node_modules/what-input/what-input.js',
                    'node_modules/foundation-sites/dist/foundation.js',
                    'js/app.js'])
            .pipe($.concat('app.js'))
            .pipe($.uglify())
            .pipe(gulp.dest('dist/js/'));
});

gulp.task('watch', ['sass', 'js'], function() {
  gulp.watch(['scss/**/*.scss'], ['sass']);
  gulp.watch(['js/**/*.js'], ['js']);
});

gulp.task('default', ['watch']);
