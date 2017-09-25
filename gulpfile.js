var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var browserSync = require('browser-sync').create();
var autoprefixer = require('gulp-autoprefixer');
var buildPath = 'roadmap-to-html'

/* Server with hot reload and CSS injection */
gulp.task('serve', ['sass', 'js'], function() {
    browserSync.init({
      server: {
        baseDir: buildPath,
        /* Defines custom route to load resources as if they were requested from /roadmap-to-html */
        routes: {
          "/roadmap-to-html": buildPath
        }
      }
    }
  );
  // all browsers reload after tasks are complete.
  gulp.watch("js/*.js", ['js-watch']);
  gulp.watch('sass/**/*.scss',['sass']);
});

gulp.task('sass', function() {
    gulp.src('sass/style.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
        }))
        .pipe(gulp.dest('./' + buildPath + '/css/'))
        .pipe(browserSync.stream());
});

// move JS files to output folder.
gulp.task('js', function () {
    return gulp.src('js/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('./' + buildPath + '/js/'));
});

// ensures the `js` task is complete before
// reloading browsers
gulp.task('js-watch', ['js'], function (done) {
    browserSync.reload();
    done();
});

//Watch task
gulp.task('default',['serve']);
