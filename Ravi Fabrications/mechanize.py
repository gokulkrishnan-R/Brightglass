import mechanize

# Create a mechanize browser object
browser = mechanize.Browser()
# Send an HTTP request to the URL of the webpage with the form you want to scrape
browser.open("https://www.google.com/")
# Select the form to scrape
browser.select_form(nr=0)
# Extract the input fields and their corresponding values

for control in browser.form.controls:
    print(control.name, control.value)
    # Submit the form
    browser.submit()
    