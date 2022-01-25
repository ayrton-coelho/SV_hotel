function clearform() {
    form = document.querySelector("#main_form");
    form.reset();
}

const date_field = document.getElementById('fecha');
const date = new Date();
let y = date.getFullYear();
let m = date.getMonth() + 1;
let d = date.getDate();
if (d < 10) {
    d = '0' + d;
}
if (m < 10) {
    m = '0' + m;
}

const today = y + '-' + m + '-' + d;
date_field.setAttribute('min', today);