const another_site_flag = document.getElementById('another_site_flag');
const another_site = document.getElementById('another_site');
const select_url = document.getElementById('select_url');
another_site_flag.onchange = function() {
  another_site.disabled = !this.checked;
  if (this.checked) {
        select_url.attr('disabled', 'disabled');
    } else {
        select_url.removeAttr('disabled');
    }
};