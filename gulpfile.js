
var gulp = require('gulp');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var csso = require('gulp-csso');
var cleanCSS = require('gulp-clean-css');

gulp.task('scripts', function() {
    return gulp.src([

            './app/js/jquery.js',
            './app/js/bootstrap.min.js',
            './app/js/jquery.bxslider.js',
            './app/js/owl.carousel.min.js',
            './app/js/master.js',
            './app/js/custom.js'

        ])
        .pipe(concat('all.js'))
        .pipe(gulp.dest('./app/js/'));
});

gulp.task('styles', function() {
    return gulp.src([
            './app/assets/frontend/css/plugins.css',
            './app/assets/frontend/css/theme.css',
            './app/assets/frontend/css/icon-fonts.css',
            './app/assets/frontend/css/custom.css',
            './app/assets/frontend/css/slick.css',
            './app/assets/frontend/css/slick-theme.css',
            './app/assets/frontend/css/mixin.css'

        ])
        .pipe(concat('jawas.css'))
        .pipe(gulp.dest('./app/assets/frontend/css/'));
});



//pipelining and combination of multiple functions in gulp default
gulp.task('allsass', function(){
    return gulp.src('./playmovies/static/playmovies/scss/styles.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./playmovies/static/playmovies/css/'));
});
gulp.task('alltask', function() {
    return gulp.src([
            './app/assets/frontend/css/raw/plugins.css',
            './app/assets/frontend/css/raw/theme.css',
            './app/assets/frontend/css/raw/icon-fonts.css',
            './app/assets/frontend/css/raw/custom.css',
            './app/assets/frontend/css/raw/slick.css',
            './app/assets/frontend/css/raw/slick-theme.css',
            './app/assets/frontend/css/raw/mixin.css',
            './app/assets/frontend/css/styles.css'
        ])
        // .pipe(watch('./app/assets/frontend/css/*.css'))
        .pipe(concat('jawas1.css'))
        .pipe(csso())
        .pipe(cleanCSS({
            compatibility: 'ie8'
        }))
        .pipe(gulp.dest('./app/assets/frontend/css/'));
});

gulp.task('watch', function() {
    // gulp.watch(['./app/assets/frontend/css/raw/*.*', './app/assets/frontend/css/styles.css'], ['alltask']);
    gulp.watch('./playmovies/static/playmovies/scss/styles.scss', ['allsass']);
});

gulp.task('default', ['allsass', 'alltask', 'watch']);