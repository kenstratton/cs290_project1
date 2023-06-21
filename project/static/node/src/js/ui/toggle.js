/* toggle.js ----------------------------------
|   On/Offで切り替えるUIデザインを操作します。   
|   Rules :
|   - .togglerがクリックされると切替挙動を行います
|   - UIの切替は、.togglerおよび切替要素のdata属性(data-status)に On / Off を指定することで行います
|   - 特定の.togglerと対応する切替要素のハッシュリストはTGL_TARGET_LISTになります(dist/ignored/js/variable.jsにて定義)
|   - target_list構成(1) => key(id名) : [要素名(string), ...]
|   - target_list構成(2) => key(id名) : [[*1], [*2]]
|     - *1 => togglerクラスのdata-statusと同値を所持する要素(例: toggler(on) => on)
|     - *2 => togglerクラスのdata-statusと逆値を所持する要素(例: toggler(on) => off)
---------------------------------------------*/

// togglerクラスと切替対象のdata-statusを変更(togglerと同値: target, 逆値: anti-target)
toggle_target_data = (toggler, target, anti_target=null) => {
    if (anti_target !== null) {
        anti_target.map(anti => {
            if (anti !== null) anti.dataset.status = (toggler.dataset.status !== "on") ? "off" : "on";
        })
    }
    toggler.dataset.status = (toggler.dataset.status !== 'on') ? 'on' : 'off';
    if (target[0]) target.map(trg => {
        if (trg !== null) trg.dataset.status = toggler.dataset.status;
    })
}

// .toggler クリック時、TGL_TARGET_LISTから対象の切替要素を検索
// => .toggler および切替対象のdata-statusに on / off の値を指定
toggle = () => {
    let togglers = get_element('.toggler');
    if (!togglers[0]) return [];
    togglers.map(tgl => {
        tgl.addEventListener('click', () => {
            let target = null;
            let anti_target = null;
            // togglerの対象がid検索の場合 (togglerがTGL_TARGET_LISTのキー値であるid値を有する)
            if (typeof TGL_TARGET_LIST[tgl.id] !== "undefined") {
                // 二重配列(逆値の枠)が設けられている場合
                if (is_array(TGL_TARGET_LIST[tgl.id][0])) {
                    target = get_element(TGL_TARGET_LIST[tgl.id][0]);
                    anti_target = get_element(TGL_TARGET_LIST[tgl.id][1]);
                // 配列要素が文字列のみ(同値の枠のみ)の場合
                } else { target = get_element(TGL_TARGET_LIST[tgl.id]); }
            // togglerの対象が同じタグ内の兄弟要素の場合 (対象のクラス名 : tgl-reactor)
            } else { target = get_element(".tgl-reactor", tgl.parentNode); }

            if (typeof anti_targe !== "undefined") toggle_target_data(tgl, target, anti_target)
            else toggle_target_data(tgl, target);
        })
    })
}

toggle();