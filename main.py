import scraper


if __name__ == "__main__":
    
    html = '''

    <!DOCTYPE html>

    <html>

    <title>Wave</title>

    <head>
        <link href="./style.css" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body>

        <div class="container">
            <div class="text">wave</div>
            <div class="box" id="upper"></div>
            <svg class="wave" id="wave" preserveAspectRatio="none" viewbox="0 0 1200 50">
                <path as id="wavepath"/>
            </svg>
            <div class="box"></div>
        </div>

        <script src="wave.js"></script>
        <script src="index.js"></script>
    </body>

    </html>

    '''

    tree = scraper.Scrape(html)
    tag = tree.getElementsByType("div")

    for i in tree.tree:
        print(i.type)
        print(i.attributes)
        print(i.text.rstrip())
        print(" ")
