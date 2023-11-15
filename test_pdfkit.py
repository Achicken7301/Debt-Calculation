import pdfkit


config = pdfkit.configuration(wkhtmltopdf="./wkhtmltox/bin/wkhtmltopdf.exe")

# Convert from a URL
pdfkit.from_url("https://google.com", "google.pdf", configuration=config)

# Convert from a file
pdfkit.from_file("test.html", "test.pdf", configuration=config)

# Convert from a string
pdfkit.from_string("<h1>Hello</h1>", "hello.pdf",configuration=config)
