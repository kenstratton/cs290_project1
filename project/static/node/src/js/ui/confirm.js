// confirm.js

const confirm_btn_list = get_element(".confirm");

confirm_loading = () => {
    if (!confirm_btn_list[0]) return[];
    confirm_btn_list.map(cb => {
        cb.addEventListener('click', () => {
            let result = confirm(cb.dataset.confirm_txt);
            if (result) location.href = cb.dataset.url;
        })
    })
}

confirm_loading();