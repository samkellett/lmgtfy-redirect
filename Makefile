NAME=lmgtfy-redirect
ICONS=chrome/icons/icon128.png chrome/icons/icon48.png chrome/icons/icon16.png
FILES=chrome/manifest.json chrome/lmgtfy.js chrome/uri/src/URI.min.js $(ICONS)

all: package

clean:
	rm $(NAME).zip

package: chrome/* 
	touch $(NAME).zip
	zip -ru $(NAME) chrome/
