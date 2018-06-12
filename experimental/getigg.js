"use strict";
var system = require('system');
var fs = require('fs');
var CookieJar = "igg_cookie.json";
var pageResponses = {};

var page = require('webpage').create();
page.settings.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"


// cookie shit, not sure it does anything
page.onResourceReceived = function(response) {
    pageResponses[response.url] = response.status;
    fs.write(CookieJar, JSON.stringify(phantom.cookies), "w");
};
if(fs.isFile(CookieJar))
    Array.prototype.forEach.call(JSON.parse(fs.read(CookieJar)), function(x){
        phantom.addCookie(x);
    });

// actual code
page.open("http://igg-games.com/?s=" + system.args[1] + "&=submit", function(status) {
    waitFor({
        interval: 100,
        timeout: 45000,
        check: function () {
            return page.evaluate(function() {
                var titleFound = document.querySelector("#primary-content h1.title span.alt") ? true : false;

                if(document.querySelector('h1.title'))
                    var noFound = document.querySelector('h1.title').textContent == "Nothing found :(";
                else
                    var noFound = false;

                return noFound || titleFound;
            });
        },
        success: function () {
            console.log(page.content);
            phantom.exit();
        },
        error: function () {
            console.log("failure");
            phantom.exit();
        }
    });
});



function waitFor ($config) {
    $config._start = $config._start || new Date();

    if ($config.timeout && new Date - $config._start > $config.timeout) {
        if ($config.error) $config.error();
        if ($config.debug) console.log('timedout ' + (new Date - $config._start) + 'ms');
        phantom.exit();
    }

    if ($config.check()) {
        if ($config.debug) console.log('success ' + (new Date - $config._start) + 'ms');
        return $config.success();
    }

    setTimeout(waitFor, $config.interval || 0, $config);
}

