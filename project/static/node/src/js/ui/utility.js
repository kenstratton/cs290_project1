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

// 指定要素名とマッチする要素を返します(第1引数: 要素名(String/Array), 第2引数: 任意の親要素
// (戻り値: 複数の要素/単一クラス => Array, 要素名がidのみ => 単一要素)
// 各要素名の構成は、document.querySelector()の引数命名法則に準拠します
// 主なエラー要因: elm_nameに該当する要素が存在しない
get_element = (elm_name, element=null) => {
    // 要素名が複数(Array)の場合
    if (is_array(elm_name)) {
        let elm_array = []
        elm_name.map(en => {
            let elms = (element !== null) ?
            Array.from(element.querySelectorAll(en))
            : Array.from(document.querySelectorAll(en));
            if (en.split(" ").slice(-1)[0].slice(0, 1) === "#") elm_array.push(elms[0]);
            else elm_array.push(...elms);
        })
        return elm_array;
    // 要素名が単一(String)の場合
    } else {
        let elms = (element !== null) ? 
        Array.from(element.querySelectorAll(elm_name))
        : Array.from(document.querySelectorAll(elm_name));
        if (elm_name.split(" ").slice(-1)[0].slice(0, 1) === "#") return elms[0]; 
        else return elms;
    }
}

// オブジェクトHTMLElementかを判断します
// ・obj instanceof HTMLElementで確認できる場合はそれを使用し、
// ・上記で確認できない場合は以下をすべて満たせばHTMLElementだと判断します
//   - オブジェクトのデータ型が "object"
//   - nodeTypeが 1 (ELEMENT_NODE)
//   - styleプロパティのデータ型が "object"
//   - ownerDocumentプロパティのデータ型が "object"
isElement = (obj) => {
    try {
        //Using W3 DOM2 (works for FF, Opera and Chrom)
        return obj instanceof HTMLElement;
    }
    catch(e){
        //Browsers not supporting W3 DOM2 don't have HTMLElement and
        //an exception is thrown and we end up here. Testing some
         //properties that all elements have. (works on IE7)
        return (typeof obj==="object") &&
            (obj.nodeType===1) && (typeof obj.style === "object") &&
            (typeof obj.ownerDocument ==="object");
    }
}