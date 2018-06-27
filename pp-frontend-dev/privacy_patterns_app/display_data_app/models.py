from django.db import models
from multiselectfield import MultiSelectField
from django import forms

# from easy_select2 import select2_modelform

SUBPRINCIPLE_CHOICES = (
    ("1", "1"), #values, labels 
    ("1.1.0", "1.1.0, Privacy Policy"), 
    ("1.1.1", "1.1.1, Communication to Internal Personnel"), 
    ("1.1.2", "1.1.2, Responsibility and Accountability for Policies"), 
    ("1.2.1",  "1.2.1, Review and Approval"), 
    ("1.2.2",  "1.2.2, Consistency of Privacy Policies and Procedures With Laws and Regulations"), 
    ("1.2.3",   "1.2.3, PI/PII Identification and Classification"), 
    ("1.2.4",  "1.2.4, Risk Assessment"), 
    ("1.2.5", "1.2.5, Consistency of Commitments With Privacy Policies and Procedures"), 
    ("1.2.6", "1.2.6, Infrastructure and Systems Management"), 
)

DATA_USAGE = (
    ("Collection", "Collection"),
    ("Access" , "Access"), 
    ("Use" , "Use"),
    ("Disclosure" , "Disclosure"),
)

# 1.2.7   Privacy Incident and Breach Management
# 1.2.8   Supporting Resources
# 1.2.9   Qualifications of Internal Personnel
# 1.2.10  Privacy Awareness and Training
# 1.2.11  Changes in Regulatory and Business Requirements
# 2   N/A
# 2.1.0   Privacy Policy
# 2.1.1   Communication to Individuals
# 2.2.1   Provision of Notice
# 2.2.2   Entities and Activities Covered
# 2.2.3   Clear and Conspicuous
# 3   N/A
# 3.1.0   Privacy Policy
# 3.1.1   Communication to Individuals
# 3.1.2   Consequences of Denying or Withdrawing Consent
# 3.2.1   Implicit or Explicit Consent
# 3.2.2   Consent for New Purposes and Uses
# 3.2.3   Explicit Consent for Sensitive Information
# 3.2.4   Consent for Online Data Transfers to or from an Individual's Computer or Other Similar Electronic Devices
# 4   N/A
# 4.1.0   Privacy Policies
# 4.1.1   Communication to Individuals
# 4.1.2   Types of PI/PII Collected and Methods of Collection
# 4.2.1   Collection Limited to Identified Purpose
# 4.2.2   Collection by Fair and Lawful Means
# 4.2.3   Collection from Third Parties
# 4.2.4   Information Developed about Individuals
# 5   N/A
# 5.1.0   Privacy Policies
# 5.1.1   Communication to Individuals
# 5.2.1   Use of PI/PII
# 5.2.2   Retention of PI/PII
# 5.2.3   Disposal, Destruction and Redaction of PI/PII
# 6   N/A
# 6.1.0   Privacy Policies
# 6.1.1   Communication to Individuals
# 6.2.1   Access by Individuals to Their PI/PII
# 6.2.2   Confirmation of an Individual's Identity
# 6.2.3   Understandable PI/PII, Time Frame and Cost
# 6.2.4   Denial of Access
# 6.2.5   Updating or Correcting PI/PII
# 6.2.6   Statement of Disagreement
# 7   N/A
# 7.1.0   Privacy Policies
# 7.1.1   Communication to Individuals
# 7.1.2   Communication to Third Parties
# 7.2.1   Disclosure of PI/PII
# 7.2.2   Protection of PI/PII
# 7.2.3   New Purposes and Uses
# 7.2.4   Misuse of PI/PII by a Third Party
# 8   N/A
# 8.1.0   Privacy Policies
# 8.1.1   Communication to Individuals
# 8.2.1   Information Security Program
# 8.2.2   Logical Access Controls
# 8.2.3   Physical Access Controls
# 8.2.4   Environmental Safeguards
# 8.2.5   Transmitted PI/PII
# 8.2.6   PI/PII on Portable Media
# 8.2.7   Testing Security Safeguards
# 9   N/A
# 9.1.0   Privacy Policies
# 9.1.1   Communication to Individuals
# 9.2.1   Accuracy and Completeness of PI/PII 
# 9.2.2,   Relevance of PI/PII
# 10, 
# 10.1.0  Privacy Policies
# 10.1.1  Communication to Individuals
# 10.2.1  Inquiry, Complaint and Dispute Process
# 10.2.2  Dispute Resolution and Recourse
# 10.2.3  Compliance Review
# 10.2.4  Instances of Noncompliance 
# 10.2.5  Ongoing Monitoring

#tracks ftc case data and links to privacy principles

class Recommendation(models.Model): 
    text = models.TextField(default='', null=True, blank=True)
    principle_id = models.TextField(default='', null=True, blank=True)
    priority_number = models.IntegerField(default=0)
    note = models.TextField(default='')
    subprinciple = models.TextField(default='')
    ref = models.TextField(default='')
    url = models.TextField(default='')
    def __str__(self): 
        return self.ref + " (" + self.principle_id + ")" + ' - ' + self.subprinciple

class DataEntry(models.Model): 
    case_name = models.TextField(default='')
    case_url = models.TextField(default='')
    last_updated = models.TextField(default='')
    tags = models.TextField(default='')
    specific_violation = models.TextField(default='')
    company_type_key = models.TextField(default='')
    location = models.TextField(default='')

    #privacy 
    subprinciples = models.TextField(default='')  
    positive_recommendations = models.ManyToManyField(Recommendation, blank=True, symmetrical=False)

    # data_usage = models.TextField(default='')
    data_usage = MultiSelectField(max_length=100,choices=DATA_USAGE, null=True, blank=True,help_text="<div style='float:right;font-size:12px;color:red'> HELP TEXT DISPLAYED HERE</div>")
    # jurisdiction = models.TextField(default='')

#tracks user preferences   
class UserModel(models.Model): 
    data_usage = models.TextField(default='')
    location = models.TextField(default='')
    industries = models.TextField(default='')

