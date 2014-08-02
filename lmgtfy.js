var uris = {
  // Google:
  "lmgtfy.com": "google.com/search?q=###",
  "images.lmgtfy.com": "google.com/search?tbm=isch&q=###",
  "maps.lmgtfy.com": "google.com/maps/preview?q=###",
  "video.lmgtfy.com": "google.com?tbm=vid&q=###",
  "news.lmgtfy.com": "news.google.com/news/search?q=###",
  "shopping.lmgtfy.com": "google.com?tbm=shop&q=###",
  "photos.lmgtfy.com": "plus.google.com/u/0/s/###/photos",
  "plus.lmgtfy.com": "plus.google.com/s/###",
  "profiles.lmgtfy.com": "plus.google.com/s/###/people",
  "books.lmgtfy.com": "google.com/search?tbm=bks&q=###",
  "finance.lmgtfy.com": "google.com/finance?q=###",
  "scholar.lmgtfy.com": "scholar.google.com/scholar?q=###",
  // NB: http://scholar.lmgtfy.com/?q=sam&l=1
  //  -> http://scholar.google.com/scholar?as_sdt=2%2C47&q=sam

  // Other languges:
  "en.lmgtfy.com": "google.com/search?q=###",
  "ru.lmgtfy.com": "google.ru/search?q=###",
  "de.lmgtfy.com": "google.de/search?q=###",
  "pt-br.lmgtfy.com": "google.com.br/search?q=###",
  "fr.lmgtfy.com": "google.fr/search?q=###",
  "pl.lmgtfy.com": "google.pl/search?q=###",
  "zh-tw.lmgtfy.com": "google.com.tw/search?q=###",
  "nl.lmgtfy.com": "google.nl/search?q=###",
  "es.lmgtfy.com": "google.es/search?q=###",

  // Other sites:
  "bing.lmgtfy.com": "bing.com/search?q=###",
  "lmbtfy.com": "bing.com/search?q=###",
  "snopes.lmgtfy.com": "search.atomz.com/search/?sp-a=00062d45-sp00000000&sp-q=###",
  "wikipedia.lmgtfy.com": "en.wikipedia.org/wiki/Special:Search?search=###",
  "lmstfy.com": "twitter.com/search?q=###",
  "lmddgtfy.com": "duckduckgo.com?q=###",
  "lmsptfty.com": "startpage.com/do/search?query=###"
};

chrome.webRequest.onBeforeRequest.addListener(function(info) {
    var uri = new URI(info.url);
    if (uri.directory().indexOf("/assets") == 0) {
      // Don't bother if this is not a main request...
      return;
    }

    console.log("Hello from lmgtfy Redirect.");
    console.log("Got request: " + info.url);

    if (uri.subdomain() == "www") {
      // If www is there then remove it:
      uri.subdomain("");
    }

    var key = uri.hostname();
    if (key in uris) {
      var query = uri.search(true);

      var uri = uri.scheme() + "://" + uris[key];
      uri = uri.replace("###", query["q"]);

      console.log("Redirecting to " + uri + "...");
      return { redirectUrl: uri };

    } else {
      console.log("Unknown host: " + key);
      return {};
    }
  },
  {
    urls: [
      "*://*.lmgtfy.com/*",
      "*://*.lmbtfy.com/*",
      "*://*.lmddgtfy.net/*",
      "*://*.lmsptfy.com/*",
      "*://*.lmstfy.com/*"
    ]
  },
  ["blocking"]
);
