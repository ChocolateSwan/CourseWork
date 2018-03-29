const another_site_flag = document.getElementById('another_site_flag');
const another_site = document.getElementById('another_site');
const select_url = document.getElementById('select_url');
another_site.disabled = true;
another_site_flag.onchange = function() {
    another_site.disabled = !this.checked;
    select_url.disabled = !!this.checked;
};