// flash.js

// flashメッセージ内の「×」が押下された際、該当メッセージを削除します
flash = () => {
    let flash_closer = get_element(".l-header__flash-closer");
    flash_closer.map(fc => {
        fc.addEventListener('click', () => {
            fc.parentNode.remove();
        })
    })
}

flash();