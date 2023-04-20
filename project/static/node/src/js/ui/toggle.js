/* toggle.js ----------------------------------
|   On/Offなどで切り替えるUIデザインを操作します。   |
---------------------------------------------*/

(() => {

// 標準(target)のdata属性に関与し、on / off の値を付与します。
activator = (target) => {
    target.dataset.status = 
        (target.dataset.status == 'off') ? 'on' : 'off';
};

// クラス属性 '.collapser' を所有するbuttonタグにtoggle能力を付与、標準(target)の取得をします
collapseToggler = () => {
    var elms = document.querySelectorAll('.collapser');
    if (!elms[0]) return[];
    for (var i = 0; i < elms.length; i++){
        var dataId = elms[i].dataset.id;
        elms[i].addEventListener('click', () => {
            activator(document.getElementById(dataId))
        });
    };
};

collapseToggler();

})();