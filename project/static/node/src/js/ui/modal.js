// modal.js

// モーダル内の画像切替を行います
// サムネとメイン画像をそれぞれ配列化した場合、クリックされたサムネの配列位置と同位置となるメイン画像を表示します
var modal_img_swapper = () => {
    let thumnail_lists = get_element(".modal-thumnails");
    if (!thumnail_lists[0]) return[];

    thumnail_lists.map(thum_li => {
        let thum_imgs = get_element("img", thum_li);
        thum_imgs.map(thm => {
            thm.addEventListener('click', () => {
                if (thm.dataset.status != "on") {
                    let main_imgs = Array.from(get_element(".modal-mainimages", thum_li.parentNode)[0].children);
                    let thum_index = thum_imgs.indexOf(thm);
                    // サムネの配列位置と同位置となるメイン画像を表示します
                    main_imgs.map(mn => {
                        mn.style.order = (main_imgs.indexOf(mn) == thum_index) ? "1" : "2";
                    })
                    // サムネのUIを切り替えます(サムネが一つの場合、切替なし)
                    if (thum_imgs.length > 1) toggle_target_data(thm, [], thum_imgs); 
                }
            })
        })
    })
};

modal_img_swapper();