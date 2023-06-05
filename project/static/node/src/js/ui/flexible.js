// flexible.js 

// 画角や親要素枠に合わせて要素の縮小などを行います

// 文字列が枠内に収まるようにfont-sizeを調節します
optimize_text_size = () => {
    let texts = get_element(".txt-optimizer");
    texts.map(txt => {
        console.log(txt.scrollHeight);
        console.log(txt.getBoundingClientRect().height);
        for (
            let size = txt.style.getPropertyValue("font-size");
            txt.scrollHeight > txt.getBoundingClientRect().height && size > 1;
            size--
            ) {
                console.log(txt.scrollHeight);
                console.log(txt.getBoundingClientRect().height);
                textElem.style.fontSize = size + "px";
            }
    })
}

optimize_text_size();