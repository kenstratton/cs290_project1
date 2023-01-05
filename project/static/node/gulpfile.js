/* gulpfile.js */


// Load plugins
// var 
//     gulp = require('gulp'),
//     gulpsass = require('gulp-sass')(require('sass'));

// // Bootstrap scss source
// var bootstrapSass = {
//         in: './node_modules/bootstrap-sass/'
//     };

// // Default task
// gulp.task('default', function() {
//     return gulp.src('./src/scss/**/*scss')    // Specify a directory with scss files 
//         .pipe(gulpsass({                      // Compile（sass->css）
//             includePaths: [bootstrapSass.in + 'assets/stylesheets']
//         }))
//         .pipe(gulp.dest('./src/css/'));       // Output a compiled css
// });


// // source and distribution folder
// var
//     source = 'src/',
//     dest = 'dist/';

// // Bootstrap scss source
// var bootstrapSass = {
//         in: './node_modules/bootstrap-sass/'
//     };

// // fonts
// var fonts = {
//         in: [source + 'fonts/*.*', bootstrapSass.in + 'assets/fonts/**/*'],
//         out: dest + 'fonts/'
//     };

// // css source file: .scss files
// var scss = {
//     in: source + 'scss/main.scss',
//     out: dest + 'css/',
//     watch: source + 'scss/**/*',
//     sassOpts: {
//         outputStyle: 'nested',
//         precison: 3,
//         errLogToConsole: true,
//         includePaths: [bootstrapSass.in + 'assets/stylesheets']
//     }
// };

// // copy bootstrap required fonts to dest
// gulp.task('fonts', function () {
//     return gulp
//         .src(fonts.in)
//         .pipe(gulp.dest(fonts.out));
// });

// // compile scss
// gulp.task('sass', ['fonts'], function () {
//     return gulp.src(scss.in)
//         .pipe(sass(scss.sassOpts))
//         .pipe(gulp.dest(scss.out));
// });

// // default task
// gulp.task('default', ['sass'], function () {
//      gulp.watch(scss.watch, ['sass']);
// });