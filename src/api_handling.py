import logging, re
from src.constant import *
from src import settings
import google.cloud.dlp
from google.cloud import vision_v1
from google.cloud.dlp_v2 import InspectContentResponse


def extract_entity_google(contentdata, min_likelihood = "LIKELY"):
    """Inspects and extracts the info types
    Args:
        project: The Google Cloud project id to use as a parent resource.
        contentdata: The object to inspect (will be contain the text).
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
    Returns:
        None; the response from the API is printed to the terminal.

    Parameters
    ----------
    contentdata
    min_likelihood: https://cloud.google.com/dlp/docs/likelihood
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{settings.GOOGLE_PROJECT_ID}"

    # Construct inspect configuration dictionary
    inspect_config = {
        "info_types": [{"name": info_type} for info_type in response_parameters.values()],
        "min_likelihood": min_likelihood,
        "include_quote": True,
    }

    # Call the API
    logging.info("Calling Google DLP API")
    response = None
    try:
        response = dlp.inspect_content(
            request={
                "parent": parent,
                "inspect_config": inspect_config,
                "item": {"value": contentdata},
            }
        )
    except Exception as e:
        logging.info("Calling Google DLP API Exception:{}".format(str(e)))   
    extracted_list = {"status":"No Findings Matched."}
    if response:
        logging.info("Formating details of response recieved from Google DLP API")
        extracted_list = {key: format_result(response, (val,)) for key, val in response_parameters.items()}
        extracted_list["status"] = "Findings Matched."
    return extracted_list


def format_result(response: InspectContentResponse, type_: tuple) -> list:
    return [finding.quote.replace('\n',"") for finding in response.result.findings if finding.info_type.name in type_]

def extract_image(raw_content):
    client = vision_v1.ImageAnnotatorClient()
    image = vision_v1.Image(content=raw_content)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text
    

def clean_content(raw_content):
    raw_content = raw_content.encode("utf-8", "ignore").decode("utf-8", "replace").strip()
    raw_content = re.compile(r"[<>]").sub(" ", raw_content)
    raw_content = re.compile(r"\s{2,}").sub(" ", raw_content).strip()
    return raw_content