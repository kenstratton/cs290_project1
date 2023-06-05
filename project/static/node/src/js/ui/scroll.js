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

// scrollのクリック先と対象
const scl_elm_name_list = {
    "#l-header__top-entry" : "#p-index-top",
    "#l-header__about-entry" : "#p-index-about",
    "#l-header__modal-opener--p-index-func-channel" : "#p-index-func",
    "#l-header__modal-opener--p-index-func-meeting" : "#p-index-func",
    "#l-header__modal-opener--p-index-func-message" : "#p-index-func",
};

// scroll後にtoggleするクリック先と対象
const scl_toggler_list = {
    "l-header__modal-opener--p-index-func-channel" :  "p-index-func__modal-opener--channel",
    "l-header__modal-opener--p-index-func-meeting" :  "p-index-func__modal-opener--meeting",
    "l-header__modal-opener--p-index-func-message" :  "p-index-func__modal-opener--message",
};

const scl_key_elm_list = get_element(Object.keys(scl_elm_name_list));
const scl_target_elm_list = get_element(Object.values(scl_elm_name_list));

scroll = () => {
    scl_key_elm_list.map(ke => {
        ke.addEventListener('click', () => {

            var ke_idx = scl_key_elm_list.indexOf(ke);
            scl_target_elm_list[ke_idx].scrollIntoView({  
                behavior: 'smooth'
            });

            if (scl_toggler_list[ke.id]) {
                var toggler = document.getElementById(scl_toggler_list[ke.id]);
                var target = get_element(tgl_target_list[toggler.id]);
                toggle_target_data(toggler, target);
                console.log(target);
            }
            
        })
    })
}

scroll();