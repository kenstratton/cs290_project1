// form.js

/* -----------------------------------
|   パスワード入力欄のテキスト可視化します  |
------------------------------------*/

const INPUT_PASSWORD_SET = get_element(["#psw", "#conf"]);
const VISUALIZER = get_element("#p-form__password-visualizer");

visualize_password = () => {
    if (!INPUT_PASSWORD_SET[0] || !VISUALIZER) return[];
    VISUALIZER.addEventListener('click', () => {
        if (INPUT_PASSWORD_SET[0].type === "password") {
            INPUT_PASSWORD_SET.map(pi => { if (isElement(pi)) pi.type = "text"; })
            VISUALIZER.firstElementChild.style.display = "none";
            VISUALIZER.lastElementChild.style.display = "block";
        } else {
            INPUT_PASSWORD_SET.map(pi => { if (isElement(pi)) pi.type = "password"; })
            VISUALIZER.firstElementChild.style.display = "block";
            VISUALIZER.lastElementChild.style.display = "none";
        }
    })
}

visualize_password();




/* --------------------------------------------------------------------
|   フォーム内のチェックボックスの状態に応じて対象のinput要素をdisabled化します  |
---------------------------------------------------------------------*/

const CHECKBOXES = get_element(".p-form__disabled-trigger");
const INPUT_NAME = get_element("#name");
const INPUT_PSW = get_element("#psw");
const INPUT_PSW_CONF = get_element("#conf");
// const TRIGGERS = [CHECKBOX_ADMIN, CHECKBOX_PSW_DISABLED];


// チェックボックスの状態に応じて対象をdisabled化します
checkbox_toggle_disabled = (checkbox=null, target=null) => {
    if (!checkbox || !target) return [];

    if (is_array(target)) {
        target.map(trgt => {
            trgt.disabled = (checkbox.checked) ? true : false;
        })
    } else {
        target.disabled = (checkbox.checked) ? true : false;
    }
}

// チェックボックスの初期状態に応じて対象のinput要素をdisabled化します
checkbox_set_disabled = () => {
    CHECKBOXES.map(cb => {
        // 名前のdisabled化
        if (cb.id == "admin") {
            checkbox_toggle_disabled(cb, INPUT_NAME);
        }

        // パスワードのdisabled化
        if (cb.id == "psw_disabled") {
            checkbox_toggle_disabled(cb, [INPUT_PSW,INPUT_PSW_CONF]);
        }
    })
    return[];
}

// チェックボックスの変更に応じて対象のinput要素をdisabled化します
checkbox_disable_input = () => {
    CHECKBOXES.map(cb => {
        cb.addEventListener('change', () => {
            // 名前のdisabled化
            if (cb.id == "admin") {
                checkbox_toggle_disabled(cb, INPUT_NAME);
            }

            // パスワードのdisabled化
            if (cb.id == "psw_disabled") {
                checkbox_toggle_disabled(cb, [INPUT_PSW,INPUT_PSW_CONF]);
            }
        })
    })
}

if (CHECKBOXES[0]) {
    checkbox_set_disabled();
    checkbox_disable_input();
}