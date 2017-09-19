var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync').create();

/* Server with hot reload and CSS injection */
gulp.task('serve', ['sass'], function() {
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

    gulp.watch('sass/**/*.scss',['sass']);
});

gulp.task('sass', function() {
    gulp.src('sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./output/css/'))
        .pipe(browserSync.stream());
});

//Watch task
gulp.task('default',['serve']);
