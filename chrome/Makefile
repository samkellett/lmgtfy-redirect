NAME=lmgtfy-redirect
ICONS=icons/icon128.png icons/icon48.png icons/icon16.png
FILES=manifest.json lmgtfy.js uri/src/URI.min.js $(ICONS)

all: clean package

clean:
	rm $(NAME).zip

package: $(FILES)
	zip $(NAME).zip $(FILES)

