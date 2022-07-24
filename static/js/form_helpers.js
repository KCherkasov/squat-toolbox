"use strict";

function switch_tab(sender_id) {
    var tag = "#" + document.querySelector("#" + sender_id).value + "-tab"
    var tab = document.querySelector(tab)
    bootstrap.Tab.getOrCreateInstance(tab).show()
}

function switch_hw() {
    switch_tab('hw-select')
}

function switch_role() {
    switch_tab('role-select')
}

function switch_bg() {
    switch_tab('bg-select')
}