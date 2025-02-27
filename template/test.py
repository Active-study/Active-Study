def convert_google_drive_link(shareable_link):
    """
    Converts a Google Drive shareable link into a direct download or embeddable link.
    """
    # Check if the input link contains 'drive.google.com'
    if "drive.google.com" not in shareable_link:
        return "Invalid Google Drive link."

    # Extract the file ID from the shareable link
    try:
        file_id = shareable_link.split("/d/")[1].split("/")[0]
    except IndexError:
        return "Unable to extract the file ID. Check the link format."

    # Create a direct download link and an embeddable link
    direct_download_link = f"https://drive.google.com/uc?id={file_id}&export=download"
    embeddable_link = f"https://drive.google.com/viewerng/viewer?embedded=true&url=https://drive.google.com/uc?id={file_id}"

    return {
        "Direct Download Link": direct_download_link,
        "Embeddable Link": embeddable_link
    }


# Example usage
if __name__ == "__main__":
    shareable_link = input("Enter the Google Drive shareable link: ")
    result = convert_google_drive_link(shareable_link)

    if isinstance(result, dict):
        print("\nConverted Links:")
        print("Direct Download Link: ", result["Direct Download Link"])
        print("Embeddable Link: ", result["Embeddable Link"])
    else:
        print(result)
