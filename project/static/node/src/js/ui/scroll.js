/* scroll.js ----------------------------------
|   指定要素までの自動スクロールを行います。
|   Notes :
|   - イベント発生時に特定の画面位置までスクロールします 
|   - 自動スクロール後にUIの切替が期待される場合、以下フローを辿ります
|     - 
|     - toggle.js > toggle_target_data() : モーダル開くなどの場合
|   Cautions :
|   - クリック先要素に<a>は指定しない(ページ更新によりスクロール挙動が行われない為)
|   - 
---------------------------------------------*/

// scrollのクリック先とスクロール先
const SCL_ELM_NAME_LIST = {
    "#l-header__top-entry"   : "#p-index-top",
    "#l-header__about-entry" : "#p-index-about",
    "#l-header__func-entry"  : "#p-index-func",
    "#l-header__modal-opener--p-index-func-channel" : "#p-index-func",
    "#l-header__modal-opener--p-index-func-meeting" : "#p-index-func",
    "#l-header__modal-opener--p-index-func-message" : "#p-index-func",
};

// scroll後にtoggleするクリック先と切替対象
const SCL_TOGGLER_LIST = {
    "l-header__modal-opener--p-index-func-channel" :  "p-index-func__modal-opener--channel",
    "l-header__modal-opener--p-index-func-meeting" :  "p-index-func__modal-opener--meeting",
    "l-header__modal-opener--p-index-func-message" :  "p-index-func__modal-opener--message",
};

// クリック先(key)およびスクロール先(value)の各要素を配列に格納
const SCL_KEY_ELM_LIST = get_element(Object.keys(SCL_ELM_NAME_LIST));
const SCL_TARGET_ELM_LIST = get_element(Object.values(SCL_ELM_NAME_LIST));

scroll = () => {
    if (!SCL_KEY_ELM_LIST[0]) return [];
    SCL_KEY_ELM_LIST.map(ke => {
        ke.addEventListener('click', () => {

            let ke_idx = SCL_KEY_ELM_LIST.indexOf(ke);
            let rect_top = SCL_TARGET_ELM_LIST[ke_idx].getBoundingClientRect().top;
            let position_y = window.pageYOffset;
            let target = rect_top + position_y;
            let header = get_element("#l-header");
            if (header) target -= header.clientHeight;
            window.scrollTo({
                top: target,
                behavior: 'smooth',
            });

            if (SCL_TOGGLER_LIST[ke.id]) {
                let toggler = document.getElementById(SCL_TOGGLER_LIST[ke.id]);
                let target = get_element(TGL_TARGET_LIST[toggler.id]);
                toggle_target_data(toggler, target);
            }
        })
    })
}

scroll();