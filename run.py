from jinja2 import Template

vars = {
    "milos": "kozak",
    "name": "neco",    
    "nested": {
        "test": "ko",
        "nested": {
            "test": "ko"
        }
    }
}

vars2 = {
    "name": "neco2",    
    "nested": {
        "test": "OK"
    }
}


template = Template('Hello {{ nested|tojson }}! - {{ context }}')
print(template.render(**{**vars, **vars2}))