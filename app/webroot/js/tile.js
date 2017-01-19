/* Tile functions */
function replace(a, b) {
    fade(a);
    unfade(b);
}

function fade(element) {
    var op = 1; // initial opacity
    var timer = setInterval(function() {
        if (op <= 0.1) {
            clearInterval(timer);
            addClass(element, 'hidden');
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 10);
}

function unfade(element) {
    var op = 0.1; // initial opacity
    var timer = setInterval(function() {
        if (op >= 1) {
            clearInterval(timer);
            removeClass(element, 'hidden');
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 10);
}

function TileEffects() {
    [].slice.call(document.querySelectorAll('.tile')).forEach(function(el, i) {

        var front = el.querySelector('.front');
        var back = el.querySelector('.back');

        front.addEventListener('mouseover', function(ev) {
            replace(front, back);
            ev.stopPropagation();
        });

        //Safe mouseout, prevents from firing functions if event happens on children, not outside of actual element
        back.addEventListener('mouseout', function(ev) {
            var list = traverseChildren(back);
            var e = ev.toElement || ev.relatedTarget;
            if (!!~list.indexOf(e)) {
                return;
            }

            replace(back, front);

            ev.stopPropagation();
        });
    });
}

//quick and dirty DFS children traversal,
function traverseChildren(elem) {
    var children = [];
    var q = [];
    q.push(elem);
    while (q.length > 0) {
        var elem = q.pop();
        children.push(elem);
        pushAll(elem.children);
    }

    function pushAll(elemArray) {
        for (var i = 0; i < elemArray.length; i++) {
            q.push(elemArray[i]);
        }
    }
    return children;
}


/* Modals */
function TileModalEffects() {
    var overlay = document.querySelector('.modal-overlay');
    var eventBus = document.querySelector('.event-bus');
    var modal = document.querySelector('.modal');

    [].slice.call(document.querySelectorAll('.modal-trigger')).forEach(function(el, i) {
        var data_link = el.getAttribute('data-link');
        var event = new CustomEvent(data_link);

        var interval = 500;
        var status_link = '/messenger/';

        addClass(eventBus, 'visible');
        function intervalledAjaxGet() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                    eventBus.innerHTML = xhttp.responseText;
                    if (event != undefined) {
                        setTimeout(intervalledAjaxGet, interval);
                    }
                }
            };
            xhttp.open("GET", status_link, true);
            xhttp.setRequestHeader("X-Requested-With", 'XMLHttpRequest');
            xhttp.send();
        }

        function removeModal() {
            modal.innerHTML = "";
            removeClass(modal, 'modal-show');
            var current_menu = document.querySelector('.menu-link--current');
            eventFire(current_menu, "click");
        }

        function loadModal() {
            spinner.spin();
            overlay.appendChild(spinner.el);
            setTimeout(intervalledAjaxGet, interval);
            ajaxGet(data_link, modal, undefined, event);

            addClass(modal, 'modal-show');

            // Close modal if user clicked oudside of it
            //removeAllListeners(overlay, 'click');
            //addListener(overlay, 'click', removeModal, false)
        }

        function modalLoaded() {
             try {
                spinner.stop();
                overlay.removeChild(spinner.el);
            } catch (NotFoundError) {}

            clearTimeout(interval);
            removeClass(eventBus, 'visible');

            var close = modal.querySelector('.modal-close');
            var form = modal.querySelector('.modal-form');

            if (close != undefined) {
                removeAllListeners(close, 'click');
                addListener(close, 'click', function(ev) {
                    ev.stopPropagation();
                    removeModal();
                }, false);
            }

            if (form != undefined) {
                // pass parent modal and event, allowing to control form after submission
                // by dispatching the very same event
                initializeForm(form, modal, event);
            }

            // Evaluate any scripts in modal window
            var modalscript = modal.querySelector('#modalscript');
            if (modalscript != undefined) {
                eval(modalscript.innerHTML);
            }
        }

        removeAllListeners(el, 'click');
        addListener(el, 'click', loadModal, false);
        removeAllListeners(modal, data_link);
        addListener(modal, data_link, modalLoaded, false);
    });
}

TileEffects();
TileModalEffects();