// utility.js

// 引数がStringか否かを判別します(戻り値: Boolean)
is_string = (target) => {
    if(typeof target === "string") return true;
    else return false;
}

// 引数がArrayか否かを判別します(戻り値: Boolean)
is_array = (target) => {
    if(Array.isArray(target)) return true;
    else return false;
}

// 文字列内に羅列したid名を持つタグを返します(戻り値: Array) //! 未使用
// 文字列内にてidを分割する際は1スペース(例: "hi hey")
// get_elms_from_str_id = (str) => {
//     if (!is_string(str)) return [];
//     var ids = str.split("  ");
//     return ids.map(id => document.getElementById(id));
// }

// 指定要素(複数可)が、指定クラス名を有するか判別します(戻り値: Boolean) //! 未使用
// is_classname_present = (target, class_name) => {
//     if (is_array(target)) {
//         target.find( trg => {
//             if (trg.classList.contains(class_name)) return true;
//         })
//     } else {
//         if (target.classList.contains(class_name)) return true;
//     }
//     return false;
// }

// 指定要素名とマッチする要素を返します(第1引数: 要素名(String/Array), 第2引数: 任意の親要素
// (戻り値: 複数の要素/単一クラス => Array, 要素名がidのみ => 単一要素)
// 各要素名の構成は、document.querySelector()の引数命名法則に準拠します
// 主なエラー要因: elm_nameに該当する要素が存在しない
get_element = (elm_name, element=null) => {
    // 要素名が複数(Array)の場合
    if (is_array(elm_name)) {
        var elm_array = []
        elm_name.map(en => {
            var elms = (element !== null) ?
            Array.from(element.querySelectorAll(en))
            : Array.from(document.querySelectorAll(en));
            if (en.split(" ").slice(-1)[0].slice(0, 1) === "#") elm_array.push(elms[0]);
            else elm_array.push(...elms);
        })
        return elm_array;
    // 要素名が単一(String)の場合
    } else {
        var elms = (element !== null) ? 
        Array.from(element.querySelectorAll(elm_name))
        : Array.from(document.querySelectorAll(elm_name));
        if (elm_name.split(" ").slice(-1)[0].slice(0, 1) === "#") return elms[0]; 
        else return elms;
    }
}

// 指定要素の兄弟要素を返します(戻り値: Array) //! 未使用
// get_siblings = (elm) => {
//     return Array.from(elm.parentNode.children);
// }

// 指定要素の兄弟から、指定クラス名とマッチする要素を返します(戻り値: Array) //! 未使用
// get_class_from_siblings = (elm, class_name) => {
//     return Array.from(elm.parentNode.getElementsByClassName(class_name));
// }