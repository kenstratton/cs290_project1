// modal.js

// モーダル内の画像切替を行います
// サムネとメイン画像をそれぞれ配列化した場合、クリックされたサムネの配列位置と同位置となるメイン画像を表示します
var modal_img_swapper = () => {
    var thumnail_lists = get_element(".modal-thumnails");
    if (!thumnail_lists[0]) return[];

    thumnail_lists.map(thum_li => {
        var thum_imgs = get_element("img", thum_li);
        thum_imgs.map(thm => {
            thm.addEventListener('click', () => {
                if (thm.dataset.status != "on") {
                    var main_imgs = Array.from(get_element(".modal-mainimages", thum_li.parentNode)[0].children);
                    var thum_index = thum_imgs.indexOf(thm);
                    // サムネの配列位置と同位置となるメイン画像を表示します
                    main_imgs.map(mn => {
                        if (main_imgs.indexOf(mn) == thum_index) mn.style.order = "1";
                        else mn.style.order = "2";
                    })
                    // サムネのUIを切り替えます(サムネが一つの場合、切替なし)
                    if (thum_imgs.length > 1) toggle_target_data(thm, [], thum_imgs); 
                }
            })
        })
    })
};

modal_img_swapper();