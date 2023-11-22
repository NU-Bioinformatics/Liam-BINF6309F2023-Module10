#!/bin/usr/env python


# Exercise 1

# manually go to URL
# provides the following in JSON
"""
{
  "initialSampleSize" : "1,656 Han Chinese ancestry cases, 3,394 Han Chinese ancestry controls",
  "gxe" : false,
  "gxg" : false,
  "snpCount" : 2100739,
  "qualifier" : null,
  "imputed" : true,
  "pooled" : false,
  "studyDesignComment" : null,
  "accessionId" : "GCST001795",
  "fullPvalueSet" : false,
  "userRequested" : false,
  "platforms" : [ {
    "manufacturer" : "Illumina"
  } ],
  "ancestries" : [ {
    "type" : "initial",
    "numberOfIndividuals" : 5050,
    "ancestralGroups" : [ {
      "ancestralGroup" : "East Asian"
    } ],
    "countryOfOrigin" : [ ],
    "countryOfRecruitment" : [ {
      "majorArea" : "Asia",
      "region" : "Eastern Asia",
      "countryName" : "China"
    }, {
      "majorArea" : "Asia",
      "region" : "Eastern Asia",
      "countryName" : "China, Hong Kong SAR"
    } ]
  }, {
    "type" : "replication",
    "numberOfIndividuals" : 8923,
    "ancestralGroups" : [ {
      "ancestralGroup" : "East Asian"
    } ],
    "countryOfOrigin" : [ ],
    "countryOfRecruitment" : [ {
      "majorArea" : "Asia",
      "region" : "Eastern Asia",
      "countryName" : "China"
    } ]
  }, {
    "type" : "replication",
    "numberOfIndividuals" : 1416,
    "ancestralGroups" : [ {
      "ancestralGroup" : "South East Asian"
    } ],
    "countryOfOrigin" : [ ],
    "countryOfRecruitment" : [ {
      "majorArea" : "Asia",
      "region" : "South-eastern Asia",
      "countryName" : "Thailand"
    } ]
  } ],
  "diseaseTrait" : {
    "trait" : "Systemic lupus erythematosus"
  },
  "genotypingTechnologies" : [ {
    "genotypingTechnology" : "Genome-wide genotyping array"
  } ],
  "replicationSampleSize" : "3,256 Han Chinese ancestry cases, 5,667 Han Chinese ancestry controls, 453 Thai ancestry cases, 963 Thai ancestry controls",
  "publicationInfo" : {
    "pubmedId" : "23273568",
    "publicationDate" : "2012-12-27",
    "publication" : "Am J Hum Genet",
    "title" : "Meta-analysis followed by replication identifies loci in or near CDKN1B, TET3, CD80, DRAM1, and ARID5B as associated with systemic lupus erythematosus in Asians.",
    "author" : {
      "fullname" : "Yang W",
      "orcid" : null
    }
  },
  "_links" : {
    "self" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795"
    },
    "study" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795{?projection}",
      "templated" : true
    },
    "associationsByStudySummary" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795/associations?projection=associationByStudy"
    },
    "backgroundEfoTraits" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795/backgroundEfoTraits"
    },
    "associations" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795/associations"
    },
    "snps" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795/snps"
    },
    "efoTraits" : {
      "href" : "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795/efoTraits"
    }
  }
}
"""

# Exercise 2

# Import required packages
import requests  # HTTP library - manages data transfer from web resource (e.g. GWAS Catalog)
import json  # Handling the json response
import pandas as pd  # Data analysis library, a bit like R for Python!

# API Address:
apiUrl = 'https://www.ebi.ac.uk/gwas/rest/api'

# List of variants:
variants = ['rs142968358', 'rs62402518', 'rs12199222', 'rs7329174', 'rs9879858765']

# Store extracted data in this list:
extractedData = []

# Iterating over all variants:
for variant in variants:

    # Accessing data for a single variant:
    requestUrl = '%s/singleNucleotidePolymorphisms/%s/associations?projection=associationBySnp' % (apiUrl, variant)
    response = requests.get(requestUrl, headers={"Content-Type": "application/json"})

    # Testing if rsID exists:
    if not response.ok:
        print("[Warning] %s is not in the GWAS Catalog!!" % variant)
        continue

    # Test if the returned data looks good:
    try:
        decoded = response.json()
    except:
        print("[Warning] Failed to encode data for %s" % variant)
        continue

    for association in decoded['_embedded']['associations']:
        trait = ",".join([trait['trait'] for trait in association['efoTraits']])
        pvalue = association['pvalue']

        extractedData.append({'variant': variant,
                              'trait': trait,
                              'pvalue': pvalue})

# Format data into a table (data frame):
table = pd.DataFrame.from_dict(extractedData)
print(table)




# Exercise 3

# API Address:
apiUrl = 'https://www.ebi.ac.uk/gwas/summary-statistics/api'

trait = "EFO_0001360"
p_upper = "0.000000001"

requestUrl = '%s/traits/%s/associations?p_upper=%s&size=10' % (apiUrl, trait, p_upper)
response = requests.get(requestUrl, headers={"Content-Type": "application/json"})

# The returned response is a "response" object, from which we have to extract and parse the information:
decoded = response.json()
extractedData = []

for association in decoded['_embedded']['associations'].values():
    pvalue = association['p_value']
    variant = association['variant_id']
    studyID = association['study_accession']

    extractedData.append({'variant': variant,
                          'studyID': studyID,
                          'pvalue': pvalue})

ssTable = pd.DataFrame.from_dict(extractedData)
print(ssTable)

# Excercise 4

def getStudy(studyLink):
    # Accessing data for a single study:
    response = requests.get(studyLink, headers={"Content-Type": "application/json"})
    decoded = response.json()

    gwasData = requests.get(decoded['_links']['gwas_catalog']['href'], headers={"Content-Type": "application/json"})
    decodedGwasData = gwasData.json()

    traitName = decodedGwasData['diseaseTrait']['trait']
    pubmedId = decodedGwasData['publicationInfo']['pubmedId']

    return (traitName, pubmedId)


extractedData = []

for association in decoded['_embedded']['associations'].values():
    pvalue = association['p_value']
    variant = association['variant_id']
    studyID = association['study_accession']
    studyLink = association['_links']['study']['href']
    traitName, pubmedId = getStudy(studyLink)

    extractedData.append({'variant': variant,
                          'studyID': studyID,
                          'pvalue': pvalue,
                          'traitName': traitName,
                          'pubmedID': pubmedId})

ssWithGWASTable = pd.DataFrame.from_dict(extractedData)
print(ssWithGWASTable)
ssWithGWASTable.to_csv('GWAS_API_table.csv')



