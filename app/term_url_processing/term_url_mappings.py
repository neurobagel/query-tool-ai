# URLs for fetching diagnosis and assessment mappings
diagnosis_url = "https://api.neurobagel.org/attributes/nb%3ADiagnosis"
assessment_url = "https://api.neurobagel.org/attributes/nb%3AAssessment"

# Hardcoded mappings for sex
sex_mapping = {
    "male": "snomed:248153007",
    "female": "snomed:248152002",
    "other": "snomed:32570681000036106",
}

# Hardcoded mappings for image modality
image_modality_mapping = [
    {
        "label": "Arterial Spin Labeling",
        "termURL": "nidm:ArterialSpinLabeling",
    },
    {
        "label": "Diffusion Weighted",
        "termURL": "nidm:DiffusionWeighted",
    },
    {
        "label": "Electroencephalogram",
        "termURL": "nidm:EEG",
    },
    {
        "label": "Flow Weighted",
        "termURL": "nidm:FlowWeighted",
    },
    {
        "label": "T1 Weighted",
        "termURL": "nidm:T1Weighted",
    },
    {
        "label": "T2 Weighted",
        "termURL": "nidm:T2Weighted",
    },
]
