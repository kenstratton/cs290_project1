// preload.js
// 画面更新直後に発生するUIのバグや調整を行います

// アニメーション系プロパティの誤表示を防ぐ要素(.preload)を削除します(Chromのバグが原因だったり)
remove_preload = () => {
    let preload = document.querySelectorAll('.u-preload');
    preload.forEach( (pre) => {
        setTimeout((e) => { // 1秒後に削除(プロジェクト内のアニメーション設定は1秒以内であるため)
            pre.classList.remove('u-preload');
        }, 1000);
    })
}

postload = () => {
    window.addEventListener('load', () => {
        remove_preload();
    })
}

postload();