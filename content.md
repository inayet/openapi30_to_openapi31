## Table of Contents
- [script.log](#script.log)
- [dir_structure](#dir_structure)
- [display_content_readme.py](#display_content_readme.py)
- [requirements.txt](#requirements.txt)
- [__init__.py](#__init__.py)
- [openapi_converter_main.py](#openapi_converter_main.py)
- [content.md](#content.md)
- [openapi_converter.py](#openapi_converter.py)
- [README.md](#README.md)
- [calendars.json](#calendars.json)
- [License](#License)

###BEGIN_AUTO_GENERATED###

### script.log
2023-08-16 11:05:19,178 - INFO - Directory already has a git repo


### dir_structure
.
├── calendars.json
├── content.md
├── dir_structure
├── display_content_readme.py
├── __init__.py
├── License
├── openapi_converter_main.py
├── openapi_converter.py
├── __pycache__
│   └── openapi_converter.cpython-311.pyc
├── README.md
├── requirements.txt
├── script.log
├── useful.git-commands
├── useful.git-create-new-repo.py
└── useful.git-create-new-repo.sh

2 directories, 15 files


### display_content_readme.py
import os
import re
import asyncio
import aiofiles
import logging

logging.basicConfig(level=logging.INFO)

DEFAULT_IGNORE_PATTERNS = [r"\./__pycache__", r".*\.git.*", r".*\.env.*"]

CONCURRENT_TASKS_LIMIT = 4  # Adjust this based on your system's capacity and drive type
sem = asyncio.Semaphore(CONCURRENT_TASKS_LIMIT)

def compile_patterns(patterns):
    return [re.compile(pattern) for pattern in patterns]

async def should_ignore(item, compiled_patterns):
    for pattern in compiled_patterns:
        if pattern.search(item):
            logging.info(f"Ignoring item due to pattern {pattern.pattern}: {item}")
            return True
    logging.info(f"Item not ignored: {item}")
    return False

async def generate_md_files(directory, ignore_patterns):
    logging.info(f"Processing directory: {directory}")
    async with sem:
        content_filepath = os.path.join(directory, "content.md")
        readme_filepath = os.path.join(directory, "README.md")

        user_content = ""
        if os.path.exists(readme_filepath):
            async with aiofiles.open(readme_filepath, 'r') as f:
                content = await f.read()
            user_content_match = re.search('###BEGIN_USER_GENERATED###.*###END_USER_GENERATED###', content, re.DOTALL)
            if user_content_match:
                user_content = user_content_match.group(0)

        toc_content = "## Table of Contents\n"
        file_content_list = []
        toc_set = set()  # Used to ensure no duplication in TOC

        for entry in os.scandir(directory):
            if entry.is_file() and not await should_ignore(entry.path, ignore_patterns):
                if entry.name not in toc_set:
                    toc_content += f"- [{entry.name}](#{entry.name})\n"
                    toc_set.add(entry.name)
                try:
                    async with aiofiles.open(entry.path, 'r', encoding='utf-8') as f:
                        file_content = await f.read()
                        if entry.name not in ["content.md", "README.md"] and file_content not in toc_content:
                            file_content_list.append(f"\n### {entry.name}\n{file_content}\n")
                except UnicodeDecodeError:
                    file_content_list.append(f"\n### {entry.name}\n**[ERROR reading {entry.name} as text. Might be a binary file or use a different encoding.]**\n")

        new_content = toc_content + "\n###BEGIN_AUTO_GENERATED###\n" + ''.join(file_content_list) + "###END_AUTO_GENERATED###\n"

        async with aiofiles.open(content_filepath, 'w') as f:
            await f.write(new_content)

        if os.path.exists(readme_filepath):
            async with aiofiles.open(readme_filepath, 'r') as f:
                existing_content = await f.read()
            content_start = existing_content.find("###BEGIN_AUTO_GENERATED###")
            content_end = existing_content.find("###END_AUTO_GENERATED###")
            if content_start != -1 and content_end != -1:
                existing_content = existing_content[:content_start] + new_content + existing_content[content_end + len("###END_AUTO_GENERATED###"):]
                new_content = existing_content

        async with aiofiles.open(readme_filepath, 'w') as f:
            await f.write(new_content)
            await f.write("\n" + user_content)

async def process_directory(directory):
    logging.info(f"Checking directory: {directory}")

    ignore_file_path = os.path.join(directory, "display_project_files.ignore")
    if os.path.exists(ignore_file_path):
        async with aiofiles.open(ignore_file_path, 'r') as f:
            ignore_patterns = compile_patterns([line.strip() for line in await f.readlines()])
        logging.info(f"Loaded ignore patterns for {directory}: {ignore_patterns}")
    else:
        ignore_patterns = compile_patterns(DEFAULT_IGNORE_PATTERNS)

    await generate_md_files(directory, ignore_patterns)

    for entry in os.scandir(directory):
        logging.info(f"Checking item against ignore patterns: {entry.path}")
        if entry.is_dir():
            await process_directory(entry.path)

if __name__ == "__main__":
    asyncio.run(process_directory("."))


### requirements.txt
aiofiles==23.2.1
annotated-types==0.5.0
anyio==3.7.1
click==8.1.6
fastapi==0.101.1
gh==0.0.4
gitdb==4.0.10
GitPython==3.1.32
h11==0.14.0
idna==3.4
pydantic==2.1.1
pydantic_core==2.4.0
python-logstash==0.4.8
PyYAML==6.0.1
smmap==5.0.0
sniffio==1.3.0
starlette==0.27.0
typing_extensions==4.7.1
uvicorn==0.23.2


### openapi_converter_main.py
# Filename is openapi_converter_main.py
# This file contains the main function to convert an OpenAPI 3.0 spec to 3.1

import argparse
import openapi_converter as converter 
import yaml
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file', nargs='?', default=None)
    args = parser.parse_args()

    if args.output_file is None:
        base_name = os.path.splitext(args.input_file)[0]  # Get the name without extension
        args.output_file = os.path.join(os.getcwd(), f"{base_name}.yml")

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' does not exist.")

    with open(args.input_file, 'r') as f:
        openapi_dict = yaml.safe_load(f)

    try:
        converted_spec = converter.convert_openapi(openapi_dict)
        with open(args.output_file, 'w') as f:
            f.write(converted_spec)
        print(f"Converted spec saved to {args.output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


    with open(args.output_file, 'w') as f:
        f.write(converted_spec)

    print(f"Converted spec saved to {args.output_file}")


### openapi_converter.py
# Filename openapi_converter.py
# This module contains functions to convert an OpenAPI 3.0 spec to 3.1

import yaml
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.INFO)

def convert_openapi(openapi_dict):
    # Input validation

    validate_required_fields(openapi_dict)
    validate_openapi_version(openapi_dict, versions=["3.0.0", "3.1.0"])
    check_incompatible_inputs(openapi_dict, incompatible_keys=["securityDefinitions"])

    # Retain operation details

    for path in openapi_dict['paths'].values():
        for operation in path.values():
            if 'description' in operation:
                operation['x-original-description'] = operation['description']
            if 'operationId' in operation:
                operation['x-original-operationId'] = operation['operationId']

    # Retain schema details

    for schema in openapi_dict['components']['schemas'].values():
        if 'description' in schema:
            schema['x-original-description'] = schema['description']

    # Update to OpenAPI version 3.1.0

    openapi_dict['openapi'] = "3.1.0"

    # Security schemes

    security_schemes = {}

    if 'securityDefinitions' in openapi_dict:
        logging.warning(
            f"'securityDefinitions' found - converting to 'securitySchemes'. "
            "This key is deprecated in OpenAPI 3.1.0 and should be replaced with 'securitySchemes'."
        )
        security_definitions = openapi_dict.pop('securityDefinitions')
        for def_name, definition in security_definitions.items():
            scheme = {
                'type': definition.get('type', 'http'),
                'scheme': definition.get('scheme', 'bearer')
            }
            if 'bearerFormat' in definition:
                scheme['bearerFormat'] = definition['bearerFormat']
            if 'description' in definition:
                scheme['description'] = definition['description']
            security_schemes[def_name] = scheme

    openapi_dict['components']['securitySchemes'] = security_schemes

    # YAML conversion

    yaml_string = yaml.dump(openapi_dict, sort_keys=True)

    return yaml_string

# Input validation functions

def validate_required_fields(openapi_dict):
    required_fields = ['openapi', 'info', 'paths']
    for field in required_fields:
        if field not in openapi_dict:
            raise Exception(f"Field '{field}' is required")

def validate_openapi_version(openapi_dict, versions=["3.0.0", "3.1.0"]):
    if openapi_dict['openapi'] not in versions:
        raise Exception(
            f"Input version must be one of {versions}. Found {openapi_dict['openapi']}"
        )

def check_incompatible_inputs(openapi_dict, incompatible_keys=['securityDefinitions']):
    for key in incompatible_keys:
        if key in openapi_dict:
            raise Exception(f"Input contains deprecated key '{key}'.")


### calendars.json
{
    "openapi": "3.0.0",
    "info": {
        "title": "Calendars API",
        "description": "Documentation for Calendars API",
        "version": "1.0",
        "contact": {}
    },
    "tags": [
        {
            "name": "Calendars",
            "description": "Documentation for Calendars API"
        }
    ],
    "servers": [
        {
            "url": "https://services.leadconnectorhq.com"
        }
    ],
    "components": {
        "securitySchemes": {
            "bearer": {
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "type": "http"
            }
        },
        "schemas": {
            "BadRequestDTO": {
                "type": "object",
                "properties": {
                    "statusCode": {
                        "type": "number",
                        "example": 400
                    },
                    "message": {
                        "type": "string",
                        "example": "Bad Request"
                    }
                }
            },
            "UnauthorizedDTO": {
                "type": "object",
                "properties": {
                    "statusCode": {
                        "type": "number",
                        "example": 401
                    },
                    "message": {
                        "type": "string",
                        "example": "Invalid token: access token is invalid"
                    },
                    "error": {
                        "type": "string",
                        "example": "Unauthorized"
                    }
                }
            },
            "SlotsSchema": {
                "type": "object",
                "properties": {
                    "slots": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "slots"
                ]
            },
            "GetSlotsSuccessfulResponseDto": {
                "type": "object",
                "properties": {
                    "_dates_": {
                        "$ref": "#/components/schemas/SlotsSchema"
                    }
                },
                "required": [
                    "_dates_"
                ]
            },
            "CalendarSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "example": "0TkCdp9PfvLeWKYRRvIz"
                    },
                    "locationId": {
                        "type": "string",
                        "example": "ocQHyuzHvysMo5N5VsXc"
                    },
                    "groupId": {
                        "type": "string",
                        "description": "Group Id",
                        "example": "BqTwX8QFwXzpegMve9EQ"
                    },
                    "name": {
                        "type": "string",
                        "example": "test calendar"
                    },
                    "description": {
                        "type": "string",
                        "example": "this is used for testing"
                    },
                    "slug": {
                        "type": "string",
                        "example": "test1"
                    },
                    "isActive": {
                        "type": "boolean",
                        "example": true
                    },
                    "openHours": {
                        "example": [],
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "id",
                    "locationId",
                    "name"
                ]
            },
            "CalendarsGetSuccessfulResponseDto": {
                "type": "object",
                "properties": {
                    "calendars": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/CalendarSchema"
                        }
                    }
                }
            },
            "CalendarNotification": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "shouldSendToContact": {
                        "type": "object"
                    },
                    "shouldSendToUser": {
                        "type": "object"
                    },
                    "shouldSendToSelectedUsers": {
                        "type": "object"
                    },
                    "selectedUsers": {
                        "type": "string"
                    },
                    "templateId": {
                        "type": "string"
                    }
                },
                "required": [
                    "type",
                    "shouldSendToContact",
                    "shouldSendToUser",
                    "shouldSendToSelectedUsers",
                    "selectedUsers",
                    "templateId"
                ]
            },
            "TeamMemeber": {
                "type": "object",
                "properties": {
                    "userId": {
                        "type": "string",
                        "example": "ocQHyuzHvysMo5N5VsXc"
                    },
                    "priority": {
                        "type": "number",
                        "default": 0.5,
                        "enum": [
                            0,
                            0.5,
                            1
                        ]
                    },
                    "meetingLocation": {
                        "type": "string"
                    }
                },
                "required": [
                    "userId"
                ]
            },
            "Hour": {
                "type": "object",
                "properties": {
                    "openHour": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 23
                    },
                    "openMinute": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 60
                    },
                    "closeHour": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 23
                    },
                    "closeMinute": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 60
                    }
                },
                "required": [
                    "openHour",
                    "openMinute",
                    "closeHour",
                    "closeMinute"
                ]
            },
            "OpenHour": {
                "type": "object",
                "properties": {
                    "daysOfTheWeek": {
                        "type": "array",
                        "items": {
                            "type": "number",
                            "maximum": 6,
                            "minimum": 0
                        }
                    },
                    "hours": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Hour"
                        }
                    }
                },
                "required": [
                    "daysOfTheWeek",
                    "hours"
                ]
            },
            "CalendarCreateSchema": {
                "type": "object",
                "properties": {
                    "notifications": {
                        "description": "Calendar Notifications",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/CalendarNotification"
                        }
                    },
                    "locationId": {
                        "type": "string",
                        "example": "ocQHyuzHvysMo5N5VsXc"
                    },
                    "groupId": {
                        "type": "string",
                        "description": "Group Id",
                        "example": "BqTwX8QFwXzpegMve9EQ"
                    },
                    "teamMembers": {
                        "description": "Team members",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/TeamMemeber"
                        }
                    },
                    "eventType": {
                        "type": "string",
                        "enum": [
                            "RoundRobin_OptimizeForAvailability",
                            "RoundRobin_OptimizeForEqualDistribution",
                            "Collective",
                            "Group"
                        ],
                        "default": "RoundRobin_OptimizeForAvailability"
                    },
                    "name": {
                        "type": "string",
                        "example": "test calendar"
                    },
                    "description": {
                        "type": "string",
                        "example": "this is used for testing"
                    },
                    "slug": {
                        "type": "string",
                        "example": "test1"
                    },
                    "widgetSlug": {
                        "type": "string",
                        "example": "test1"
                    },
                    "calendarType": {
                        "type": "string",
                        "example": "test1"
                    },
                    "widgetType": {
                        "type": "string",
                        "example": "classic"
                    },
                    "eventTitle": {
                        "type": "string",
                        "default": "{{contact.name}}"
                    },
                    "eventColor": {
                        "type": "string",
                        "default": "#039be5"
                    },
                    "meetingLocation": {
                        "type": "string"
                    },
                    "slotDuration": {
                        "type": "number",
                        "default": 30
                    },
                    "slotInterval": {
                        "type": "number",
                        "default": 30
                    },
                    "slotBuffer": {
                        "type": "number"
                    },
                    "appoinmentPerSlot": {
                        "type": "number",
                        "default": 1
                    },
                    "appoinmentPerDay": {
                        "type": "number"
                    },
                    "openHours": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/OpenHour"
                        }
                    },
                    "formId": {
                        "type": "string"
                    },
                    "stickyContact": {
                        "type": "boolean"
                    },
                    "autoConfirm": {
                        "type": "boolean",
                        "default": true
                    },
                    "shouldSendAlertEmailsToAssignedMember": {
                        "type": "boolean"
                    },
                    "alertEmail": {
                        "type": "string"
                    },
                    "googleInvitationEmails": {
                        "type": "boolean",
                        "default": false
                    },
                    "allowReschedule": {
                        "type": "boolean",
                        "default": true
                    },
                    "allowCancellation": {
                        "type": "boolean",
                        "default": true
                    },
                    "shouldAssignContactToTeamMember": {
                        "type": "boolean"
                    },
                    "shouldSkipAssigningContactForExisting": {
                        "type": "boolean"
                    },
                    "notes": {
                        "type": "string"
                    },
                    "pixelId": {
                        "type": "string"
                    },
                    "formSubmitType": {
                        "type": "string",
                        "default": "ThankYouMessage",
                        "enum": [
                            "RedirectURL",
                            "ThankYouMessage"
                        ]
                    },
                    "formSubmitRedirectURL": {
                        "type": "string"
                    },
                    "formSubmitThanksMessage": {
                        "type": "string"
                    }
                },
                "required": [
                    "locationId",
                    "name"
                ]
            },
            "CalendarByIdSuccessfulResponseDto": {
                "type": "object",
                "properties": {
                    "calendar": {
                        "$ref": "#/components/schemas/CalendarSchema"
                    }
                },
                "required": [
                    "calendar"
                ]
            },
            "Recurring": {
                "type": "object",
                "properties": {}
            },
            "Availability": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string"
                    },
                    "calendarId": {
                        "type": "object"
                    },
                    "date": {
                        "type": "string"
                    },
                    "hours": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Hour"
                        }
                    },
                    "deleted": {
                        "type": "boolean"
                    }
                },
                "required": [
                    "id",
                    "calendarId",
                    "date",
                    "hours",
                    "deleted"
                ]
            },
            "CalendarUpdateSchema": {
                "type": "object",
                "properties": {
                    "notifications": {
                        "description": "Calendar Notifications",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/CalendarNotification"
                        }
                    },
                    "groupId": {
                        "type": "string",
                        "description": "Group Id",
                        "example": "BqTwX8QFwXzpegMve9EQ"
                    },
                    "teamMembers": {
                        "description": "Team members",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/TeamMemeber"
                        }
                    },
                    "eventType": {
                        "type": "string",
                        "enum": [
                            "RoundRobin_OptimizeForAvailability",
                            "RoundRobin_OptimizeForEqualDistribution",
                            "Collective",
                            "Group"
                        ]
                    },
                    "name": {
                        "type": "string",
                        "example": "test calendar"
                    },
                    "description": {
                        "type": "string",
                        "example": "this is used for testing"
                    },
                    "slug": {
                        "type": "string",
                        "example": "test1"
                    },
                    "widgetSlug": {
                        "type": "string",
                        "example": "test1"
                    },
                    "calendarType": {
                        "type": "string",
                        "example": "test1"
                    },
                    "widgetType": {
                        "type": "string",
                        "example": "classic"
                    },
                    "eventTitle": {
                        "type": "string"
                    },
                    "eventColor": {
                        "type": "string"
                    },
                    "meetingLocation": {
                        "type": "string"
                    },
                    "slotDuration": {
                        "type": "number"
                    },
                    "slotInterval": {
                        "type": "object"
                    },
                    "slotBuffer": {
                        "type": "number"
                    },
                    "appoinmentPerSlot": {
                        "type": "number"
                    },
                    "appoinmentPerDay": {
                        "type": "number"
                    },
                    "openHours": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/OpenHour"
                        }
                    },
                    "enableRecurring": {
                        "type": "boolean"
                    },
                    "recurring": {
                        "$ref": "#/components/schemas/Recurring"
                    },
                    "formId": {
                        "type": "string"
                    },
                    "stickyContact": {
                        "type": "boolean"
                    },
                    "isLivePaymentMode": {
                        "type": "boolean"
                    },
                    "autoConfirm": {
                        "type": "boolean"
                    },
                    "shouldSendAlertEmailsToAssignedMember": {
                        "type": "boolean"
                    },
                    "alertEmail": {
                        "type": "string"
                    },
                    "googleInvitationEmails": {
                        "type": "boolean"
                    },
                    "allowReschedule": {
                        "type": "boolean"
                    },
                    "allowCancellation": {
                        "type": "boolean"
                    },
                    "shouldAssignContactToTeamMember": {
                        "type": "boolean"
                    },
                    "shouldSkipAssigningContactForExisting": {
                        "type": "boolean"
                    },
                    "notes": {
                        "type": "string"
                    },
                    "pixelId": {
                        "type": "string"
                    },
                    "formSubmitType": {
                        "type": "string",
                        "default": "ThankYouMessage",
                        "enum": [
                            "RedirectURL",
                            "ThankYouMessage"
                        ]
                    },
                    "formSubmitRedirectURL": {
                        "type": "string"
                    },
                    "formSubmitThanksMessage": {
                        "type": "string"
                    },
                    "availabilityType": {
                        "type": "number",
                        "example": 0
                    },
                    "availabilities": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Availability"
                        }
                    }
                }
            },
            "AppointmentSchemaResponse": {
                "type": "object",
                "properties": {
                    "calendarId": {
                        "type": "string",
                        "description": "Calendar Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    },
                    "locationId": {
                        "type": "string",
                        "description": "Location Id",
                        "example": "C2QujeCh8ZnC7al2InWR"
                    },
                    "contactId": {
                        "type": "string",
                        "description": "Contact Id",
                        "example": "0007BWpSzSwfiuSl0tR2"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start Time",
                        "example": "2021-06-23T03:30:00+05:30"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End Time",
                        "example": "2021-06-23T04:30:00+05:30"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title",
                        "example": "Test Event"
                    },
                    "appointmentStatus": {
                        "type": "string",
                        "example": "confirmed",
                        "enum": [
                            "new",
                            "confirmed",
                            "cancelled",
                            "showed",
                            "noshow",
                            "invalid"
                        ]
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "Assigned User Id",
                        "example": "0007BWpSzSwfiuSl0tR2"
                    },
                    "address": {
                        "type": "string",
                        "description": "Appointment Address",
                        "example": "Zoom"
                    },
                    "id": {
                        "type": "string",
                        "description": "Id",
                        "example": "0TkCdp9PfvLeWKYRRvIz"
                    }
                },
                "required": [
                    "calendarId",
                    "locationId",
                    "contactId",
                    "id"
                ]
            },
            "AppointmentCreateSchema": {
                "type": "object",
                "properties": {
                    "calendarId": {
                        "type": "string",
                        "description": "Calendar Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    },
                    "locationId": {
                        "type": "string",
                        "description": "Location Id",
                        "example": "C2QujeCh8ZnC7al2InWR"
                    },
                    "contactId": {
                        "type": "string",
                        "description": "Contact Id",
                        "example": "0007BWpSzSwfiuSl0tR2"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start Time",
                        "example": "2021-06-23T03:30:00+05:30"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End Time",
                        "example": "2021-06-23T04:30:00+05:30"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title",
                        "example": "Test Event"
                    },
                    "appointmentStatus": {
                        "type": "string",
                        "example": "confirmed",
                        "enum": [
                            "new",
                            "confirmed",
                            "cancelled",
                            "showed",
                            "noshow",
                            "invalid"
                        ]
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "Assigned User Id",
                        "example": "0007BWpSzSwfiuSl0tR2"
                    },
                    "address": {
                        "type": "string",
                        "description": "Appointment Address",
                        "example": "Zoom"
                    },
                    "ignoreDateRange": {
                        "type": "boolean",
                        "description": "If set to true, the minimum scheduling notice and date range would be ignored",
                        "example": false
                    },
                    "toNotify": {
                        "type": "boolean",
                        "description": "If set to false, the automations will not run",
                        "example": false
                    }
                },
                "required": [
                    "calendarId",
                    "locationId",
                    "contactId",
                    "startTime"
                ]
            },
            "AppointmentEditSchema": {
                "type": "object",
                "properties": {
                    "calendarId": {
                        "type": "string",
                        "description": "Calendar Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start Time",
                        "example": "2021-06-23T03:30:00+05:30"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End Time",
                        "example": "2021-06-23T04:30:00+05:30"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title",
                        "example": "Test Event"
                    },
                    "appointmentStatus": {
                        "type": "string",
                        "example": "confirmed",
                        "enum": [
                            "new",
                            "confirmed",
                            "cancelled",
                            "showed",
                            "noshow",
                            "invalid"
                        ]
                    },
                    "address": {
                        "type": "string",
                        "description": "Appointment Address",
                        "example": "Zoom"
                    },
                    "ignoreDateRange": {
                        "type": "boolean",
                        "description": "If set to true, the minimum scheduling notice and date range would be ignored",
                        "example": false
                    },
                    "toNotify": {
                        "type": "boolean",
                        "description": "If set to false, the automations will not run",
                        "example": false
                    }
                }
            },
            "BlockSlotCreateSchema": {
                "type": "object",
                "properties": {
                    "calendarId": {
                        "type": "string",
                        "description": "Calendar Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    },
                    "locationId": {
                        "type": "string",
                        "description": "Location Id",
                        "example": "C2QujeCh8ZnC7al2InWR"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start Time",
                        "example": "2021-06-23T03:30:00+05:30"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End Time",
                        "example": "2021-06-23T04:30:00+05:30"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title",
                        "example": "Test Event"
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "Assigned User Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    }
                },
                "required": [
                    "locationId",
                    "startTime",
                    "endTime"
                ]
            },
            "CreateBookedSlotSuccessfulResponseDto": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Id",
                        "example": "0TkCdp9PfvLeWKYRRvIz"
                    },
                    "locationId": {
                        "type": "string",
                        "description": "Location Id",
                        "example": "C2QujeCh8ZnC7al2InWR"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title",
                        "example": "My event"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start Time",
                        "example": "2021-06-23T03:30:00+05:30"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End Time",
                        "example": "2021-06-23T04:30:00+05:30"
                    },
                    "calendarId": {
                        "type": "string",
                        "description": "Calendar id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "Assigned User Id",
                        "example": "0007BWpSzSwfiuSl0tR2"
                    }
                },
                "required": [
                    "id",
                    "locationId",
                    "title",
                    "startTime",
                    "endTime"
                ]
            },
            "BlockSlotEditSchema": {
                "type": "object",
                "properties": {
                    "calendarId": {
                        "type": "string",
                        "description": "Calendar Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start Time",
                        "example": "2021-06-23T03:30:00+05:30"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End Time",
                        "example": "2021-06-23T04:30:00+05:30"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title",
                        "example": "Test Event"
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "Assigned User Id",
                        "example": "CVokAlI8fgw4WYWoCtQz"
                    }
                }
            },
            "DeleteAppointmentSchema": {
                "type": "object",
                "properties": {}
            },
            "DeleteEventSuccessfulResponseDto": {
                "type": "object",
                "properties": {
                    "succeded": {
                        "type": "boolean",
                        "example": true
                    }
                }
            }
        }
    },
    "paths": {
        "/calendars/{calendarId}/free-slots": {
            "get": {
                "operationId": "get-slots",
                "summary": "Get Free Slots",
                "description": "Get free slots for a calendar between a date range. Optionally a consumer can also request free slots in a particular timezone and also for a particular user.",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "calendarId",
                        "required": true,
                        "in": "path",
                        "description": "Calendar Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "startDate",
                        "required": true,
                        "in": "query",
                        "description": "Start Date",
                        "example": "1548898600000",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "endDate",
                        "required": true,
                        "in": "query",
                        "description": "End Date",
                        "example": "1601490599999",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "timezone",
                        "required": false,
                        "in": "query",
                        "description": "The timezone in which the free slots are returned",
                        "example": "America/Chihuahua",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "userId",
                        "required": false,
                        "in": "query",
                        "description": "The user for whom the free slots are returned",
                        "example": "082goXVW3lIExEQPOnd3",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/GetSlotsSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendars"
                ]
            }
        },
        "/calendars/{calendarId}": {
            "put": {
                "operationId": "update-calendar",
                "summary": "Update Calendar",
                "description": "Update calendar by ID.",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "calendarId",
                        "required": true,
                        "in": "path",
                        "description": "Calendar Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CalendarUpdateSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CalendarByIdSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendars"
                ]
            },
            "get": {
                "operationId": "get-calendar",
                "summary": "Get Calendar",
                "description": "Get calendar by ID",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "calendarId",
                        "required": true,
                        "in": "path",
                        "description": "Calendar Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CalendarByIdSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendars"
                ]
            },
            "delete": {
                "operationId": "delete-calendar",
                "summary": "Delete Calendar",
                "description": "Delete calendar by ID",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "calendarId",
                        "required": true,
                        "in": "path",
                        "description": "Calendar Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CalendarByIdSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendars"
                ]
            }
        },
        "/calendars/events/appointments/{eventId}": {
            "get": {
                "operationId": "get-appointment",
                "summary": "Get Appointment",
                "description": "Get appointment by ID",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "eventId",
                        "required": true,
                        "in": "path",
                        "description": "Event Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AppointmentSchemaResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendar Events"
                ]
            },
            "put": {
                "operationId": "edit-appointment",
                "summary": "Edit Appointment",
                "description": "Edit appointment by ID",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "eventId",
                        "required": true,
                        "in": "path",
                        "description": "Event Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AppointmentEditSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AppointmentSchemaResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendar Events"
                ]
            }
        },
        "/calendars/events/appointments": {
            "post": {
                "operationId": "create-appointment",
                "summary": "Create Appointment",
                "description": "Create appointment",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AppointmentCreateSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AppointmentSchemaResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendar Events"
                ]
            }
        },
        "/calendars/events/block-slots": {
            "post": {
                "operationId": "create-block-slot",
                "summary": "Create Block Slot",
                "description": "Create block slot",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/BlockSlotCreateSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CreateBookedSlotSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendar Events"
                ]
            }
        },
        "/calendars/events/block-slots/{eventId}": {
            "put": {
                "operationId": "edit-block-slot",
                "summary": "Edit Block Slot",
                "description": "Edit block slot by ID",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "eventId",
                        "required": true,
                        "in": "path",
                        "description": "Event Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/BlockSlotEditSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CreateBookedSlotSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendar Events"
                ]
            }
        },
        "/calendars/events/{eventId}": {
            "delete": {
                "operationId": "delete-event",
                "summary": "Delete Event",
                "description": "Delete event by ID",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "eventId",
                        "required": true,
                        "in": "path",
                        "description": "Event Id",
                        "example": "ocQHyuzHvysMo5N5VsXc",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/DeleteAppointmentSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/DeleteEventSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendar Events"
                ]
            }
        },
        "/calendars/": {
            "get": {
                "operationId": "get-calendars",
                "summary": "Get Calendars",
                "description": "Get all calendars in a location.",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    },
                    {
                        "name": "locationId",
                        "required": true,
                        "in": "query",
                        "description": "Location Id",
                        "example": "ve9EPM428h8vShlRW1KT",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "groupId",
                        "required": false,
                        "in": "query",
                        "description": "Group Id",
                        "example": "BqTwX8QFwXzpegMve9EQ",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CalendarsGetSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendars"
                ]
            },
            "post": {
                "operationId": "create-calendar",
                "summary": "Create Calendar",
                "description": "Create calendar in a location.",
                "parameters": [
                    {
                        "name": "Authorization",
                        "in": "header",
                        "description": "Access Token",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "Access Token"
                        }
                    },
                    {
                        "name": "Version",
                        "in": "header",
                        "description": "Api Version",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "example": "2021-04-15"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CalendarCreateSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CalendarByIdSuccessfulResponseDto"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BadRequestDTO"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UnauthorizedDTO"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Calendars"
                ]
            }
        }
    }
}

### License
MIT License

Copyright (c) 2023 Bard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
###END_AUTO_GENERATED###
