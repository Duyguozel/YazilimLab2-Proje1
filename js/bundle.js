(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
    const Frequence = require('frequence');
     
    let freq = Frequence.words('I hear the drums echoing tonight\r\nBut she hears only whispers of some quiet conversation\r\nShes coming in 12:30 flight\r\nThe moonlit wings reflect the stars that guide me towards salvation\r\nI stopped an old man along the way\r\nHoping to find some long forgotten words or ancient melodies\n\nHe turned to me as if to say , \"Hurry boy, its waiting there for you\"\n\n\n\nIts gonna take a lot to drag me away from you\n\nTheres nothing that a hundred men or more could ever do\n\nI bless the rains down in Africa\n\nGonna take some time to do the things we never had\n\n\n\nThe wild dogs cry out in the night\n\nAs they grow restless longing for some solitary company\n\nI know that I must do whats right\n\nAs sure as Kilimanjaro rises like Olympus above the Serangetti\n\nI seek to cure whats deep inside, frightened of this thing that Ive become\n\n\n\nIts gonna take a lot to drag me away from you\n\nTheres nothing that a hundred men or more could ever do\n\nI bless the rains down in Africa\n\nGonna take some time to do the things we never had\n\n\n\nHurry boy, shes waiting there for you\n\n\n\nIts gonna take a lot to drag me away from you\n\nTheres nothing that a hundred men or more could ever do\n\nI bless the rains down in Africa\n\nI bless the rains down in Africa\n\nI bless the rains down in Africa\n\nI bless the rains down in Africa\n\nI bless the rains down in Africa\n\nI bless the rains down in Africa\n\nGonna take some time to do the things we never had');
    console.log(freq);
    },{"frequence":2}],2:[function(require,module,exports){
    'use strict';
    
    function Frequence(data, options) {
        options = options || {};
    
        let caseSensitive = options.caseSensitive || false;
        let keepSpecialChars = options.keepSpecialChars || false;
        let type = options.type || 'word';  //letter|word
    
        let buckets = [];
        let dictionary = [];
    
        if (data) {
            if (Array.isArray(data)) {
                data = data.join(' ');
            }
            if (!keepSpecialChars) {
                data = data.replace(/[^0-9a-zA-Z ]/g, '');
            }
            if (!caseSensitive) {
                data = data.toLowerCase();
            }
            switch (type) {
                case 'word':
                    data = data.replace(/\s+/g, ' ');
                    buckets = data.split(' ');
                    break;
                case 'letter':
                    data = data.replace(/\s+/g, '');
                    buckets = data.split('');
                    break;
            }
            let dictMap = {};
            buckets.forEach((token) => {
                dictMap[token] = dictMap[token] || 0;
                dictMap[token]++;
            });
            Object.keys(dictMap).sort().forEach((key) => {
                dictionary.push({
                    key,
                    count: dictMap[key]
                })
            });
        }
        return dictionary;
    }
    
    function words(data, options) {
        options = options || {};
        options.type = 'word';
        return Frequence(data, options);
    }
    
    function letters(data, options) {
        options = options || {};
        options.type = 'letter';
        return Frequence(data, options);
    }
    
    module.exports = Frequence;
    module.exports.words = words;
    module.exports.letters = letters;
    
    },{}]},{},[1]);