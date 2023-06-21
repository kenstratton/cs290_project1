// validate.js

// Change input form designs at the Admin > Add User page
let change_form_design = () => {
    let input_list = []
    let error_list = []

    input_list.push(document.getElementById('name'))
    input_list.push(document.getElementById('email'))
    input_list.push(document.getElementById('psw'))

    error_list.push(document.getElementById('error_name'))
    error_list.push(document.getElementById('error_email'))
    error_list.push(document.getElementById('error_psw'))

    for (let i = 0; i < 3; i++) {
        if (error_list[i] && error_list[i].dataset.error == "1")
            input_list[i].classList.add("is-invalid");
    };
};

change_form_design();