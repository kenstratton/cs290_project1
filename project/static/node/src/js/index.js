//* SCSS / CSS
import '../scss/style.scss';
import '../../node_modules/@splidejs/splide/dist/css/splide.min.css';

//* JavaScript
import './ui/utility';
import './ui/preload';
import './ui/toggle';
import './ui/modal';
import './ui/scroll';
import './ui/validate';
// import './ui/flexible'; 文字サイズを自動変更 //! 未使用
import './ui/flash';
// import '../../node_modules/@splidejs/splide/dist/js/splide.min.js';
// import './ui/animation';
// import 'bootstrap';

new Splide( '.splide' ).mount()