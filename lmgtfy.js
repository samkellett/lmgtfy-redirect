var uris = {
  // Google:
  "lmgtfy.com": "google.com/search?q={query}",
  "images.lmgtfy.com": "google.com/search?tbm=isch&q={query}",
  "maps.lmgtfy.com": "google.com/maps/preview?q={query}",
  "video.lmgtfy.com": "google.com?tbm=vid&q={query}",
  "news.lmgtfy.com": "news.google.com/news/search?q={query}",
  "shopping.lmgtfy.com": "google.com?tbm=shop&q={query}",
  "photos.lmgtfy.com": "plus.google.com/u/0/s/{query}/photos",
  "plus.lmgtfy.com": "plus.google.com/s/{query}",
  "profiles.lmgtfy.com": "plus.google.com/s/{query}/people",
  "books.lmgtfy.com": "google.com/search?tbm=bks&q={query}",
  "finance.lmgtfy.com": "google.com/finance?q={query}",
  "scholar.lmgtfy.com": "scholar.google.com/scholar?q={query}",

  // Other languges:
  "en.lmgtfy.com": "google.com/search?q={query}",
  "ru.lmgtfy.com": "google.ru/search?q={query}",
  "de.lmgtfy.com": "google.de/search?q={query}",
  "pt-br.lmgtfy.com": "google.com.br/search?q={query}",
  "fr.lmgtfy.com": "google.fr/search?q={query}",
  "pl.lmgtfy.com": "google.pl/search?q={query}",
  "zh-tw.lmgtfy.com": "google.com.tw/search?q={query}",
  "nl.lmgtfy.com": "google.nl/search?q={query}",
  "es.lmgtfy.com": "google.es/search?q={query}",

  // Other sites:
  "bing.lmgtfy.com": "bing.com/search?q={query}",
  "lmbtfy.com": "bing.com/search?q={query}",
  "snopes.lmgtfy.com": "search.atomz.com/search/?sp-a=00062d45-sp00000000&sp-q={query}",
  "wikipedia.lmgtfy.com": "en.wikipedia.org/wiki/Special:Search?search={query}",
  "lmstfy.com": "twitter.com/search?q={query}",
  "lmddgtfy.net": "duckduckgo.com?q={query}",
  "lmsptfty.com": "startpage.com/do/search?query={query}"
};

chrome.webRequest.onBeforeRequest.addListener(function(info) {
    var from = new URI(info.url);
    if (from.directory().indexOf("/assets") == 0) {
      // Don't bother if this is not a main request...
      return;
    }

    console.log("Hello from lmgtfy Redirect.");
    console.log("Got request: " + info.url);

    if (from.subdomain() == "www") {
      // If www is there then remove it:
      from.subdomain("");
    }

    var key = from.hostname();
    if (key in uris) {
      var query = from.search(true);
      if (!("q" in query)) {
        // Nothing searched for (yet!)
        console.log("No query to redirect... exiting.");
        return {};
      }

      var to = URITemplate(from.scheme() + "://" + uris[key]).expand({ query: query["q"] });

      if (key == "scholar.lmgtfy.com") {
        // scholar.lmgtfy.com is a special case as their are two buttons that the user can push.
        //  Determining which was clicked is decided by the 'l' query parameter.
        if (query["l"] === "1") {
          to.addQuery("as_sdt", "2,47")
        }
      }

      console.log("Redirecting to " + to + "...");
      return { redirectUrl: to };

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
