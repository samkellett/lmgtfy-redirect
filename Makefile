
all: package

package: manifest.json lmgtfy.js uri/src/URI.min.js
	zip -u lmgtfy.zip manifest.json lmgtfy.js uri/src/URI.min.js
