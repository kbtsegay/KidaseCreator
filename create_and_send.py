import os
import base64
import json
import yagmail
import datetime
from src.kidase_creator import KidaseCreator

def decode_credentials(encoded):
    # Decode the base64 string
    decoded = base64.b64decode(encoded)
    # Write the decoded content to credentials.json
    with open('./credentials.json', 'wb') as file:
        file.write(decoded)

def send_email(sender_email, recipient_email, attachment_path):
    # Initialize yagmail with OAuth2 credentials
    yag = yagmail.SMTP(sender_email, oauth2_file='./credentials.json')
    
    # Create the email content
    subject = 'Your Kidase Slide Deck'
    body = f"Please find your Kidase PowerPoint presentation for {datetime.datetime.now().strftime('%B %d, %Y')} attached."
    
    # Send the email with the attachment
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=body,
        attachments=attachment_path
    )

# Example usage
if __name__ == '__main__':
    encoded = os.environ['GOOGLE_CREDENTIALS']
    print('Decoding credentials...')
    decode_credentials(encoded)

    sender_email = os.environ['EMAIL_ADDRESS']
    responses = json.loads(os.environ['FORM_RESPONSES'])
    recipient_email = responses[1]
    lang_form_mapping = {
        'ግዕዝ': 'ግእዝ',
        'Ge\'ez (Transliterated)': 'ge\'ez',
        'አማርኛ': 'አማርኛ',
        'Amharic (Transliterated)': 'amharic',
        'ትግርኛ': 'ትግርኛ',
        'Tigrinya (Transliterated)': 'tigrinya',
        'English': 'english'
    }
    languages = [lang_form_mapping[lang] for lang in responses[2:6] if lang != '']

    print('Creating the Kidase presentation...')
    kidase_creator = KidaseCreator('./data', languages)
    prs = kidase_creator.create_presentation()
    prs.save('test.pptx')
    
    print('Sending the email...')
    
    send_email(sender_email, recipient_email, 'test.pptx')
