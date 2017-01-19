var network;
var vlans;
var nodes;
var edges;
var data;

function initializeNetwork() {
    //create network
    var container = document.getElementById('networkbox');
    var options = {
        autoResize: true,
        hover: true,
        height: '100%',
        width: '100%',
        locale: 'en',
        nodes: {
            shape: 'box',
            color: '#1C1D22',
            font: {
                color: '#bdbdbd'
            },
            scaling: {
                min: 10,
                max: 30,
                label: {
                    enabled: true,
                    min: 14,
                    max: 30,
                    maxVisible: 30,
                    drawThreshold: 5
                }
            }
        },
        edges: {
            width: 1,
            length: 200,
            //physics: false,
            fontStrokeColor: "#000000",
            smooth: {
                enabled: false,
                type: "diagonalCross", // "straightCross" "horizontal" "continuous" "discrete"
                roundness: 0.5
            },
            font: {
                size: 8,
                align: 'top',
                color: '#bdbdbd'
            },
            color: {
                inherit: false,
                color: '#3B3D4A'
            }
        },
        layout: {
            randomSeed: undefined, // "undefined" 464992
            improvedLayout: true
        },
        physics: {
            enabled: true
        }
    };

    //initialize
    var async_storage = {
        counter: 0
    };

    var eventBus = document.createElement('div');

    eventBus.addEventListener('topology-loaded', function(e) {
        vlans = async_storage['vlans'];
        nodes = new vis.DataSet(async_storage['nodes']);
        edges = new vis.DataSet(async_storage['edges']);

        //grab the data
        data = {
            nodes: nodes,
            edges: edges
        };
        network = new vis.Network(container, data, options);

        createVlanButtons();
        emergencyToggle();

        NodeModalEffects();
        ButtonModalEffects();

    }, false);

    var event = new CustomEvent('topology-loaded');

    function async_storage_append(data, key, value, eventBus, event) {
        data[key] = value;
        data['counter'] = data['counter'] + 1;
        if (data['counter'] == 3) {
            eventBus.dispatchEvent(event);
        }
    }

    var path = '/topology/';
    getNetworkData('vlans', path, async_storage_append, async_storage, eventBus, event);
    getNetworkData('nodes', path, async_storage_append, async_storage, eventBus, event);
    getNetworkData('edges', path, async_storage_append, async_storage, eventBus, event);
}

// this is used by the main.html AJAX section to get data
function getNetworkData(request, path, callback, storage, eventBus, event) {
    var xhr = new XMLHttpRequest();
    var result;

    xhr.open('GET', path + request); // requests: 'vlans' 'nodes' 'edges'
    xhr.send();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            result = JSON.parse(xhr.responseText);
            callback(storage, request, result, eventBus, event);
        }
    };
}

/*
 * CONTROLS - PHYSICS BUTTONS
 */

function emergencyToggle() {
    HierarchyLROn();
    HierarchyOff();
}

function PhyOff() {
    var options = {
        physics: false
    };
    network.setOptions(options);
}

function PhyOn() {
    var options = {
        physics: true
    };
    network.setOptions(options);
}

/*
 * CONTROLS - LAYOUT BUTTONS
 */

function HierarchyLROn() {
    var options = {
        layout: {
            randomSeed: undefined, // "undefined" 464992
            improvedLayout: true,
            hierarchical: {
                enabled: true, // set TRUE to enable
                levelSeparation: 150,
                nodeSpacing: 100,
                treeSpacing: 200,
                blockShifting: true,
                edgeMinimization: true,
                direction: 'LR', // UD, DU, LR, RL
                sortMethod: 'directed' // hubsize, directed
            }
        }
    };
    network.setOptions(options);
}

function HierarchyOff() {
    var options = {
        layout: {
            hierarchical: {
                enabled: false
            }
        }
    };
    network.setOptions(options);
}

function HierarchyUDOn() {
    var options = {
        layout: {
            randomSeed: undefined, // "undefined" 464992
            improvedLayout: true,
            hierarchical: {
                enabled: true, // set TRUE to enable
                levelSeparation: 150,
                nodeSpacing: 100,
                treeSpacing: 200,
                blockShifting: true,
                edgeMinimization: true,
                direction: 'UD', // UD, DU, LR, RL
                sortMethod: 'directed' // hubsize, directed
            }
        }
    };
    network.setOptions(options);
}

/*
 * VLAN BUTTONS SECTION
 */

function clearVlans() {
    var nIDs = data.nodes.getIds();
    var x;
    for (x = 0; x < nIDs.length; x++) {
        data.nodes.update({
            id: nIDs[x],
            color: '#1C1D22'
        });
    }
    var y;
    var eIDs = data.edges.getIds();
    for (y = 0; y < eIDs.length; y++) {
        data.edges.update({
            id: eIDs[y],
            color: '#3B3D4A',
            width: 1,
            arrows: {
                to: {
                    enabled: false,
                    scaleFactor: 1
                },
                middle: {
                    enabled: false,
                    scaleFactor: 1
                },
                from: {
                    enabled: false,
                    scaleFactor: 1
                }
            }
        });
    }
}

function createVlanButtons() {
    var wrapper = document.getElementById("vlanbox-container");
    wrapper.innerHTML = "";

    var i;
    var button;
    var text;

    button = document.createElement("button");
    text = document.createTextNode('No VLANs');
    button.appendChild(text);
    button.setAttribute('class', 'vlanbtn');
    button.setAttribute('id', 'activebtn');
    button.addEventListener("click", function(event) {
        clearVlans();
        document.getElementById('activebtn').removeAttribute('id');
        event.target.setAttribute('id', 'activebtn');
    });
    wrapper.appendChild(button);

    for (i = 0; i < vlans.length; i++) {
        button = document.createElement("button");
        text = document.createTextNode("VLAN: " + vlans[i]);
        button.appendChild(text);
        button.setAttribute('value', vlans[i]);
        button.setAttribute('class', 'vlanbtn');
        button.addEventListener("click", function(event) {
            // clear coloring
            clearVlans();
            // switch active button css style
            document.getElementById('activebtn').removeAttribute('id');
            event.target.setAttribute('id', 'activebtn');
            // color nodes
            var vlanNodes = data.nodes.getIds({
                filter: function(item) {
                    var l = item.vlan.length;
                    var key = event.target.value;
                    var match = false;
                    for (var k = 0; k < l; k++) {
                        if (item.vlan[k] == key) {
                            match = true;
                        }
                    }
                    return match;
                }

            });
            var j;
            for (j = 0; j < vlanNodes.length; j++) {
                data.nodes.update({
                    id: vlanNodes[j],
                    color: '#5C5EDC'
                });
            }
            // color edges
            var targetVlan = event.target.value;
            var vlanEdges = data.edges.getIds({
                filter: function(item) {
                    var edgeVlans = Object.keys(item.vlan);
                    var p = edgeVlans.length;
                    var key = event.target.value;
                    var match = false;
                    for (var q = 0; q < p; q++) {
                        if (edgeVlans[q] == key) {
                            match = true;
                        }
                    }
                    return match;
                }

            });
            var m;
            var currentEdge;
            var currentPvid;
            for (m = 0; m < vlanEdges.length; m++) {
                currentEdge = data.edges.get(vlanEdges[m]);
                currentPvid = currentEdge.vlan[targetVlan];
                switch (currentPvid) {
                    case 'both':
                        data.edges.update({
                            id: vlanEdges[m],
                            arrows: 'to;from',
                            color: '#5C5EDC',
                            width: 3
                        });
                        break;
                    case 'to':
                        data.edges.update({
                            id: vlanEdges[m],
                            arrows: 'to',
                            color: '#5C5EDC',
                            width: 3
                        });
                        break;
                    case 'from':
                        data.edges.update({
                            id: vlanEdges[m],
                            arrows: 'from',
                            color: '#5C5EDC',
                            width: 3
                        });
                        break;
                    case 'none':
                        data.edges.update({
                            id: vlanEdges[m],
                            color: '#5C5EDC',
                            width: 3
                        });
                        break;
                    default:
                        data.edges.update({
                            id: vlanEdges[m],
                            color: '#5C5EDC',
                            width: 3
                        });
                }
            }
        });

        wrapper.appendChild(button);
    }
}

function NodeDetails(scope) {
    var interface_selector = scope.querySelector("#interface");
    var vlans_table = scope.querySelector('#vlans');

    var vlans_selector = scope.querySelector("#vlan");
    var interfaces_table = scope.querySelector('#interfaces');

    function load_interfaces() {
        var data_link = "/topology/vlan/" + vlans_selector.value;
        ajaxGet(data_link, interfaces_table, undefined, undefined);
    }

    function load_vlans() {
        var data_link = "/topology/interface/" + interface_selector.value;
        ajaxGet(data_link, vlans_table, undefined, undefined);
    }

    interface_selector.addEventListener('change', load_vlans);
    vlans_selector.addEventListener('change', load_interfaces);

    load_vlans();
    load_interfaces();
}

function EdgeDelete(scope) {
    var target_node = scope.querySelector("#target_node");
    var target_node_id = scope.querySelector("#target_node_id");

    var target_interface = scope.querySelector('#target_interface');
    var target_interface_id = scope.querySelector("#target_interface_id");

    var source_interface_selector = scope.querySelector("#source_interface");
    var source_interface_id = scope.querySelector("#source_interface_id");

    var async_storage = {};
    var eventBus = document.createElement('div');


    function getEdgeDetails() {
        var custom_event = guid();
        var async_loaded_event = new CustomEvent(custom_event);
        source_interface_id.value = source_interface_selector.value;
        async_storage = {};
        eventBus.remove();
        document.createElement('div');

        function asyncLoaded() {
            var connection = async_storage['connection'];
            if (connection['empty'] == true) {
                target_interface.value = null;
                target_interface_id.value = null;
                target_node.value = null;
                target_node_id.value = null;
                return
            }
            target_interface.value = connection['interface_name'];
            target_interface_id.value = connection['interface_id'];
            target_node.value = connection['node_name'];
            target_node_id.value = connection['node_id'];
        }

        addListener(eventBus, custom_event, asyncLoaded, false);

        function async_storage_append(data, key, value, eventBus, event) {
            data[key] = value;
            eventBus.dispatchEvent(event);
            removeAllListeners(eventBus, asyncLoaded);
        }

        var path = '/topology/interface/' + source_interface_id.value + '/';
        getNetworkData('connection', path, async_storage_append, async_storage, eventBus, async_loaded_event);
    }

    removeAllListeners(source_interface_selector, getEdgeDetails);
    addListener(source_interface_selector, 'change', getEdgeDetails, false);
    getEdgeDetails();

}

function TargetNodeInterfaces(scope) {
    var target_node_selector = scope.querySelector("#target_node");
    var target_interface_selector = scope.querySelector('#target_interface');

    var source_interface_selector = scope.querySelector("#source_interface");
    var source_interface_input = scope.querySelector("#source_interface_id");

    var target_node_input = scope.querySelector("#target_node_id");
    var target_interface_input = scope.querySelector("#target_interface_id");

    function set_source_interface_id() {
        source_interface_input.value = source_interface_selector.value
    }

    var interfaces_loaded_event = new CustomEvent('interfaces-loaded');
    function load_interfaces() {
        var data_link = "/topology/node/" + target_node_selector.value + "/available_interfaces";
        ajaxGet(data_link, target_interface_selector, undefined, interfaces_loaded_event);
        target_node_input.value = target_node_selector.value
    }

    function set_target_interface_id() {
        target_interface_input.value = target_interface_selector.value
    }

    target_node_selector.addEventListener('change', load_interfaces);
    source_interface_selector.addEventListener('change', set_source_interface_id);
    target_interface_selector.addEventListener('change', set_target_interface_id);
    target_interface_selector.addEventListener('interfaces-loaded', set_target_interface_id);

    set_source_interface_id();
    load_interfaces();
}

function NodeModalEffects() {
    var overlay = parent.document.querySelector('.modal-overlay');
    var modal = parent.document.querySelector('.modal');

    network.on("doubleClick", function(params) {
        if (params.nodes.length == 0) {
            return;
        }

        var node_id = params.nodes[0];
        var data_link = "/topology/details/" + node_id;

        // Use unique event ids, otherwise we are listening to all modals
        var event_guid = guid();
        var event = new CustomEvent(event_guid);

        spinner.spin();
        overlay.appendChild(spinner.el);
        ajaxGet(data_link, modal, undefined, event);

        addClass(modal, 'modal-show');

        // Close modal if user clicked oudside of it
        //overlay.removeEventListener('click', removeModal);
        //overlay.addEventListener('click', removeModal);

        function removeModal() {
            modal.innerHTML = "";
            removeClass(modal, 'modal-show');
        }

        modal.addEventListener(event_guid, function(ev) {
            try {
                spinner.stop();
                overlay.removeChild(spinner.el);
            } catch (NotFoundError) {}
            var close = modal.querySelector('.modal-close');
            var form = modal.querySelector('.modal-form');

            if (close != undefined) {
                close.addEventListener('click', function(ev) {
                    ev.stopPropagation();
                    removeModal();
                });
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
        });
    });
}

function ButtonModalEffects() {
    var overlay = document.querySelector('.modal-overlay');
    var modal = document.querySelector('.modal');

    [].slice.call(document.querySelectorAll('.modal-trigger')).forEach(function(el, i) {
        var data_link = el.getAttribute('data-link');
        var event = new CustomEvent(data_link);

        function removeModal() {
            modal.innerHTML = "";
            removeClass(modal, 'modal-show');
            var current_menu = document.querySelector('.menu-link--current');
            eventFire(current_menu, "click");
        }

        function loadModal() {
            var selected_nodes = network.getSelectedNodes();
            if (selected_nodes.length == 0 && data_link.indexOf('[id]') !== -1) {
                return
            }
            var selected_node = selected_nodes[0];
            data_link = data_link.replace('[id]', selected_node);

            spinner.spin();
            overlay.appendChild(spinner.el);

            // Extract currently selected node and add it to data_link.

            ajaxGet(data_link, modal, undefined, event);

            addClass(modal, 'modal-show');

            removeAllListeners(overlay, 'click');
            addListener(overlay, 'click', removeModal, false)
        }

        function modalLoaded() {
            try {
                spinner.stop();
                overlay.removeChild(spinner.el);
            } catch (NotFoundError) {}
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

initializeNetwork();