/* ie fix provided by mozilla */
(function() {
    function CustomEvent(event, params) {
        params = params || {
            bubbles: false,
            cancelable: false,
            detail: undefined
        };
        var evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
        return evt;
    }

    CustomEvent.prototype = window.Event.prototype;

    window.CustomEvent = CustomEvent;
})();

(function() {
    var menu_el = document.getElementById('menu');
    var links = [].slice.call(menu_el.querySelectorAll('.menu-item'));
    links.forEach(function(item) {
        item.querySelector('a').addEventListener('click', function(ev) {
            // add class current
            var current_link = menu_el.querySelector('.menu-link--current');
            if (current_link) {
                removeClass(menu_el.querySelector('.menu-link--current'), 'menu-link--current');
            }
            addClass(ev.target, 'menu-link--current');
            var data_link = item.getAttribute('data-link');
            var init_link = item.getAttribute('init-link');

            if (data_link !== null) {
                ajaxLoader(ev, data_link, init_link);
            }
        });
    });

    var gridWrapper = document.querySelector('.content');

    function ajaxLoader(ev, data_link, init_link) {
        ev.preventDefault();
        gridWrapper.innerHTML = '';
        addClass(gridWrapper, 'content--loading');
        setTimeout(function() {
            removeClass(gridWrapper, 'content--loading');
            ajaxGet(data_link, gridWrapper, init_link);
        }, 700);
    }
})();
