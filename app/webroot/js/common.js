//Global event handler storage
var _eventHandlers = {};
var opts = {
    lines: 13 // The number of lines to draw
        ,
    length: 28 // The length of each line
        ,
    width: 14 // The line thickness
        ,
    radius: 42 // The radius of the inner circle
        ,
    scale: 1 // Scales overall size of the spinner
        ,
    corners: 1 // Corner roundness (0..1)
        ,
    color: '#bdbdbd' // #rgb or #rrggbb or array of colors
        ,
    opacity: 0.25 // Opacity of the lines
        ,
    rotate: 0 // The rotation offset
        ,
    direction: 1 // 1: clockwise, -1: counterclockwise
        ,
    speed: 1 // Rounds per second
        ,
    trail: 60 // Afterglow percentage
        ,
    fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
        ,
    zIndex: 1001 // The z-index (defaults to 2000000000)
        ,
    className: 'spinner' // The CSS class to assign to the spinner
        ,
    top: '50%' // Top position relative to parent
        ,
    left: '50%' // Left position relative to parent
        ,
    shadow: false // Whether to render a shadow
        ,
    hwaccel: false // Whether to use hardware acceleration
        ,
    position: 'absolute' // Element positioning
};
var spinner = new Spinner(opts);

function addListener(node, event, handler, capture) {
    if(!(node in _eventHandlers)) {
        // _eventHandlers stores references to nodes
        _eventHandlers[node] = {};
    }
    if(!(event in _eventHandlers[node])) {
        // each entry contains another entry for each event type
        _eventHandlers[node][event] = [];
    }
    // capture reference
    _eventHandlers[node][event].push([handler, capture]);
    node.addEventListener(event, handler, capture);
 }

function removeAllListeners(node, event) {
    if(node in _eventHandlers) {
        var handlers = _eventHandlers[node];
        if(event in handlers) {
            var eventHandlers = handlers[event];
            for(var i = eventHandlers.length; i--;) {
                var handler = eventHandlers[i];
                node.removeEventListener(event, handler[0], handler[1]);
            }
        }
    }
}

function loadScript(url, callback) {

    var script = document.createElement("script");
    script.id = url;
    script.type = "text/javascript";

    if (script.readyState) { //IE
        script.onreadystatechange = function() {
            if (script.readyState == "loaded" ||
                script.readyState == "complete") {
                script.onreadystatechange = null;
                if (callback != undefined) {
                    callback();
                }
            }
        };
    } else { //Others
        script.onload = function() {
            if (callback != undefined) {
                callback();
            }
        };
    }

    script.src = url;
    var script_node = document.getElementById(url);
    if (script_node != null) {
        script_node.remove();
    }

    document.getElementsByTagName("head")[0].appendChild(script);
}

/* Helper functions */
function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return 'i' + s4() + s4() + s4() + s4() + s4() + s4();
}

function ajaxGet(data_link, target, init_link, event) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            target.innerHTML = xhttp.responseText;
            if (event != undefined) {
                target.dispatchEvent(event);
            }
            if (init_link != undefined) {
                loadScript(init_link)
            }
        }
    };
    xhttp.open("GET", data_link, true);
    xhttp.setRequestHeader("X-Requested-With", 'XMLHttpRequest');
    xhttp.send();
}

function ajaxPost(data_link, target, form, init_link, event) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            target.innerHTML = xhttp.responseText;
            if (event != undefined) {
                target.dispatchEvent(event);
            }
            if (init_link != undefined) {
                loadScript(init_link)
            }
        }
    };
    xhttp.open("POST", data_link, true);
    xhttp.setRequestHeader("X-Requested-With", 'XMLHttpRequest');
    xhttp.send(form);
}

function hasClass(el, className) {
    if (el.classList)
        return el.classList.contains(className);
    else
        return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))
}

function addClass(el, className) {
    if (el.classList)
        el.classList.add(className);
    else if (!hasClass(el, className)) el.className += " " + className
}

function removeClass(el, className) {
    if (el.classList)
        el.classList.remove(className);
    else if (hasClass(el, className)) {
        var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
        el.className = el.className.replace(reg, ' ')
    }
}

function eventFire(el, etype) {
    if (el.fireEvent) {
        el.fireEvent('on' + etype);
    } else {
        var evObj = document.createEvent('Events');
        evObj.initEvent(etype, true, false);
        el.dispatchEvent(evObj);
    }
}

function initializeForm(form, modal, event) {
    var submit = form.querySelector('.modal-submit');

    if (submit != undefined) {
        submit.addEventListener('click', function(ev) {
            ev.stopPropagation();
            submitForm(form, modal, event);
        });
    }
}

function submitForm(form, modal, event) {
    var data_link = form.getAttribute('data-link');
    var formData = new FormData();
    [].forEach.call(form.querySelectorAll('.input'), function(el) {
        var input = el.childNodes[1];
        var name = input.id;
        var data;

        if (input.localName == 'input') {
            if (input.type == 'file' && input.files.length > 0) {
                data = input.files[0];
            } else {
                data = input.value;

            }
        } else if (input.localName == 'select') {
            data = input.options[input.selectedIndex].text;
        }

        if (data != undefined) {
            formData.append(name, data);
        }
    });
    ajaxPost(data_link, modal, formData, undefined, event);
}