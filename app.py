import streamlit.components.v1 as components
import streamlit as st
from bs4 import BeautifulSoup
import requests
import io

## ............................................... ##
# Set page configuration (Call this once and make changes as needed)
st.set_page_config(page_title='HTML-Content-Extractor',  layout='wide', page_icon=':spiral_note_pad:')

## ............................................... ##
# Instructions and information
st.sidebar.subheader("How to Use?")
st.sidebar.info("1. Enter the URL you want to extract HTML content from.")
st.sidebar.info("2. Click the 'Fetch and Process HTML' button.")
st.sidebar.info("3. The HTML content will be displayed.")
st.sidebar.info("4. Click the 'Download HTML' button to save the HTML file.")

## ............................................... ##
# Footer
st.sidebar.markdown("© 2023 Bayhaqy")

## ............................................... ##
# Streamlit app title and description
with st.container():
  # Define Streamlit app title and introduction
  st.title("HTML Content Extractor")
  st.write("Tools to extract HTML content from the Google web cache.")

## ............................................... ##
# Input field for the URL
url = st.text_input("Enter the URL:")

## ............................................... ##
# Function to remove script tag and text before <html>
def remove_script_and_before_html(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find and remove the script tag
    script_tag = soup.find("script", text="window.main();")
    if script_tag:
        script_tag.extract()

    # Get the modified HTML content
    html_content = str(soup)

    # Find the position of the <html> tag
    html_start = html_content.find("<html")

    if html_start != -1:
        # Extract everything starting from the <html> tag
        html_content = html_content[html_start:]
        return html_content
    else:
        return "No <html> tag found in the HTML content."
    return html_content

## ............................................... ##
# Button to fetch and process the content
if st.button("Fetch and Process HTML"):
    if url:
        base_url = 'https://webcache.googleusercontent.com/search?q=cache:'
        full_url = base_url + url + '&strip=0&vwsrc=0'

        st.write(full_url)

        # Send an HTTP GET request to the URL
        response = requests.get(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            html_content = response.text
            modified_html_content = remove_script_and_before_html(html_content)

            # Save the HTML content to a file
            with st.expander("Show Medium Content"):
                components.html(modified_html_content, width=1280, height=700, scrolling=True)

            # Button to download the HTML file
            download_button = st.download_button(
                label="Download HTML",
                data=modified_html_content,
                key="download_html_button",
                file_name="web_cache.html",
            )

        else:
            st.error(f"Failed to retrieve the web page. Status code: {response.status_code}")
    else:
        st.warning("Please enter a URL.")
