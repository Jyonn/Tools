function template(strings, ...keys) {
    return (function (...values) {
        const dict = values[values.length - 1] || {};
        const result = [strings[0]];
        keys.forEach(function (key, i) {
            const value = Number.isInteger(key) ? values[key] : dict[key];
            result.push(value, strings[i + 1]);
        });
        return result.join('');
    });
}

function stringToHtml(s) {
    let tmp = document.createElement('div');
    tmp.innerHTML = s;
    return tmp.firstElementChild;
}

let active = 'active';
let inactive = 'inactive';

function activate(ele) {
    ele.classList.add(active);
    ele.classList.remove(inactive);
}

function deactivate(ele) {
    ele.classList.add(inactive);
    ele.classList.remove(active);
}

function toggle(ele) {
    if (ele.classList.contains('active')) {
        deactivate(ele);
    } else {
        activate(ele);
    }
}

function getQueryParam(key) {
    let params = new URLSearchParams(window.location.search);
    if (params.has(key))
        return params.get(key);
}

function getByClass(className) {
    return document.getElementsByClassName(className)[0];
}

function getById(id) {
    return document.getElementById(id);
}

function listToMatrix(list, elementsPerSubArray) {
    let matrix = [], i, k;

    for (i = 0, k = -1; i < list.length; i++) {
        if (i % elementsPerSubArray === 0) {
            k++;
            matrix[k] = [];
        }

        matrix[k].push(list[i]);
    }

    return matrix;
}