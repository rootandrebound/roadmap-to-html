var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync').create();

/* Server with hot reload and CSS injection */
gulp.task('serve', ['sass', 'js'], function() {
    browserSync.init({
      server: {
        baseDir: "output",
        /* Defines custom route to load resources as if they were requested from /roadmap-to-html */
        routes: {
          "/roadmap-to-html": "output"
        }
      }
    }
  );
  // all browsers reload after tasks are complete.
  gulp.watch("js/*.js", ['js-watch']);
  gulp.watch('sass/**/*.scss',['sass']);
});

gulp.task('sass', function() {
    gulp.src('sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./output/css/'))
        .pipe(browserSync.stream());
});

// move JS files to output folder.
gulp.task('js', function () {
    return gulp.src('js/*.js')
        .pipe(gulp.dest('./output/js/'));
});

// ensures the `js` task is complete before
// reloading browsers
gulp.task('js-watch', ['js'], function (done) {
    browserSync.reload();
    done();
});

//Watch task
gulp.task('default',['serve']);
